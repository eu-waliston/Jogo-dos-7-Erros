"""
Telas de questionario, selecao direta e resultado de perfil.
Equivalente a questionnaire.js — gerencia o fluxo de perguntas e
determina a trilha/tema do jogador.
"""
import pygame
from constants import (
    WIDTH, HEIGHT, BG_DARK, TEXT_LIGHT, TEXT_MUTED, WHITE,
    COLOR_BORDER, COLOR_SUCCESS, COLOR_PRIMARY, COLOR_HOVER,
    FONT_TITLE, FONT_SUBTITLE, FONT_BOLD, FONT_UI, FONT_SMALL,
)
from widgets import Button, draw_wrapped, draw_panel
from game_data import QUESTIONS, TRAILS, THEMES, TRAIL_TO_PROFILE, PROFILES, apply_theme_to_profile

import json, os
SAVE_PATH = os.path.join(os.path.dirname(__file__), "player_profile.json")


def save_profile(trail, theme):
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump({"trail": trail, "theme": theme}, f)
    except Exception as e:
        print(f"[AVISO] Nao foi possivel salvar perfil: {e}")


def load_profile():
    try:
        with open(SAVE_PATH) as f:
            data = json.load(f)
        if data.get("trail") and data.get("theme"):
            return data
    except Exception:
        pass
    return None


def clear_profile():
    try:
        os.remove(SAVE_PATH)
    except Exception:
        pass


