import pygame as pg
import math
import random
from utils import Vec
import config as C 

# FUNÇÃO AUXILIAR PARA CARREGAR FRAMES 
def load_frames(prefix, count, size):
    """Carrega frames de imagem do disco, retornando [] em caso de falha."""
    frames = []
    for i in range(1, count + 1):
        path = f"entities/{prefix}/{prefix}_{i}.png"
        try:
            frame = pg.image.load(path).convert_alpha()
            frame = pg.transform.scale(frame, (int(size), int(size)))
            frames.append(frame)
        except (pg.error, FileNotFoundError):
            print(f"AVISO: Imagem não encontrada em '{path}'.")
            return [] 
    return frames

# CLASSE ASTEROID 
class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, r, all_asteroid_frames):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.r = r
        self.angle = random.uniform(0, 360)
        
        self.is_splittable = self.r > C.ASTEROID_MIN_RADIUS 
        
        self.frames = all_asteroid_frames
        self.frame_index = random.randint(0, len(self.frames) - 1) if self.frames else 0
        self.anim_timer = 0.0

        # Garante que o tamanho da Surface é um inteiro
        size = int(self.r * 2)

        if self.frames:
            try:
                self.original_image = pg.transform.scale(self.frames[self.frame_index], (size, size))
            except TypeError:
                self.original_image = self._create_procedural_image()
        else:
            self.original_image = self._create_procedural_image()
            
        self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        
    def _create_procedural_image(self):
        size = int(self.r * 2)
        img = pg.Surface((size, size), pg.SRCALPHA)
        center_x = int(self.r)
        center_y = int(self.r)
        radius = int(self.r)
        pg.draw.circle(img, C.WHITE, (center_x, center_y), radius, 2)
        print("AVISO: Usando imagem procedural de asteróide.")
        return img
        
    def split(self, game):
        self.kill() 

        if self.is_splittable:
            new_r = self.r - C.ASTEROID_MIN_RADIUS 
            
            if new_r >= C.ASTEROID_MIN_RADIUS: 
                
                base_speed = self.vel.length() * 1.5

                angle1 = math.radians(self.vel.angle() + 45) 
                vx1 = math.cos(angle1) * base_speed
                vy1 = math.sin(angle1) * base_speed
                
                new_asteroid1 = Asteroid(self.pos, Vec(vx1, vy1), new_r, self.frames)
                game.all_sprites.add(new_asteroid1)
                game.asteroids.add(new_asteroid1)

                angle2 = math.radians(self.vel.angle() - 45) 
                vx2 = math.cos(angle2) * base_speed
                vy2 = math.sin(angle2) * base_speed
                
                new_asteroid2 = Asteroid(self.pos, Vec(vx2, vy2), new_r, self.frames)
                game.all_sprites.add(new_asteroid2)
                game.asteroids.add(new_asteroid2)
        
    def update(self, dt):
        current_image = self.original_image 
        if self.frames:
            # Lógica de animação
            self.anim_timer += dt
            if self.anim_timer >= C.ASTEROID_ANIMATION_SPEED:
                self.anim_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            
            current_frame = self.frames[self.frame_index]
            size = int(self.r * 2)
            current_image = pg.transform.scale(current_frame, (size, size))
        
        # Rotação
        self.angle += C.ASTEROID_ROTATION_SPEED * dt
        self.image = pg.transform.rotate(current_image, self.angle) 
        
        # Movimento
        self.pos += self.vel * dt
        
        # Screen wrap
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        
        # Atualiza o rect, sempre convertendo Vec para tupla de INTs
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))