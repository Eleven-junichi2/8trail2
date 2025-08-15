"""入力デバイスを抽象化し、ユーザー入力からゲームのアクションをトリガーする処理の実装ためのモジュール。"""

import pygame


class Input:
    def __init__(self):
        self.controls: dict[str, dict] = {}
        self.actions = {}

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.controls["button"][f"keyboard/{event.key}"] = True
        elif event.type == pygame.KEYUP:
            self.controls["button"][f"keyboard/{event.key}"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.controls["button"][f"mouse/{event.button}"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.controls["button"][f"mouse/{event.button}"] = False
        elif event.type == pygame.MOUSEWHEEL:
            self.controls["axis"]["mousewheel/x"] = event.x
            self.controls["axis"]["mousewheel/y"] = event.y
        elif event.type == pygame.MOUSEMOTION:
            self.controls["vector2"]["mousemotion/position"] = pygame.Vector2(event.pos)
            self.controls["vector2"]["mousemotion/delta_position"] = pygame.Vector2(
                event.rel
            )

    def update(self, dt: float):
        for key_code, pressed in enumerate(pygame.key.get_pressed()):
            self.controls["button"][f"keyboard/{key_code}"] = pressed
        for button, pressed in enumerate(pygame.mouse.get_pressed()):
            self.controls["button"][f"mouse/{button}"] = pressed
        self.controls["vector2"]["mouse/position"] = pygame.Vector2(
            pygame.mouse.get_pos()
        )
        self.controls["vector2"]["mouse/delta_position"] = pygame.Vector2(
            pygame.mouse.get_rel()
        )

    def bind_action(self, action: str, control: str):
        self.actions[action] = control

    def is_action_pressed(self, action: str):
        return self.controls["button"].get(self.actions.get(action))

    def get_action_axis_value(self, action: str):
        return self.controls["axis"].get(self.actions.get(action))

    def get_action_vector2_value(self, action: str):
        return self.controls["vector2"].get(self.actions.get(action))
