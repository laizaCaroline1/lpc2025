import pygame as pg
import math
import random
import config as C
from utils import Vec 

# FUNÇÃO AUXILIAR PARA CRIAR O SPRITE PROCEDURAL
def _create_procedural_image(r: int):
    """Cria a imagem triangular da nave (placeholders)"""
    size = r * 2
    img = pg.Surface((size, size), pg.SRCALPHA)
    center_x = r
    
    points = [
        (size, center_x),  # Ponta direita
        (0, 0),            # Canto superior esquerdo
        (0, size)          # Canto inferior esquerdo
    ]
    
    # Desenha o triângulo (assumindo C.WHITE está em config)
    pg.draw.polygon(img, C.WHITE, points, 0) 
    
    return img

class Player(pg.sprite.Sprite): 
    # Usando constantes do módulo C ou valores internos como fallback
    SPEED_MAX = getattr(C, 'SHIP_MAX_SPEED', 300) 
    FRICTION = getattr(C, 'SHIP_FRICTION', 0.99)
    ROT = getattr(C, 'SHIP_ROTATION_SPEED', 200) 
    
    SHIP_RADIUS = getattr(C, 'SHIP_RADIUS', 15)

    def __init__(self, pos: Vec, frames: list): 
        super().__init__()
        
        # Propriedades de Posição e Movimento
        self.pos = Vec(pos) 
        self.vel = Vec(0, 0) 
        self.angle = -90 
        self.r = self.SHIP_RADIUS
        self.shot_cool = 0.0
        
        # Variável de invulnerabilidade (usada no game.py)
        self.invuln = 0.0 
        
        # Inicialização do Sprite (Image e Rect)
        self.frames = frames
        
        if self.frames:
            # Se houver frames carregados, usa o primeiro e redimensiona
            target_size = self.r * 2
            self.original_image = pg.transform.scale(self.frames[0], (int(target_size), int(target_size)))
        else:
            # Fallback procedural
            self.original_image = _create_procedural_image(self.r)
            
        self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        
    def control(self, keys, dt):
        """Trata a rotação da nave (chamado pelo game.py)"""
        if keys[pg.K_LEFT]:
            self.angle += self.ROT * dt
        if keys[pg.K_RIGHT]:
            self.angle -= self.ROT * dt
        self.angle = self.angle % 360

    def thrust(self):
        """Aplica a propulsão (chamado por K_UP em game.py)"""
        rad_angle = math.radians(self.angle)
        dirv = Vec(math.cos(rad_angle), math.sin(rad_angle)) 
        
        # Aplica uma força constante
        self.vel += dirv * getattr(C, 'SHIP_THRUST', 50) * 0.5 
        
        # Limita a velocidade
        if self.vel.magnitude_sqrd() > self.SPEED_MAX**2:
            self.vel.scale_to_length(self.SPEED_MAX)

    def update(self, dt):
        """Atualiza posição e rotação do sprite"""
        
        # Aplica atrito (exponencial)
        self.vel *= (self.FRICTION ** dt)
        
        # Atualiza a posição
        self.pos += self.vel * dt
        
        # Screen wrap
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT

        self.image = pg.transform.rotate(self.original_image, -self.angle - 90)
        
        # Atualiza o cooldown de tiro
        self.shot_cool = max(0.0, self.shot_cool - dt)
        
        # Atualiza invulnerabilidade
        self.invuln = max(0.0, self.invuln - dt)
        
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))