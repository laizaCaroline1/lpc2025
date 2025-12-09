import pygame as pg
import math
import random
import config as C
# Importações necessárias
from utils import Vec 
from entities.bullet import Bullet 

# ===============================================
# FUNÇÃO AUXILIAR PARA CRIAR O SPRITE PROCEDURAL (Fallback)
# (Você pode copiar a mesma função de EnemySmall ou criar uma específica)
# ===============================================
def _create_procedural_image(r: int):
    """Cria a imagem de círculo de UFO procedural para fallback (UFO Grande)."""
    size = int(r * 2)
    img = pg.Surface((size, size), pg.SRCALPHA)
    center = (r, r)
    
    # Desenha um círculo maior ou diferente (UFO)
    color = getattr(C, 'UFO_BIG_COLOR', C.RED) # Usando uma cor diferente
    pg.draw.circle(img, color, center, r, 0)
    
    return img

# CORREÇÃO CRÍTICA 1: Deve herdar de pg.sprite.Sprite
class EnemyBig(pg.sprite.Sprite): 
    # Use constantes de C se existirem, senão use valores fixos
    SPEED = getattr(C, 'UFO_BIG_SPEED', 80)
    SHOOT_INTERVAL = getattr(C, 'UFO_BIG_SHOOT_INTERVAL', 3.5)
    BULLET_SPEED = 200
    
    # CORREÇÃO CRÍTICA 2: O construtor deve aceitar 4 argumentos
    def __init__(self, pos: Vec, vel: Vec, r: int, frames: list):
        super().__init__()
        
        # Propriedades de Posição e Movimento (usando Vec)
        self.pos = Vec(pos) 
        self.vel = Vec(vel) 
        self.r = r
        self.shoot_timer = 0.0
        self.alive = True
        
        # --- Configuração do Sprite ---
        self.frames = frames
        size = int(self.r * 2)

        if self.frames:
            # Pega o primeiro frame e redimensiona
            self.original_image = pg.transform.scale(self.frames[0], (size, size))
        else:
            # Fallback procedural
            self.original_image = _create_procedural_image(self.r)
            
        self.image = self.original_image.copy()
        
        # Inicializa o Rect, usando INTEIROS
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        
    def update(self, dt, player, world):
        """Atualiza o movimento e o tiro do UFO Big."""
        
        # Movimento
        self.pos += self.vel * dt
        
        # Screen wrap
        self.pos.x = self.pos.x % C.WIDTH
        self.pos.y = self.pos.y % C.HEIGHT
        
        # Atualiza a posição do rect
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        # Lógica de Tiro
        self.shoot_timer += dt
        if self.shoot_timer >= self.SHOOT_INTERVAL:
            self.shoot_timer = 0
            
            # O UFO Grande (geralmente) atira aleatoriamente, não mirado.
            random_angle = random.uniform(0, 2 * math.pi)
            
            # Componentes de velocidade
            vx = math.cos(random_angle) * self.BULLET_SPEED
            vy = math.sin(random_angle) * self.BULLET_SPEED
            
            # Presumindo que 'world' é a instância do Game:
            new_bullet = Bullet(self.pos.copy(), random_angle, vx, vy, self)
            world.all_sprites.add(new_bullet) 
            world.bullets.add(new_bullet)
            
            # Toca o som de tiro (se disponível)
            if world.sounds.get("enemy_shoot"):
                world.sounds["enemy_shoot"].play()

    # (Métodos adicionais como draw, kill, etc., devem vir aqui se existirem)