class QuestionnaireScreen:
    """Gerencia toda a sequencia de telas ate comecar o jogo."""

    def __init__(self, screen, on_complete):
        self.screen = screen
        self.on_complete = on_complete  # callback(profile_dict, theme_dict)
        self.state = "welcome"          # welcome | quiz | trail_select | theme_select | result
        self.scores = {k: 0 for k in TRAILS}
        self.theme_scores = {k: 0 for k in THEMES}
        self.q_index = 0
        self.chosen_trail = None
        self.chosen_theme = None
        self.buttons = []
        self._build_welcome()

    # ------------------------------------------------------------------ build
    def _clear(self):
        self.buttons = []

    def _build_welcome(self):
        self.state = "welcome"
        self._clear()
        cx = WIDTH // 2
        self.buttons.append(Button(
            (cx - 160, 340, 320, 52), "Fazer Questionario",
            on_click=self._start_quiz,
            color=COLOR_PRIMARY,
        ))
        self.buttons.append(Button(
            (cx - 160, 410, 320, 52), "Escolher Trilha Direta",
            on_click=self._show_trail_select,
            color=(55, 65, 81),
        ))
        saved = load_profile()
        if saved:
            self.buttons.append(Button(
                (cx - 160, 480, 320, 52), "Continuar Perfil Salvo",
                on_click=lambda: self._use_saved(saved),
                color=(22, 101, 52),
            ))

    def _start_quiz(self):
        self.scores = {k: 0 for k in TRAILS}
        self.theme_scores = {k: 0 for k in THEMES}
        self.q_index = 0
        self._build_question()

    def _build_question(self):
        self.state = "quiz"
        self._clear()
        q = QUESTIONS[self.q_index]
        cx = WIDTH // 2
        for i, opt in enumerate(q["options"]):
            idx = i
            def make_cb(o=opt):
                return lambda: self._answer(o)
            self.buttons.append(Button(
                (cx - 220, 310 + idx * 72, 440, 56), opt["text"],
                on_click=make_cb(),
                color=(33, 38, 45),
            ))

    def _answer(self, option):
        if "scores" in option:
            for k, v in option["scores"].items():
                self.scores[k] = self.scores.get(k, 0) + v
        if "theme" in option:
            self.theme_scores[option["theme"]] = self.theme_scores.get(option["theme"], 0) + 3
        self.q_index += 1
        if self.q_index >= len(QUESTIONS):
            self._determine_result()
        else:
            self._build_question()

    def _determine_result(self):
        priority = ["mestre", "hacker", "explorador", "iniciante"]
        best_score = max(self.scores.values())
        winners = [k for k, v in self.scores.items() if v == best_score]
        trail = next((p for p in priority if p in winners), winners[0])
        best_theme_score = max(self.theme_scores.values()) if any(self.theme_scores.values()) else 0
        theme_winners = [k for k, v in self.theme_scores.items() if v == best_theme_score]
        theme = theme_winners[0] if theme_winners else "tecnologia"
        self.chosen_trail = trail
        self.chosen_theme = theme
        self._build_result()

    def _build_result(self):
        self.state = "result"
        self._clear()
        cx = WIDTH // 2
        self.buttons.append(Button(
            (cx - 200, 520, 185, 50), "Comecar o Jogo",
            on_click=self._start_game, color=COLOR_SUCCESS,
        ))
        self.buttons.append(Button(
            (cx + 15, 520, 185, 50), "Refazer Quiz",
            on_click=self._start_quiz, color=(33, 38, 45),
        ))

    def _show_trail_select(self):
        self.state = "trail_select"
        self._clear()
        cx = WIDTH // 2
        for i, (tid, trail) in enumerate(TRAILS.items()):
            col = i % 2
            row = i // 2
            x = cx - 240 + col * 250
            y = 250 + row * 130
            def make_cb(t=tid):
                return lambda: self._pick_trail(t)
            self.buttons.append(Button(
                (x, y, 220, 100), trail["name"],
                on_click=make_cb(), color=trail["color"],
            ))
        self.buttons.append(Button(
            (cx - 80, 550, 160, 44), "Voltar",
            on_click=self._build_welcome, color=(55, 65, 81),
        ))

    def _pick_trail(self, trail_id):
        self.chosen_trail = trail_id
        self._show_theme_select()

    def _show_theme_select(self):
        self.state = "theme_select"
        self._clear()
        cx = WIDTH // 2
        for i, (tid, theme) in enumerate(THEMES.items()):
            col = i % 2
            row = i // 2
            x = cx - 240 + col * 250
            y = 250 + row * 110
            def make_cb(t=tid):
                return lambda: self._pick_theme(t)
            self.buttons.append(Button(
                (x, y, 220, 88), theme["name"],
                on_click=make_cb(), color=(33, 38, 45),
            ))
        self.buttons.append(Button(
            (cx - 80, 550, 160, 44), "Voltar",
            on_click=self._show_trail_select, color=(55, 65, 81),
        ))

    def _pick_theme(self, theme_id):
        self.chosen_theme = theme_id
        self._build_result()

    def _use_saved(self, saved):
        self.chosen_trail = saved["trail"]
        self.chosen_theme = saved["theme"]
        self._start_game()

    def _start_game(self):
        save_profile(self.chosen_trail, self.chosen_theme)
        profile_key = TRAIL_TO_PROFILE.get(self.chosen_trail, "detetive")
        profile = apply_theme_to_profile(PROFILES[profile_key], THEMES[self.chosen_theme])
        self.on_complete(profile, THEMES[self.chosen_theme], self.chosen_trail)

    # ------------------------------------------------------------------ draw
    def draw(self):
        self.screen.fill(BG_DARK)
        if self.state == "welcome":
            self._draw_welcome()
        elif self.state == "quiz":
            self._draw_quiz()
        elif self.state in ("trail_select", "theme_select"):
            self._draw_select()
        elif self.state == "result":
            self._draw_result()
        for btn in self.buttons:
            btn.draw(self.screen)

    def _draw_welcome(self):
        title = FONT_TITLE.render("Caca aos Bugs!", True, (34, 197, 94))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))
        sub = FONT_UI.render("Encontre e corrija erros de codigo antes que o inimigo fuja!", True, TEXT_MUTED)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 220)))
        instr = FONT_UI.render("Como deseja comecar?", True, TEXT_LIGHT)
        self.screen.blit(instr, instr.get_rect(center=(WIDTH // 2, 295)))

    def _draw_quiz(self):
        q = QUESTIONS[self.q_index]
        prog = FONT_SMALL.render(f"Pergunta {self.q_index + 1} de {len(QUESTIONS)}", True, TEXT_MUTED)
        self.screen.blit(prog, (40, 40))
        bar_w = int((self.q_index / len(QUESTIONS)) * (WIDTH - 80))
        pygame.draw.rect(self.screen, (33, 38, 45), (40, 65, WIDTH - 80, 8), border_radius=4)
        if bar_w > 0:
            pygame.draw.rect(self.screen, COLOR_SUCCESS, (40, 65, bar_w, 8), border_radius=4)
        draw_wrapped(self.screen, q["question"],
                     pygame.Rect(WIDTH // 2 - 300, 120, 600, 150),
                     FONT_SUBTITLE, TEXT_LIGHT, align="center")

    def _draw_select(self):
        if self.state == "trail_select":
            title_text = "Escolha sua Trilha"
        else:
            title_text = "Escolha o Tema Narrativo"
        title = FONT_TITLE.render(title_text, True, TEXT_LIGHT)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))

    def _draw_result(self):
        trail = TRAILS[self.chosen_trail]
        theme = THEMES[self.chosen_theme]
        profile_key = TRAIL_TO_PROFILE.get(self.chosen_trail, "detetive")
        profile = PROFILES[profile_key]

        title = FONT_TITLE.render("Seu Perfil!", True, (251, 191, 36))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        draw_panel(self.screen, pygame.Rect(WIDTH // 2 - 300, 155, 600, 330))

        trail_lbl = FONT_SUBTITLE.render(f"Trilha: {trail['name']}", True, trail["color"])
        self.screen.blit(trail_lbl, trail_lbl.get_rect(center=(WIDTH // 2, 200)))

        profile_lbl = FONT_BOLD.render(f"Personagem: {profile['name']}", True, TEXT_LIGHT)
        self.screen.blit(profile_lbl, profile_lbl.get_rect(center=(WIDTH // 2, 250)))

        theme_lbl = FONT_UI.render(f"Tema: {theme['name']}", True, TEXT_MUTED)
        self.screen.blit(theme_lbl, theme_lbl.get_rect(center=(WIDTH // 2, 295)))

        enemy_lbl = FONT_UI.render(f"Inimigo: {profile['enemy_name']}", True, COLOR_PRIMARY)
        self.screen.blit(enemy_lbl, enemy_lbl.get_rect(center=(WIDTH // 2, 335)))

        draw_wrapped(self.screen, trail["description"],
                     pygame.Rect(WIDTH // 2 - 260, 370, 520, 80),
                     FONT_SMALL, TEXT_MUTED, align="center")

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)
