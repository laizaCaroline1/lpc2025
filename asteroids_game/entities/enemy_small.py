import pygame as pg
import math
import random
import config as C
from entities.bullet import Bullet

class EnemySmall:
    SPEED = 120
    SHOOT_INTERVAL = 2.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.alive = True

    def update(self, dt, player, world):
        # move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy) + 1e-6
        nx = dx / dist
        ny = dy / dist
        self.x = (self.x + nx * self.SPEED * dt)
        self.y = (self.y + ny * self.SPEED * dt)
        self.x %= C.WIDTH
        self.y %= C.HEIGHT

        self.timer += dt
        if self.timer >= self.SHOOT_INTERVAL:
            self.timer = 0
            ang = math.atan2(dy, dx)
            vx = math.cos(ang) * 250
            vy = math.sin(ang) * 250
            world.enemy_bullets.append(Bullet(self.x, self.y, vx, vy, "enemy"))
            world.audio.play("enemy_shoot")

    def draw(self, screen):
        pg.draw.circle(screen, C.GREEN, (int(self.x), int(self.y)), 12)
