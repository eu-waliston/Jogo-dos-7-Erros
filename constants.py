"""Constantes globais: cores, dimensões e fontes."""
import pygame

WIDTH, HEIGHT = 1100, 680
FPS = 60

BG_DARK        = (13, 17, 23)
PANEL_DARK     = (1, 4, 9)
TEXT_LIGHT     = (230, 237, 243)
TEXT_MUTED     = (150, 160, 170)
WHITE          = (255, 255, 255)
COLOR_SUCCESS  = (34, 197, 94)
COLOR_ERROR    = (239, 68, 68)
COLOR_WARNING  = (249, 115, 22)
COLOR_PRIMARY  = (37, 99, 235)
COLOR_BORDER   = (48, 54, 61)
COLOR_BUTTON   = (33, 38, 45)
COLOR_HOVER    = (55, 65, 81)
COLOR_PURPLE   = (139, 92, 246)
COLOR_GREEN    = (34, 197, 94)

pygame.font.init()
_MONO = pygame.font.match_font("couriernew,consolas,dejavusansmono,freemono,monospace")

def font(size, bold=False):
    f = pygame.font.Font(_MONO, size)
    if bold:
        f.set_bold(True)
    return f

FONT_CODE     = font(17)
FONT_UI       = font(17)
FONT_BOLD     = font(17, bold=True)
FONT_TITLE    = font(32, bold=True)
FONT_SUBTITLE = font(20, bold=True)
FONT_SMALL    = font(13)
