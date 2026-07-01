"""Widgets reutilizáveis: Button e helpers de texto."""
import pygame
from constants import FONT_BOLD, FONT_UI, TEXT_LIGHT, COLOR_BUTTON, COLOR_HOVER, COLOR_BORDER, WHITE


class Button:
    def __init__(self, rect, text, on_click=None,
                 color=None, text_color=WHITE, font=None,
                 border_color=COLOR_BORDER, border_radius=8):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.color = color or COLOR_BUTTON
        self.text_color = text_color
        self.font = font or FONT_BOLD
        self.border_color = border_color
        self.border_radius = border_radius
        self.disabled = False
        self.visible = True

    def draw(self, surface):
        if not self.visible:
            return
        hovering = self.rect.collidepoint(pygame.mouse.get_pos()) and not self.disabled
        bg = COLOR_HOVER if hovering else self.color
        if self.disabled:
            bg = tuple(max(0, c - 25) for c in self.color)
        pygame.draw.rect(surface, bg, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, 1, border_radius=self.border_radius)
        col = (110, 118, 126) if self.disabled else self.text_color
        lbl = self.font.render(self.text, True, col)
        surface.blit(lbl, lbl.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if self.disabled or not self.visible:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False


def draw_wrapped(surface, text, rect, font, color=TEXT_LIGHT, line_gap=4, align="left"):
    """Quebra o texto para caber na largura do rect e desenha linha a linha."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= rect.width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = rect.top
    for line in lines:
        surf = font.render(line, True, color)
        x = rect.left + (rect.width - surf.get_width()) // 2 if align == "center" else rect.left
        surface.blit(surf, (x, y))
        y += font.get_height() + line_gap
    return y


def draw_panel(surface, rect, bg=None, border=COLOR_BORDER, radius=10):
    from constants import PANEL_DARK
    pygame.draw.rect(surface, bg or PANEL_DARK, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)
