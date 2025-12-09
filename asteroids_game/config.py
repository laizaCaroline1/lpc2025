# config.py

# CONFIGURAÇÕES DO PYGAME / TELA
WIDTH = 800
HEIGHT = 600
TITLE = "Asteroides Pygame"
FPS = 60

# CONFIGURAÇÕES DE CORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# CONSTANTES DA NAVE (SHIP)
SHIP_RADIUS = 15 
SHIP_THRUST = 150.0 

SHIP_SPEED_MAX = 300.0  # Velocidade máxima
SHIP_TURN_SPEED = 200.0 # Velocidade de rotação (ajustado de ROT_SPEED para TURN_SPEED)
SHIP_FRICTION = 0.99 # Fator de atrito (ajustado de RATE para FRICTION)

SHIP_INVULNERABILITY_TIME = 3.0 # Tempo de invulnerabilidade

# CONSTANTES DE ASTEROIDES E BALAS
BULLET_SPEED = 400
BULLET_LIFETIME = 1.5 # Tempo de vida da bala em segundos (adicionado para a classe Bullet)
ASTEROID_ROTATION_SPEED = 50 # Velocidade de rotação em graus/s
ASTEROID_BASE_RADIUS = 32 

ASTEROID_MIN_RADIUS = 10 

ASTEROID_ANIMATION_SPEED = 0.1
ASTEROID_FRAME_COUNT = 4 

# CONSTANTES DE ANIMAÇÃO/FRAMES
SHIP_ANIMATION_SPEED = 0.05 
SHIP_FRAME_COUNT = 9 

UFO_FRAME_COUNT = 1 

# UFO (Tamanhos e pontuações)
UFO_SMALL = {"r": 20, "score": 200, "aim": 2.5}
UFO_BIG = {"r": 30, "score": 100, "aim": 3.0}