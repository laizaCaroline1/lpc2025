import pygame as pg
import math
import random
from utils import Vec
import config as C 

# FUNÇÃO AUXILIAR PARA CARREGAR FRAMES (CAMINHO CORRIGIDO)
def load_frames(prefix, count, size):
    """Carrega uma sequência de sprites (ex: 'ship_1.png', 'ship_2.png')"""
    frames = []
    for i in range(1, count + 1):
        path = f"entities/{prefix}/" + (f"{prefix}_{i}.png" if '/' not in prefix else f"{prefix.split('/')[-1]}_{i}.png")
        try:
            frame = pg.image.load(path).convert_alpha()
            frame = pg.transform.scale(frame, (size, size))
            frames.append(frame)
        except (pg.error, FileNotFoundError):
            print(f"AVISO: Frame '{path}' não encontrado. Usando fallback procedural.")
            return [] 
    return frames

# CLASSE SHIP (Player)
class Ship(pg.sprite.Sprite):
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90 
        self.r = C.SHIP_RADIUS
        self.invuln = C.SHIP_INVULNERABILITY_TIME
        self.shot_cool = 0.0
        
        self.frames = load_frames("ship", C.SHIP_FRAME_COUNT, self.r * 2)
        self.original_image = self.frames[0] if self.frames else self._create_procedural_image()
        self.image = self.original_image.copy()
        self.frame_index = 0
        self.anim_timer = 0.0

        self.rect = self.image.get_rect(center=self.pos)
        
    def _create_procedural_image(self):
        size = self.r * 2
        img = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.polygon(img, C.WHITE, [(size, size/2), (0, size), (0, 0)]) 
        print("AVISO: Usando imagem procedural da nave.")
        return img
    
    def control(self, keys, dt):
        if keys[pg.K_LEFT]:
            self.angle += C.SHIP_TURN_SPEED * dt
        if keys[pg.K_RIGHT]:
            self.angle -= C.SHIP_TURN_SPEED * dt
        self.angle = self.angle % 360

    def thrust(self):
        rad_angle = math.radians(self.angle)
        dirv = Vec(math.cos(rad_angle), math.sin(rad_angle))
        self.vel += dirv * C.SHIP_THRUST
        
    def update(self, dt):
        current_frame = self.original_image
        if self.frames:
            self.anim_timer += dt
            if self.anim_timer >= C.SHIP_ANIMATION_SPEED:
                self.anim_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            current_frame = self.frames[self.frame_index]
        
        self.image = pg.transform.rotate(current_frame, -self.angle) 
        
        self.vel *= (C.SHIP_FRICTION ** dt) 
        self.pos += self.vel * dt
        
        self.rect = self.image.get_rect(center=self.pos) 
        self.shot_cool -= dt
        if self.invuln > 0:
            self.invuln -= dt

        # Screen wrap
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        self.rect.center = self.pos

# CLASSE ASTEROID
class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, r, all_asteroid_frames):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.r = r
        self.angle = random.uniform(0, 360)
        
        # Define se este asteroide deve se dividir. O asteroide menor não se divide.
        self.is_splittable = self.r > C.ASTEROID_MIN_RADIUS 
        
        self.frames = all_asteroid_frames
        self.original_image = self.frames[0] if self.frames else self._create_procedural_image()
        self.frame_index = random.randint(0, len(self.frames) - 1) if self.frames else 0
        self.anim_timer = 0.0

        if self.frames:
             self.original_image = pg.transform.scale(self.frames[0], (self.r * 2, self.r * 2))
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def _create_procedural_image(self):
        size = self.r * 2
        img = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(img, C.WHITE, (self.r, self.r), self.r, 2)
        print("AVISO: Usando imagem procedural de asteróide.")
        return img
        
    def split(self, game):
        """
        Método que destrói o asteroide atual e cria dois fragmentos no local.
        """
        # 1. Destrói o asteroide atual
        self.kill() 

        if self.is_splittable:
            new_r = self.r - C.ASTEROID_MIN_RADIUS / 2 
            
            # Garante que não criamos um asteroide menor do que o permitido
            if new_r >= 10: 
                
                # Velocidade base aumenta para simular a quebra
                base_speed = self.vel.length() * 1.5

                # 1. Fragmento 1: Desvio de +45 graus
                angle1 = math.radians(self.vel.angle() + 45) 
                vx1 = math.cos(angle1) * base_speed
                vy1 = math.sin(angle1) * base_speed
                
                # Cria e adiciona o novo asteroide
                new_asteroid1 = Asteroid(self.pos, Vec(vx1, vy1), new_r, self.frames)
                game.all_sprites.add(new_asteroid1)
                game.asteroids.add(new_asteroid1)


                # 2. Fragmento 2: Desvio de -45 graus
                angle2 = math.radians(self.vel.angle() - 45) 
                vx2 = math.cos(angle2) * base_speed
                vy2 = math.sin(angle2) * base_speed
                
                new_asteroid2 = Asteroid(self.pos, Vec(vx2, vy2), new_r, self.frames)
                game.all_sprites.add(new_asteroid2)
                game.asteroids.add(new_asteroid2)
            
    def update(self, dt):
        current_image = self.original_image 
        if self.frames:
            self.anim_timer += dt
            if self.anim_timer >= C.ASTEROID_ANIMATION_SPEED:
                self.anim_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            
            current_frame = self.frames[self.frame_index]
            size = self.r * 2
            current_image = pg.transform.scale(current_frame, (size, size))
        
        self.angle += C.ASTEROID_ROTATION_SPEED * dt
        self.image = pg.transform.rotate(current_image, self.angle) 
        
        self.pos += self.vel * dt
        self.rect = self.image.get_rect(center=self.pos)
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        self.rect.center = self.pos


# CLASSE UFO (EnemyBig / EnemySmall)
class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, r, frames): 
        super().__init__()
        
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.r = r
        self.frames = frames 

        self.score = 500
        self.aim_cooldown = 1.0 
        self.shoot_cool = 0.0
        
        if self.frames:
            self.image = pg.transform.scale(self.frames[0], (self.r * 2, self.r * 2))
        else:
            self.image = self._create_procedural_image()

        self.rect = self.image.get_rect(center=self.pos)

    def _create_procedural_image(self):
        size = int(self.r * 2)
        img = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.ellipse(img, C.WHITE, (0, self.r // 2, size, self.r))
        print("AVISO: Usando imagem procedural do UFO.")
        return img
        
    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        self.rect.center = self.pos
        
# CLASSES ALIAS PARA UFO
EnemyBig = UFO
EnemySmall = UFO

# CLASSE BULLET (PROJÉTIL)
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, angle: float, vx: float, vy: float, owner):
        super().__init__()
        self.r = 3
        self.pos = pos.copy() 
        self.owner = owner
        
        self.vel = Vec(vx, vy)
        self.lifetime = C.BULLET_LIFETIME 
        
        self.image = pg.Surface((self.r * 2, self.r * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, C.WHITE, (self.r, self.r), self.r)
        self.rect = self.image.get_rect(center=self.pos)
        

    def update(self, dt):
        self.pos += self.vel * dt
        
        self.lifetime -= dt
        
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        if self.lifetime <= 0:
            self.kill()