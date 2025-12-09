import pygame as pg
import config as C
import math 
from entities.player import Player as Ship 
from entities.asteroid import Asteroid 
# Presumindo que Bullet, EnemyBig, EnemySmall, Vec e sys/random estão corretos
from entities.bullet import Bullet
from entities.enemy_big import EnemyBig
from entities.enemy_small import EnemySmall 
from utils import Vec
import random
import sys


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption(C.TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        # Variáveis de Jogo
        self.dt = 0.0
        
        # 2. CARREGAMENTO DE ATIVOS
        self.load_background()
        self.load_sounds()
        
        # O frame do asteroide é carregado aqui
        self.asteroid_frames = self.load_all_asteroid_frames()
        self.ship_frames = self.load_all_ship_frames() 
        self.ufo_frames = self.load_all_ufo_frames() 

        # Grupos de Sprites
        # ATENÇÃO: self.ufos NÃO DEVE ser atualizado via self.all_sprites.update()
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group() # Este grupo será atualizado separadamente

        # Inicializa a Nave
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2), self.ship_frames) 
        self.all_sprites.add(self.ship)
        
        # Geração inicial de asteroides
        self.check_asteroid_spawn()
        
        # Variáveis de Controle de Spawn
        self.ufo_spawn_timer = 5.0 

    # ===============================================
    # FUNÇÕES DE CARREGAMENTO
    # ===============================================
    def load_background(self):
        """IGNORA a imagem de fundo e cria uma superfície preta sólida."""
        print("Fundo definido como preto sólido (C.BLACK).")
        self.background = pg.Surface((C.WIDTH, C.HEIGHT))
        self.background.fill(C.BLACK)

    def load_sounds(self):
        """Carrega todos os efeitos sonoros, usando o caminho 'entities/'."""
        sound_paths = {
            "laser": "entities/laser.wav",
            "explosion": "entities/explosion.wav",
            "enemy_shoot": "entities/enemy_shoot.wav"
        }
        self.sounds = {}
        for name, path in sound_paths.items():
            try:
                self.sounds[name] = pg.mixer.Sound(path)
            except pg.error as e:
                # Trata a falha de carregamento de forma limpa
                print(f"AVISO: Som '{path}' não encontrado. Erro: {e}")
                self.sounds[name] = None
                
    def load_all_asteroid_frames(self):
        """Carrega e redimensiona os frames do meteoro."""
        frames = []
        target_size = C.ASTEROID_BASE_RADIUS * 2
        
        for i in range(1, C.ASTEROID_FRAME_COUNT + 1):
            path = f"entities/asteroid/asteroid_{i}.png" 
            try:
                frame = pg.image.load(path).convert_alpha()
                resized_frame = pg.transform.scale(frame, (int(target_size), int(target_size)))
                frames.append(resized_frame) 
            except (pg.error, FileNotFoundError) as e:
                print(f"ERRO: Frame '{path}' não encontrado. {e}")
                return [] 
        return frames

    def load_all_ship_frames(self):
        """Carrega os frames da nave (se houver animação)."""
        frames = []
        target_size = C.SHIP_RADIUS * 2
        
        for i in range(1, C.SHIP_FRAME_COUNT + 1):
            path = f"entities/ship/ship_{i}.png" 
            try:
                frame = pg.image.load(path).convert_alpha()
                resized_frame = pg.transform.scale(frame, (int(target_size), int(target_size)))
                frames.append(resized_frame)
            except (pg.error, FileNotFoundError):
                return [] 
        return frames
    
    def load_all_ufo_frames(self):
        """Carrega os frames do UFO."""
        frames = []
        # Garante que C.UFO_BIG existe e tem 'r'
        ufo_r = C.UFO_BIG["r"] if hasattr(C, 'UFO_BIG') and isinstance(C.UFO_BIG, dict) and 'r' in C.UFO_BIG else 30
        target_size = ufo_r * 2 
        
        for i in range(1, C.UFO_FRAME_COUNT + 1):
            path = f"entities/ufo/ufo_{i}.png" 
            try:
                frame = pg.image.load(path).convert_alpha()
                resized_frame = pg.transform.scale(frame, (int(target_size), int(target_size)))
                frames.append(resized_frame)
            except (pg.error, FileNotFoundError):
                print(f"AVISO: Frame do UFO em '{path}' não encontrado.")
                return []
        return frames

    # ===============================================
    # FUNÇÕES DE LÓGICA DE JOGO
    # ===============================================
    def spawn_asteroid(self, size_key: int):
        """Cria um asteroide de tamanho 'size_key' numa borda aleatória."""
        
        # Define o raio (r) com base na chave de tamanho (3, 2 ou 1)
        r = C.ASTEROID_BASE_RADIUS
        if size_key == 3: r = 30 # Grande
        elif size_key == 2: r = 20 # Médio
        elif size_key == 1: r = 10 # Pequeno
        
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = Vec(random.randint(0, C.WIDTH), -r)
            vel = Vec(random.uniform(-50, 50), random.uniform(50, 150))
        elif side == "bottom":
            pos = Vec(random.randint(0, C.WIDTH), C.HEIGHT + r)
            vel = Vec(random.uniform(-50, 50), random.uniform(-150, -50))
        elif side == "left":
            pos = Vec(-r, random.randint(0, C.HEIGHT))
            vel = Vec(random.uniform(50, 150), random.uniform(-50, 50))
        elif side == "right":
            pos = Vec(C.WIDTH + r, random.randint(0, C.HEIGHT))
            vel = Vec(random.uniform(-150, -50), random.uniform(-50, 50))
        else: 
            pos = Vec(random.randint(0, C.WIDTH), random.randint(0, C.HEIGHT))
            vel = Vec(random.uniform(-50, 50), random.uniform(-50, 50))
        
        new_asteroid = Asteroid(pos, vel, r, self.asteroid_frames) 
        self.all_sprites.add(new_asteroid)
        self.asteroids.add(new_asteroid)

    def spawn_ufo(self):
        """Gera um UFO pequeno ou grande em uma borda aleatória."""
        if not self.ufo_frames:
            return 
            
        is_big = random.choice([True, False])
        ufo_data = C.UFO_BIG if is_big else C.UFO_SMALL
        r = ufo_data["r"]
        
        pos_x = C.WIDTH + r if random.choice([True, False]) else -r
        pos = Vec(pos_x, random.randint(0, C.HEIGHT))
        
        vel_x = random.uniform(-50, -20) if pos_x > 0 else random.uniform(20, 50)
        vel = Vec(vel_x, 0)
        
        # O EnemySmall precisa de uma correção similar à do Player (Vec, frames, r)
        if is_big:
             new_ufo = EnemyBig(pos, vel, r, self.ufo_frames)
        else:
             new_ufo = EnemySmall(pos, vel, r, self.ufo_frames)

        self.all_sprites.add(new_ufo) # Mantemos aqui para a função draw()
        self.ufos.add(new_ufo) # Grupo específico para update complexo

    def handle_input(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            self.ship.thrust() 

        self.ship.control(keys, self.dt)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.ship.shot_cool <= 0:
                    self.shoot()

    def shoot(self):
        """Calcula as componentes de velocidade e cria uma nova bala."""
        rad_angle = math.radians(self.ship.angle)
        
        vx = math.cos(rad_angle) * C.BULLET_SPEED + self.ship.vel.x
        vy = math.sin(rad_angle) * C.BULLET_SPEED + self.ship.vel.y
        
        new_bullet = Bullet(self.ship.pos.copy(), self.ship.angle, vx, vy, self.ship) # Copia pos para evitar referência
        
        self.all_sprites.add(new_bullet)
        self.bullets.add(new_bullet)
        self.ship.shot_cool = 0.2 
        if self.sounds.get("laser"):
            self.sounds["laser"].play()

    def check_asteroid_spawn(self):
        """Verifica se não há asteroides e gera um novo conjunto."""
        if not self.asteroids:
            print("Campo limpo! Gerando nova onda de asteroides grandes.")
            for _ in range(4):
                self.spawn_asteroid(3)

    def update(self):
        # 1. ATUALIZAÇÃO DE SPRITES

        # Atualiza a Nave e todos os sprites que não são UFOs e só precisam de dt
        # Criamos um grupo temporário que exclui os UFOs para evitar o TypeError
        sprites_dt_only = pg.sprite.Group(s for s in self.all_sprites if s not in self.ufos)
        sprites_dt_only.update(self.dt)

        # Atualiza UFOs (EnemySmall/EnemyBig) que exigem (dt, player, world)
        # CORREÇÃO: Chama o update manualmente, passando o player (self.ship) e o world (self)
        for ufo in self.ufos:
            ufo.update(self.dt, self.ship, self) 

        # Atualiza o temporizador do UFO e tenta gerar um
        self.ufo_spawn_timer -= self.dt
        if self.ufo_spawn_timer <= 0:
            self.spawn_ufo() 
            self.ufo_spawn_timer = random.uniform(10.0, 20.0) 
        
        # 2. Lógica de Colisão - Asteroides vs. Balas
        hits = pg.sprite.groupcollide(self.bullets, self.asteroids, True, False)

        for bullet, hit_asteroids in hits.items():
            for asteroid in hit_asteroids:
                asteroid.split(self) 
                
        # 3. Verifica e gera nova onda de asteroides se o campo estiver limpo.
        self.check_asteroid_spawn()

        # 4. Lógica de Colisão - Nave vs. Asteroides
        if self.ship.invuln <= 0:
            ship_hits = pg.sprite.spritecollide(self.ship, self.asteroids, False, pg.sprite.collide_circle)
            if ship_hits:
                print("Nave atingida! Perdeu vida.")
                self.ship.invuln = C.SHIP_INVULNERABILITY_TIME
                # TODO: Implementar lógica de reset/perda de vida da nave aqui.
        
        # TODO: Lógica de Colisão - Nave vs. UFOs
        # TODO: Lógica de Colisão - Nave vs. Balas Inimigas (EnemyBullets)
        
    def draw(self):
        """Desenha todos os elementos na tela."""
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            self.dt = self.clock.tick(C.FPS) / 1000.0
            self.handle_input()
            self.update()
            self.draw()

        pg.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()