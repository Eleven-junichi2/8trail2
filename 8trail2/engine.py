from enum import Enum, auto

import pygame


class ActorState(Enum):
    Active = auto()
    Paused = auto()
    Dead = auto()


class Component:
    def update(self, dt: float):
        pass


class Actor:
    def __init__(self):
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

    def add_component(self, component: Component):
        self.components.append(component)

    def remove_component(self, component: Component):
        self.components.remove(component)


class Game:
    def init(self):
        self.actors: list[Actor] = []
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("8trail2")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        dt = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))
            for actor in self.actors:
                actor.update(dt)
            pygame.display.flip()
            dt += clock.tick(60) / 1000

        pygame.quit()
