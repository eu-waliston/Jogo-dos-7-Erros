"""
Tela de jogo em si: código errado vs correto, círculos de erro,
animação do inimigo atravessando a tela, dicas e parabéns.
Equivalente à lógica de gameplay de script.js.
"""
import pygame
import math
import time
from constants import (
    WIDTH, HEIGHT, BG_DARK, PANEL_DARK, TEXT_LIGHT, TEXT_MUTED, WHITE,
    COLOR_BORDER, COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING,
    COLOR_PRIMARY, COLOR_HOVER,
    FONT_CODE, FONT_UI, FONT_BOLD, FONT_TITLE, FONT_SUBTITLE, FONT_SMALL,
)
from widgets import Button, draw_wrapped, draw_panel
from game_data import LEVELS


LINE_H = 26          # altura de cada linha de código
CODE_PAD_X = 16      # margem esquerda dentro do painel de código
CODE_PAD_Y = 14
CIRCLE_R = 10        # raio do círculo de erro
PANEL_TOP = 130      # y onde os painéis de código começam
PANEL_H = 220        # altura dos painéis de código
CODE_W = 490         # largura de cada painel de código
CODE_LEFT = 30       # x do painel de código errado
CODE_RIGHT = WIDTH - CODE_W - 30   # x do painel de código correto


