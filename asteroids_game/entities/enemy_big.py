import pygame as pg
import random
import config as C
from entities.bullet import Bullet

class EnemyBig:
    SPEED = 140
    SHOOT_INTERVAL = 1.0

    def __init__(self, side=None):
        # spawn just outside a random horizontal edge; travel horizontally across the screen
        if side is None:
            side = random.choice(["left","right"])
        if side == "left":
            self.x = -60
            self.vx = self.SPEED
        else:
            self.x = C.WIDTH + 60
            self.vx = -self.SPEED
        self.y = random.randint(50, C.HEIGHT - 50)
        self.timer = 0
        self.alive = True

    def update(self, dt, world):
        self.x += self.vx * dt

        # remove if gone
        if self.x < -100 or self.x > C.WIDTH + 100:
            world.enemy_big = None
            return

        self.timer += dt
        if self.timer >= self.SHOOT_INTERVAL:
            self.timer = 0
            # shoot roughly outward (opposite side of screen): if coming from left, shoot right (positive vx)
            bullet_vx = 350 if self.vx>0 else -350
            world.enemy_bullets.append(Bullet(self.x, self.y, bullet_vx, 0, "enemy"))
            world.audio.play("enemy_shoot")

    def draw(self, screen):
        pg.draw.rect(screen, C.YELLOW, (int(self.x)-24, int(self.y)-12, 48, 24), 0)
