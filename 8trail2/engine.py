from enum import Enum, auto

import pygame


class Input:
    """入力デバイスからの入力を管理しゲーム内アクションに関連づけるクラス。"""

    def __init__(self):
        self.controls: dict[str, dict] = {"button": {}, "axis": {}, "vector2": {}}
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

    def is_action_pressed(self, action: str) -> bool:
        return self.controls["button"].get(self.actions.get(action), False)

    def get_action_axis_value(self, action: str) -> float:
        return self.controls["axis"].get(self.actions.get(action), 0.0)

    def get_action_vector2_value(self, action: str) -> pygame.Vector2:
        return self.controls["vector2"].get(
            self.actions.get(action), pygame.Vector2(0, 0)
        )


class ActorState(Enum):
    Active = auto()
    Paused = auto()
    Dead = auto()


class Component:
    def __init__(self):
        self.owner: Actor | None = None

    def update(self, dt: float):
        pass


class DrawableComponent(Component):
    def __init__(self):
        super().__init__()

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError


class Sprite2DComponent(DrawableComponent):
    def __init__(self):
        super().__init__()
        self.texture: pygame.Surface = pygame.Surface((0, 0))

    def set_texture(self, texture: pygame.Surface):
        self.texture = texture

    def draw(self, screen: pygame.Surface):
        if self.owner:
            screen.blit(self.texture, self.owner.position)


class AnimSprite2DComponent(Sprite2DComponent):
    def __init__(self):
        super().__init__()
        self.frames: list[pygame.Surface] = []
        self.current_frame = 0
        self.animation_fps = 24

    def update(self, dt: float):
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def set_frames(self, frames: list[pygame.Surface]):
        self.frames = frames

    def draw(self, screen: pygame.Surface):
        if self.owner:
            screen.blit(self.frames[self.current_frame], self.owner.position)


class Actor:
    def __init__(self, game: "Game"):
        self.game = game
        self.state = ActorState.Active
        self.components: list[Component] = []
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.scale = 1.0
        self.rotation = 0.0

    def update_actor(self, dt: float):
        pass

    def update(self, dt: float):
        if self.state == ActorState.Active:
            for component in self.components:
                component.update(dt)
            self.update_actor(dt)
            self.position += self.velocity * dt

    def add_component(self, component: Component):
        component.owner = self
        self.components.append(component)
        if isinstance(component, DrawableComponent):
            self.game.drawables.append(component)

    def remove_component(self, component: Component):
        self.components.remove(component)
        if isinstance(component, DrawableComponent):
            self.game.drawables.remove(component)


class Game:
    def __init__(self, size=(800, 600), title: str | None = None):
        self.screen = pygame.display.set_mode(size)
        if title:
            pygame.display.set_caption(title)
        self.input = Input()
        self.actors: list[Actor] = []
        self.pending_actors: list[Actor] = []
        self.is_updating_actors = False
        self.dead_actors: list[Actor] = []
        self.drawables: list[DrawableComponent] = []

    def reset(self):
        self.actors.clear()
        self.drawables.clear()

    def add_actor(self, actor: Actor):
        if self.is_updating_actors:
            self.pending_actors.append(actor)
        else:
            self.actors.append(actor)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        dt = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.input.event(event)
            self.screen.fill((0, 0, 0))
            self.input.update(dt)
            self.is_updating_actors = True
            for actor in self.actors:
                actor.update(dt)
            self.is_updating_actors = False
            for actor in self.pending_actors:
                self.actors.append(actor)
            self.pending_actors.clear()
            for actor in self.actors:
                if actor.state == ActorState.Dead:
                    self.dead_actors.append(actor)
            for actor in self.dead_actors:
                self.actors.remove(actor)
            for drawable in self.drawables:
                drawable.draw(self.screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000

        pygame.quit()
