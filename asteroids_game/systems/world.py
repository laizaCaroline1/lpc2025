import random
import config as C
from entities.player import Player
from entities.asteroid import Asteroid
from entities.bullet import Bullet
from entities.enemy_small import EnemySmall
from entities.enemy_big import EnemyBig
from audio.audio import Audio

class World:
    def __init__(self):
        self.player = Player()
        self.asteroids = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies_small = []
        self.enemy_big = None

        self.audio = Audio()
        self.spawn_asteroids(6)

    def try_fire(self):
        vx = self.player.dirx * 350
        vy = self.player.diry * 350
        self.bullets.append(Bullet(self.player.x, self.player.y, vx, vy, "player"))
        self.audio.play("laser")

    def hyperspace(self):
        self.player.random_position()

    def spawn_asteroids(self, n):
        for _ in range(n):
            self.asteroids.append(Asteroid())

    def update(self, dt, keys):
        self.player.update(dt, keys)
        for a in self.asteroids:
            a.update(dt)

        for b in list(self.bullets):
            b.update(dt)
            if b.life <= 0:
                try:
                    self.bullets.remove(b)
                except ValueError:
                    pass

        for eb in list(self.enemy_bullets):
            eb.update(dt)
            if eb.life <= 0:
                try:
                    self.enemy_bullets.remove(eb)
                except ValueError:
                    pass

        # spawn small enemies if none
        if len(self.enemies_small) < 2 and random.random() < 0.01:
            side_x = random.choice([0, C.WIDTH])
            side_y = random.randint(0, C.HEIGHT)
            self.enemies_small.append(EnemySmall(side_x, side_y))

        # maybe spawn a big enemy occasionally
        if self.enemy_big is None and random.random() < 0.002:
            self.enemy_big = EnemyBig()

        for e in list(self.enemies_small):
            e.update(dt, self.player, self)

        if self.enemy_big:
            self.enemy_big.update(dt, self)

        self.handle_collisions()

    def handle_collisions(self):
        # bullets hitting asteroids
        for b in list(self.bullets):
            for a in list(self.asteroids):
                if a.collides(b.x, b.y):
                    try:
                        self.bullets.remove(b)
                    except ValueError:
                        pass
                    try:
                        self.asteroids.remove(a)
                    except ValueError:
                        pass
                    self.audio.play("explosion")
                    break

        # enemy bullets hitting player
        for eb in list(self.enemy_bullets):
            if (self.player.x - eb.x)**2 + (self.player.y - eb.y)**2 < 15**2:
                try:
                    self.enemy_bullets.remove(eb)
                except ValueError:
                    pass
                self.audio.play("explosion")
                self.player.random_position()
                break

        # enemies destroyed by asteroids
        for e in list(self.enemies_small):
            for a in list(self.asteroids):
                if a.collides(e.x, e.y):
                    try:
                        self.enemies_small.remove(e)
                    except ValueError:
                        pass
                    self.audio.play("explosion")
                    break

        if self.enemy_big:
            for a in list(self.asteroids):
                if a.collides(self.enemy_big.x, self.enemy_big.y):
                    self.enemy_big = None
                    self.audio.play("explosion")
                    break

    def draw(self, screen, font):
        self.player.draw(screen)
        for a in self.asteroids:
            a.draw(screen)
        for b in self.bullets:
            b.draw(screen)
        for eb in self.enemy_bullets:
            eb.draw(screen)
        for e in self.enemies_small:
            e.draw(screen)
        if self.enemy_big:
            self.enemy_big.draw(screen)
