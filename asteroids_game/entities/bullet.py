import pygame as pg
import config as C
from utils import Vec

# CONSTANTES DA BALA
BULLET_RADIUS = 2  # Raio visual da bala (2 pixels é um bom ponto)
BULLET_LIFETIME = 1.0 # Tempo de vida da bala em segundos

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, angle: float, vx: float, vy: float, owner):
        """
        Inicializa a bala.
        Args:
            pos (Vec): Posição inicial (centro).
            angle (float): Ângulo (não usado diretamente, mas bom para registro).
            vx (float): Componente X da velocidade.
            vy (float): Componente Y da velocidade.
            owner (Sprite): O objeto que disparou (Player ou UFO).
        """
        super().__init__()
        
        # Atributos de Jogo
        self.pos = pos.copy()
        self.vel = Vec(vx, vy) 
        self.angle = angle
        self.owner = owner
        self.radius = BULLET_RADIUS
        self.lifetime = BULLET_LIFETIME
        
        # Atributos de Pygame (Imagem e Rect)
        # Cria a imagem procedural da bala (círculo branco)
        self.image = self._create_procedural_image(self.radius)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _create_procedural_image(self, r: int) -> pg.Surface:
        """Cria a imagem da bala como um pequeno círculo branco."""
        # O diâmetro (tamanho da superfície) é o raio * 2 + 2 de margem
        size = r * 2 + 2
        img = pg.Surface((size, size), pg.SRCALPHA)
        
        # Desenha o círculo branco no centro
        pg.draw.circle(img, C.WHITE, (size // 2, size // 2), r, 0)
        
        return img

    def update(self, dt: float):
        """Atualiza a posição e o tempo de vida da bala."""
        
        # 1. Movimento:
        self.pos += self.vel * dt
        
        # 2. Atualiza o Rect:
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # 3. Wrapping (teletransporte)
        # Se a bala sair da tela, ela reaparece no lado oposto
        if self.pos.x < 0:
            self.pos.x += C.WIDTH
        if self.pos.x > C.WIDTH:
            self.pos.x -= C.WIDTH
        if self.pos.y < 0:
            self.pos.y += C.HEIGHT
        if self.pos.y > C.HEIGHT:
            self.pos.y -= C.HEIGHT
            
        # 4. Tempo de Vida (Remoção Automática):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill() 