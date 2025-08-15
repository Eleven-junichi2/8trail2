from pathlib import Path

from engine import Game, Sprite2DComponent, Actor, AnimSprite2DComponent

import pygame

pygame.init()


class Player(Actor):
    def __init__(self, game: "Game"):
        super().__init__(game)
        image = pygame.image.load(Path(__file__).parent / "assets/images/player.png").convert_alpha()
        animsprite_component = AnimSprite2DComponent()
        frames = [image.subsurface(pygame.Rect(0, i * 22, 22, 22)) for i in range(4)]
        animsprite_component.set_frames(frames)
        # self.add_component(animsprite_component)
        # sprite_component = Sprite2DComponent()
        # sprite_component.set_texture(image)
        # self.add_component(sprite_component)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 220.0
        self.game.input.bind_action("move_left", f"keyboard/{pygame.K_LEFT}")
        self.game.input.bind_action("move_up", f"keyboard/{pygame.K_UP}")
        self.game.input.bind_action("move_right", f"keyboard/{pygame.K_RIGHT}")
        self.game.input.bind_action("move_down", f"keyboard/{pygame.K_DOWN}")

    def update_actor(self, dt: float):
        self.direction.x = self.game.input.is_action_pressed(
            "move_right"
        ) - self.game.input.is_action_pressed("move_left")
        self.direction.y = self.game.input.is_action_pressed(
            "move_down"
        ) - self.game.input.is_action_pressed("move_up")
        if self.direction.length_squared() > 0:
            self.velocity = self.direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)


def main():
    game = Game()
    game.add_actor(Player(game))
    game.run()


if __name__ == "__main__":
    main()
