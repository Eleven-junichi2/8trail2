from engine import Game

import pygame

pygame.init()


def main():
    game = Game()
    game.init()
    game.run()


if __name__ == "__main__":
    main()
