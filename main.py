"""
Ponto de entrada do jogo. Gerencia a maquina de estados de telas:
  welcome/quiz/result  →  (QuestionnaireScreen)
  game                 →  (Minigame)
"""
import os
os.environ["SDL_VIDEODRIVER"] = os.environ.get("SDL_VIDEODRIVER", "x11")

import pygame
import sys

from constants import WIDTH, HEIGHT, FPS, BG_DARK
import music


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caca aos Bugs!")
    clock = pygame.time.Clock()

    # Inicia música de fundo em thread separada
    music.start()

    current_screen = None

    def go_to_questionnaire():
        nonlocal current_screen
        from questionnaire import QuestionnaireScreen
        current_screen = QuestionnaireScreen(screen, on_quiz_complete)

    def on_quiz_complete(profile, theme, trail):
        nonlocal current_screen
        from minigame import Minigame
        current_screen = Minigame(screen, profile, theme, trail, go_to_questionnaire)

    go_to_questionnaire()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if current_screen:
                current_screen.handle_event(event)

        if hasattr(current_screen, "update"):
            current_screen.update()

        screen.fill(BG_DARK)
        if current_screen:
            current_screen.draw()

        pygame.display.flip()
        clock.tick(FPS)

    music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
