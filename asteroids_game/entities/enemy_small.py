import pygame as pg
import math
import random
import config as C
# Importações necessárias para a estrutura do seu projeto
from utils import Vec 
from entities.bullet import Bullet 

# ===============================================
# FUNÇÃO AUXILIAR PARA CRIAR O SPRITE PROCEDURAL (Fallback)
# ===============================================
def _create_procedural_image(r: int):
    """Cria a imagem de círculo de UFO procedural para fallback."""
    size = int(r * 2)
    img = pg.Surface((size, size), pg.SRCALPHA)
    center = (r, r)
    
    # Desenha um círculo (UFO) com a cor pequena definida em config (ou verde)
    color = getattr(C, 'UFO_SMALL_COLOR', C.GREEN)
    pg.draw.circle(img, color, center, r, 0)
    
    return img

class EnemySmall(pg.sprite.Sprite): 
    # Use constantes de C se existirem, senão use valores fixos
    SPEED = getattr(C, 'UFO_SMALL_SPEED', 120)
    SHOOT_INTERVAL = getattr(C, 'UFO_SMALL_SHOOT_INTERVAL', 2.0)
    BULLET_SPEED = 250
    
    # CORREÇÃO CRÍTICA 1: Deve herdar de pg.sprite.Sprite
    def __init__(self, pos: Vec, vel: Vec, r: int, frames: list):
        # CORREÇÃO CRÍTICA 2: Deve aceitar 4 argumentos posicionais (além de self)
        super().__init__()
        
        # Propriedades de Posição e Movimento (usando Vec)
        self.pos = Vec(pos) 
        self.vel = Vec(vel) 
        self.r = r
        self.shoot_timer = 0.0 # Renomeado para evitar conflito com self.timer
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
        """Atualiza o movimento e o tiro do UFO Small."""
        
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
            
            # Cálculo da direção (do UFO ao Player)
            # O UFO Small deve mirar diretamente no player
            target_pos = player.pos - self.pos
            
            # Calcula o ângulo em radianos
            ang = math.atan2(target_pos.y, target_pos.x)
            
            # Componentes de velocidade
            vx = math.cos(ang) * self.BULLET_SPEED
            vy = math.sin(ang) * self.BULLET_SPEED
            
            # O UFO Small atira em linha reta.
            # NOTA: O Bullets precisa ser corrigido para aceitar Vec, ang, vx, vy, tipo_atirador
            # Presumindo que 'world' é a instância do Game:
            # world.bullets.add(Bullet(self.pos.copy(), ang, vx, vy, self))
            
            # Chamada original simplificada (ajustada para Vec)
            new_bullet = Bullet(self.pos.copy(), ang, vx, vy, self)
            world.all_sprites.add(new_bullet) # Adiciona ao grupo global
            world.bullets.add(new_bullet)    # Adiciona ao grupo de balas (para colisão)
            
            # Toca o som de tiro (se disponível)
            if world.sounds.get("enemy_shoot"):
                world.sounds["enemy_shoot"].play()

    def draw(self, screen):
        """O método draw é geralmente manipulado por self.all_sprites.draw(screen) no game.py,
        mas o Pygame precisa de self.image e self.rect.
        """
        # (O método draw não precisa ser implementado aqui se o self.all_sprites.draw() for usado)
        pass