class Enemy:
    """Inimigo que atravessa a tela quando rouba o código."""
    SIZE = 28

    def __init__(self, shape, color, eye_color, direction=1):
        self.shape = shape      # "square" | "triangle" | "square_eyes"
        self.color = color
        self.eye_color = eye_color
        self.direction = direction  # 1 = esquerda->direita, -1 = direita->esquerda
        self.reset()

    def reset(self):
        self.active = False
        self.x = -self.SIZE if self.direction == 1 else WIDTH + self.SIZE
        self.y = HEIGHT // 2 - 20
        self.speed = 4.5

    def start(self):
        self.active = True
        self.x = -self.SIZE if self.direction == 1 else WIDTH + self.SIZE

    @property
    def done(self):
        if self.direction == 1:
            return self.x > WIDTH + self.SIZE
        return self.x < -self.SIZE

    def update(self):
        if self.active:
            self.x += self.speed * self.direction

    def draw(self, surface):
        if not self.active:
            return
        x, y, s = int(self.x), int(self.y), self.SIZE
        if self.shape == "square":
            pygame.draw.rect(surface, self.color, (x, y, s, s))
            # olhos
            pygame.draw.rect(surface, self.eye_color, (x + 4, y + 6, 6, 6))
            pygame.draw.rect(surface, self.eye_color, (x + 16, y + 6, 6, 6))
        elif self.shape == "triangle":
            pts = [(x + s // 2, y), (x + s, y + s), (x, y + s)]
            pygame.draw.polygon(surface, self.color, pts)
            pygame.draw.rect(surface, self.eye_color, (x + 8, y + s // 2, 10, 4))
        elif self.shape == "square_eyes":
            pygame.draw.rect(surface, self.color, (x, y, s, s))
            pygame.draw.rect(surface, self.eye_color, (x, y + 6, s, 8))
            pygame.draw.rect(surface, (0, 0, 0), (x + 4, y + 8, 4, 4))
            pygame.draw.rect(surface, (0, 0, 0), (x + 16, y + 8, 4, 4))


class Minigame:
    def __init__(self, screen, profile, theme, trail, on_back):
        self.screen = screen
        self.profile = profile      # dict (cópia já temática)
        self.theme = theme
        self.trail = trail
        self.on_back = on_back      # callback para voltar ao menu
        self.current_level = 0
        self.total_levels = len(LEVELS)
        self._reset_level_state()
        self._build_hud_buttons()
        self._init_correct_surf()   # renderiza o canvas correto uma só vez
        self.enemy = Enemy(
            profile["enemy_shape"],
            profile["enemy_color"],
            profile["enemy_eye_color"],
        )

    # ---------------------------------------------------------------- init
    def _reset_level_state(self):
        self.errors = []            # lista de dicts com posição, found, etc.
        self.attempts = 0
        self.wrong_attempts = 0
        self.can_click = True
        self.level_completed = False
        self.show_steal_msg = False
        self.steal_msg_timer = 0
        self.pulse_t = 0
        self.hint_index = -1
        self.show_hint = False
        self.hint_timer = 0
        self.show_congrats = False
        self.show_game_over = False
        self._build_error_positions()

    def _build_error_positions(self):
        lvl = LEVELS[self.current_level]
        lines = lvl["wrong_code"].split("\n")
        self.errors = []
        for err in lvl["errors"]:
            line_idx = err["line"]
            char_pos = min(err["char_pos"], len(lines[line_idx]) if line_idx < len(lines) else 0)
            x = CODE_LEFT + CODE_PAD_X + FONT_CODE.size(lines[line_idx][:char_pos])[0]
            y = PANEL_TOP + CODE_PAD_Y + line_idx * LINE_H + LINE_H // 2
            self.errors.append({
                "x": x, "y": y,
                "explanation": err["explanation"],
                "found": False,
            })

    def _init_correct_surf(self):
        """Renderiza o código correto em uma Surface estática (não muda nunca)."""
        self.correct_surf = pygame.Surface((CODE_W, PANEL_H))
        self._draw_code_to_surf(self.correct_surf, LEVELS[self.current_level]["correct_code"])

    def _draw_code_to_surf(self, surf, code):
        from constants import PANEL_DARK
        surf.fill(PANEL_DARK)
        lines = code.split("\n")
        for i, line in enumerate(lines):
            col = self._syntax_color(line)
            lbl = FONT_CODE.render(line, True, col)
            surf.blit(lbl, (CODE_PAD_X, CODE_PAD_Y + i * LINE_H))

    def _syntax_color(self, line):
        stripped = line.strip()
        keywords = ("def ", "if ", "else:", "elif ", "for ", "while ", "return ",
                    "import ", "from ", "class ", "break", "continue", "print")
        html_tags = stripped.startswith("<")
        if any(stripped.startswith(k) for k in keywords):
            return (197, 134, 192)
        if html_tags:
            return (86, 156, 214)
        if stripped.startswith("#") or stripped.startswith("<!--"):
            return (106, 153, 85)
        return TEXT_LIGHT

    def _build_hud_buttons(self):
        self.btn_hint = Button(
            (WIDTH // 2 - 80, HEIGHT - 60, 160, 40), "Dica",
            on_click=self._show_hint_action,
            color=(55, 65, 81),
        )
        self.btn_next = Button(
            (WIDTH - 170, HEIGHT - 60, 150, 40), "Proximo Nivel",
            on_click=self._next_level,
            color=COLOR_SUCCESS,
        )
        self.btn_next.disabled = True
        self.btn_back = Button(
            (20, HEIGHT - 60, 100, 40), "Menu",
            on_click=self._back_to_menu,
            color=(55, 65, 81),
        )
        self.btn_music = Button(
            (WIDTH - 130, 10, 120, 34), "Musica: ON",
            on_click=self._toggle_music,
            color=(33, 38, 45),
        )
        self._music_on = True
        self.hud_buttons = [self.btn_hint, self.btn_next, self.btn_back, self.btn_music]

    # ---------------------------------------------------------------- actions
    def _toggle_music(self):
        import music
        muted = music.toggle_mute()
        self.btn_music.text = "Musica: OFF" if muted else "Musica: ON"
        self._music_on = not muted

    def _show_hint_action(self):
        self.hint_index = (self.hint_index + 1) % len(self.errors)
        self.show_hint = True
        self.hint_timer = 180  # frames (~3s)

    def _next_level(self):
        self.current_level += 1
        if self.current_level >= self.total_levels:
            self.show_game_over = True   # reaproveitando flag para "fim de jogo" (vitória)
            return
        self._reset_level_state()
        self._init_correct_surf()
        self.btn_next.disabled = True

    def _back_to_menu(self):
        from questionnaire import clear_profile
        clear_profile()
        self.on_back()

    # ---------------------------------------------------------------- click
    def handle_event(self, event):
        for btn in self.hud_buttons:
            btn.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.can_click and not self.level_completed:
                self._check_click(event.pos)

    def _check_click(self, pos):
        mx, my = pos
        self.attempts += 1
        hit = False
        for err in self.errors:
            if not err["found"]:
                dist = math.hypot(mx - err["x"], my - err["y"])
                if dist <= CIRCLE_R + 12:
                    err["found"] = True
                    hit = True
                    self._trigger_steal_msg(err["explanation"])
                    break
        if not hit:
            self.wrong_attempts += 1
            self._flash_wrong(pos)
        # verifica se todos foram encontrados
        if all(e["found"] for e in self.errors):
            self.level_completed = True
            self.can_click = False
            self.btn_next.disabled = (self.current_level >= self.total_levels - 1)
            self.show_congrats = True

    def _trigger_steal_msg(self, explanation):
        self.current_hint_text = explanation
        self.show_steal_msg = True
        self.steal_msg_timer = 150
        self.enemy.start()

    def _flash_wrong(self, pos):
        # pequena partícula vermelha (desenhada por 1 frame via flag)
        self._wrong_flash = pos
        self._wrong_flash_timer = 18

    # ---------------------------------------------------------------- update
    def update(self):
        self.pulse_t += 0.07
        if self.steal_msg_timer > 0:
            self.steal_msg_timer -= 1
        else:
            self.show_steal_msg = False
        if self.hint_timer > 0:
            self.hint_timer -= 1
        else:
            self.show_hint = False
        if hasattr(self, "_wrong_flash_timer") and self._wrong_flash_timer > 0:
            self._wrong_flash_timer -= 1
        self.enemy.update()
        if self.enemy.done:
            self.enemy.reset()

    # ---------------------------------------------------------------- draw
    def draw(self):
        self.screen.fill(BG_DARK)
        self._draw_hud()
        self._draw_code_panels()
        self._draw_error_circles()
        self.enemy.draw(self.screen)
        if self.show_steal_msg:
            self._draw_steal_msg()
        if self.show_hint:
            self._draw_hint()
        if hasattr(self, "_wrong_flash_timer") and self._wrong_flash_timer > 0:
            self._draw_wrong_flash()
        if self.show_congrats:
            self._draw_congrats()
        if self.show_game_over:
            self._draw_game_over()
        for btn in self.hud_buttons:
            btn.draw(self.screen)

    def _draw_hud(self):
        lvl = LEVELS[self.current_level]
        level_name = self.profile["level_names"][self.current_level]
        title = FONT_BOLD.render(f"{lvl['language']} | {level_name}", True, TEXT_LIGHT)
        self.screen.blit(title, (20, 14))

        found = sum(1 for e in self.errors if e["found"])
        remaining = len(self.errors) - found
        stats = (f"Tentativas: {self.attempts}  |  "
                 f"Erros: {self.wrong_attempts}  |  "
                 f"Encontrados: {found}/{len(self.errors)}  |  "
                 f"Nivel: {self.current_level + 1}/{self.total_levels}")
        stat_lbl = FONT_SMALL.render(stats, True, TEXT_MUTED)
        self.screen.blit(stat_lbl, (20, 46))

        # labels dos painéis
        err_lbl = FONT_SMALL.render("CODIGO COM ERROS (clique nos circulos!)", True, COLOR_ERROR)
        self.screen.blit(err_lbl, (CODE_LEFT, PANEL_TOP - 22))
        cor_lbl = FONT_SMALL.render("CODIGO CORRETO (referencia)", True, COLOR_SUCCESS)
        self.screen.blit(cor_lbl, (CODE_RIGHT, PANEL_TOP - 22))

    def _draw_code_panels(self):
        # Painel esquerdo: código errado (redesenhado a cada frame pois tem circles)
        err_surf = pygame.Surface((CODE_W, PANEL_H))
        self._draw_code_to_surf(err_surf, LEVELS[self.current_level]["wrong_code"])
        pygame.draw.rect(self.screen, (1, 4, 9), (CODE_LEFT, PANEL_TOP, CODE_W, PANEL_H))
        self.screen.blit(err_surf, (CODE_LEFT, PANEL_TOP))
        pygame.draw.rect(self.screen, COLOR_BORDER, (CODE_LEFT, PANEL_TOP, CODE_W, PANEL_H), 1, border_radius=6)

        # Painel direito: código correto (surface estática, só blit)
        pygame.draw.rect(self.screen, (1, 4, 9), (CODE_RIGHT, PANEL_TOP, CODE_W, PANEL_H))
        self.screen.blit(self.correct_surf, (CODE_RIGHT, PANEL_TOP))
        pygame.draw.rect(self.screen, COLOR_BORDER, (CODE_RIGHT, PANEL_TOP, CODE_W, PANEL_H), 1, border_radius=6)

    def _draw_error_circles(self):
        pulse = 0.5 + 0.5 * math.sin(self.pulse_t)
        for err in self.errors:
            if err["found"]:
                pygame.draw.circle(self.screen, COLOR_SUCCESS, (err["x"], err["y"]), CIRCLE_R)
                check = FONT_SMALL.render("✓", True, WHITE)
                self.screen.blit(check, check.get_rect(center=(err["x"], err["y"])))
            else:
                alpha_r = int(CIRCLE_R + 4 * pulse)
                color = (
                    int(239 * pulse + 249 * (1 - pulse)),
                    int(68 * pulse + 115 * (1 - pulse)),
                    int(68 * pulse),
                )
                pygame.draw.circle(self.screen, color, (err["x"], err["y"]), alpha_r, 2)
                pygame.draw.circle(self.screen, color, (err["x"], err["y"]), CIRCLE_R)
                q = FONT_SMALL.render("?", True, WHITE)
                self.screen.blit(q, q.get_rect(center=(err["x"], err["y"])))

    def _draw_steal_msg(self):
        msg = self.profile["steal_msg"]
        panel = pygame.Rect(CODE_LEFT, PANEL_TOP + PANEL_H + 12, WIDTH - CODE_LEFT * 2, 60)
        draw_panel(self.screen, panel, bg=(60, 20, 20))
        draw_wrapped(self.screen, msg, panel.inflate(-20, -10), FONT_UI, COLOR_ERROR, align="center")
        if hasattr(self, "current_hint_text"):
            hint_lbl = FONT_SMALL.render(self.current_hint_text, True, COLOR_WARNING)
            self.screen.blit(hint_lbl, hint_lbl.get_rect(center=(WIDTH // 2, panel.bottom + 18)))

    def _draw_hint(self):
        if self.hint_index < 0 or self.hint_index >= len(self.errors):
            return
        err = self.errors[self.hint_index]
        txt = f"DICA: {err['explanation']}"
        panel = pygame.Rect(CODE_LEFT, HEIGHT - 115, WIDTH - CODE_LEFT * 2, 46)
        draw_panel(self.screen, panel, bg=(30, 40, 10))
        draw_wrapped(self.screen, txt, panel.inflate(-16, -8), FONT_UI, COLOR_SUCCESS, align="center")

    def _draw_wrong_flash(self):
        if hasattr(self, "_wrong_flash"):
            pygame.draw.circle(self.screen, COLOR_ERROR, self._wrong_flash, 14, 2)

    def _draw_congrats(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        box = pygame.Rect(WIDTH // 2 - 260, HEIGHT // 2 - 120, 520, 240)
        draw_panel(self.screen, box, bg=(5, 30, 10))
        title = FONT_TITLE.render(self.profile["win_msg"][:30], True, COLOR_SUCCESS)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        sub = FONT_UI.render(f"Nivel {self.current_level + 1} concluido!", True, TEXT_LIGHT)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if self.current_level < self.total_levels - 1:
            instr = FONT_SMALL.render("Clique em 'Proximo Nivel' para continuar", True, TEXT_MUTED)
        else:
            instr = FONT_SMALL.render("Voce completou todos os niveis! Clique em 'Proximo Nivel'", True, TEXT_MUTED)
        self.screen.blit(instr, instr.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    def _draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        box = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 140, 600, 280)
        draw_panel(self.screen, box, bg=(5, 20, 35))
        title = FONT_TITLE.render("PARABENS! JOGO COMPLETO!", True, (251, 191, 36))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        sub = FONT_SUBTITLE.render(f"Voce venceu o {self.profile['enemy_name']}!", True, COLOR_SUCCESS)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        stats = FONT_UI.render(
            f"Tentativas totais: {self.attempts}  |  Erros: {self.wrong_attempts}", True, TEXT_MUTED)
        self.screen.blit(stats, stats.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        instr = FONT_SMALL.render("Clique em 'Menu' para jogar novamente", True, TEXT_MUTED)
        self.screen.blit(instr, instr.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90)))
