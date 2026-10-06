"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FALLING_OBJECT_RADIUS, FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MIN_SPAWN_INTERVAL_FRAMES = 35
MAX_SPAWN_INTERVAL_FRAMES = 65
MIN_SPAWN_DISTANCE = 60
MAX_ACTIVE_OBJECTS = 5
MAX_MISSES = 5
BOOST_DURATION_FRAMES = 180


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        min_x = FALLING_OBJECT_RADIUS
        max_x = WIDTH - FALLING_OBJECT_RADIUS
        x = random.randint(min_x, max_x)
        while self.last_spawn_x is not None and abs(x - self.last_spawn_x) < MIN_SPAWN_DISTANCE:
            x = random.randint(min_x, max_x)

        self.last_spawn_x = x
        self.objects.append(FallingObject(
            x=x, y=FALLING_OBJECT_RADIUS, speed=3,
        ))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        movement = 0
        if keys_pressed[pygame.K_LEFT]:
            movement -= 1
        if keys_pressed[pygame.K_RIGHT]:
            movement += 1

        self.basket.x += movement * self.basket.speed
        half_width = self.basket.width / 2
        self.basket.x = max(half_width, min(WIDTH - half_width, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.basket.boosted_frames = BOOST_DURATION_FRAMES
            self.basket.speed = self.basket.boost_speed

    def update(self):
        if self.game_over:
            return

        if self.basket.boosted_frames > 0:
            self.basket.boosted_frames -= 1
            if self.basket.boosted_frames == 0:
                self.basket.speed = self.basket.normal_speed

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_ACTIVE_OBJECTS:
                self._spawn_object()
            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL_FRAMES, MAX_SPAWN_INTERVAL_FRAMES,
            )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        caught_objects = []

        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
                caught_objects.append(obj)

        for obj in caught_objects:
            self.objects.remove(obj)

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.boosted_frames > 0:
            renderer.draw_text(surface, font, "SPEED BOOST!", (10, 62))

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
