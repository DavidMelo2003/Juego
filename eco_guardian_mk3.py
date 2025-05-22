import pygame
import random
import os

# Inicializar Pygame
pygame.init()
pygame.mixer.init() # Inicializar el mezclador de sonido

# --- Constantes ---
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Configuración de pantalla ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco-Guardián Espacial MK.II")

# --- Cargar Assets ---
def load_image(filename, alpha=True):
    """Carga una imagen y la convierte (con o sin canal alfa)."""
    path = os.path.join(assets_path, 'images', filename)
    try:
        image = pygame.image.load(path)
        if alpha:
            return image.convert_alpha()
        else:
            return image.convert()
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {filename} - {e}")
        # Devuelve una superficie de marcador de posición si la imagen no se carga
        surface = pygame.Surface((50, 50))
        surface.fill(RED)
        return surface

def load_sound(filename):
    """Carga un sonido."""
    path = os.path.join(assets_path, 'sounds', filename)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"No se pudo cargar el sonido: {filename} - {e}")
        return None # O un sonido de marcador de posición si lo deseas

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# Imágenes (Asegúrate de tener estas imágenes en tu carpeta assets/images)
player_img = load_image('player.png')
enemy_imgs = [
    load_image('enemy1.png'),
    load_image('enemy2.png'),
    load_image('enemy3.png')
]
bullet_img = load_image('bullet.png')
enemy_bullet_img = load_image('enemy_bullet.png') # Necesitarás esta imagen
powerup_rapidfire_img = load_image('powerup_rapidfire.png') # Y esta
background_img = load_image('background.jpg', alpha=False)
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT)) # Escalar fondo

# Sonidos (Asegúrate de tener estos sonidos en tu carpeta assets/sounds)
laser_sound = load_sound('laser.mp3')
explosion_sound = load_sound('explosion.mp3')
player_hit_sound = load_sound('player_hit.mp3') # Sonido para cuando el jugador es golpeado
powerup_sound = load_sound('powerup.mp3') # Sonido para recoger power-up

# --- Clases ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_img
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 7
        self.lives = 3
        self.score = 0
        self.shoot_delay = 250 # Milisegundos entre disparos
        self.last_shot_time = pygame.time.get_ticks()
        self.is_rapid_fire = False
        self.rapid_fire_end_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        # Manejar fin de rapid fire
        if self.is_rapid_fire and pygame.time.get_ticks() > self.rapid_fire_end_time:
            self.is_rapid_fire = False
            self.shoot_delay = 250 # Volver al delay normal

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            bullet = Bullet(self.rect.centerx, self.rect.top, -12, bullet_img)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            if laser_sound: laser_sound.play()

    def activate_rapid_fire(self, duration=5000): # 5 segundos
        self.is_rapid_fire = True
        self.shoot_delay = 100 # Delay más corto
        self.rapid_fire_end_time = pygame.time.get_ticks() + duration
        if powerup_sound: powerup_sound.play()

    def hit(self):
        self.lives -= 1
        if player_hit_sound: player_hit_sound.play()
        if self.lives <= 0:
            return True # Game Over
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type_idx, speed_multiplier=1.0):
        super().__init__()
        self.image = enemy_imgs[type_idx % len(enemy_imgs)] # Usar módulo por si type_idx es muy grande
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_speed = random.randint(1, 3)
        self.speed = self.base_speed * speed_multiplier
        self.direction = 1 # 1 para derecha, -1 para izquierda
        self.shoot_chance = 0.002 # Probabilidad de disparar en cada frame (ajustar)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH:
            self.direction = -1
            self.rect.y += 20 # Bajar un poco más
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.y += 20

        # Los enemigos no deben bajar infinitamente
        if self.rect.top > HEIGHT:
            self.kill() # Si se salen por abajo, desaparecen (o pierdes una vida)

        # Disparo enemigo
        if random.random() < self.shoot_chance:
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 6, enemy_bullet_img) # Disparan hacia abajo
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        # Podrías añadir un sonido de disparo enemigo aquí

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y # Usar centery para que salga del centro de la nave
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.type = "rapid_fire" # Por ahora solo un tipo
        self.image = powerup_rapidfire_img
        self.rect = self.image.get_rect()
        self.rect.center = center_pos
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# --- Grupos de Sprites ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# --- Funciones del Juego ---
def spawn_enemy_wave(wave_number):
    num_enemies_per_row = 8
    num_rows = min(3 + wave_number // 2, 5) # Aumentar filas con las olas, máximo 5
    enemy_spacing_x = 70
    enemy_spacing_y = 60
    start_x = (WIDTH - (num_enemies_per_row * enemy_spacing_x)) // 2 + 30
    start_y = 50
    speed_multiplier = 1.0 + (wave_number * 0.1) # Enemigos más rápidos cada ola

    for row in range(num_rows):
        for column in range(num_enemies_per_row):
            enemy_type = random.randint(0, len(enemy_imgs) - 1) # Variedad de enemigos
            x = start_x + column * enemy_spacing_x
            y = start_y + row * enemy_spacing_y
            enemy = Enemy(x, y, enemy_type, speed_multiplier)
            all_sprites.add(enemy)
            enemies.add(enemy)

def spawn_powerup(position):
    powerup = PowerUp(position)
    all_sprites.add(powerup)
    powerups.add(powerup)

def draw_text(surface, text, size, x, y, color=WHITE, font_name=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_game_screen(screen_type="start"):
    screen.blit(background_img, (0,0)) # Fondo para las pantallas
    if screen_type == "start":
        draw_text(screen, "Eco-Guardián Espacial MK.II", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Flechas para mover, Espacio para disparar", 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Pulsa cualquier tecla para empezar", 18, WIDTH / 2, HEIGHT * 3 / 4)
    elif screen_type == "game_over":
        draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, f"Puntuación Final: {player.score}", 30, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Pulsa 'R' para reintentar o 'Q' para salir", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if screen_type == "start":
                if event.type == pygame.KEYUP:
                    waiting = False
            elif screen_type == "game_over":
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        return True # Reintentar
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
    return False # No reintentar (solo para game_over si no es R)

# --- Inicialización del Juego ---
player = Player()
clock = pygame.time.Clock()
current_wave = 0
game_over = False
show_start_screen = True
background_y1 = 0
background_y2 = -HEIGHT # Para el scroll

# --- Bucle Principal del Juego ---
running = True
while running:
    if show_start_screen:
        show_game_screen("start")
        show_start_screen = False
        # Reiniciar el juego para una nueva partida
        all_sprites.empty()
        enemies.empty()
        player_bullets.empty()
        enemy_bullets.empty()
        powerups.empty()

        player = Player() # Crear nuevo jugador
        all_sprites.add(player)
        current_wave = 0
        spawn_enemy_wave(current_wave)
        game_over = False
        background_y1 = 0
        background_y2 = -HEIGHT

    if game_over:
        if show_game_screen("game_over"): # Si devuelve True, es para reintentar
            show_start_screen = True # Volverá a mostrar la pantalla de inicio y reiniciará
            game_over = False # Para que no entre aquí de nuevo inmediatamente
        else: # Si no se reintenta (salió por Q o cerró ventana)
            running = False
        continue # Saltar el resto del bucle de juego

    # --- Manejo de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE: # Salir con ESC
                 running = False


    # --- Actualizar Sprites ---
    all_sprites.update()

    # --- Colisiones ---
    # Balas del jugador con enemigos
    enemy_hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    for enemy_hit in enemy_hits:
        if explosion_sound: explosion_sound.play()
        player.score += 100
        # Posibilidad de soltar un power-up
        if random.random() < 0.1: # 10% de probabilidad
            spawn_powerup(enemy_hit.rect.center)

    # Balas enemigas con jugador
    player_hits_by_enemy = pygame.sprite.spritecollide(player, enemy_bullets, True) # True para que la bala desaparezca
    if player_hits_by_enemy:
        if player.hit(): # Si hit() devuelve True, el jugador no tiene más vidas
            game_over = True

    # Jugador con enemigos (colisión directa)
    player_collides_enemy = pygame.sprite.spritecollide(player, enemies, True) # True para que el enemigo desaparezca
    if player_collides_enemy:
        if explosion_sound: explosion_sound.play() # El enemigo explota
        if player.hit():
            game_over = True

    # Jugador con power-ups
    powerup_collected = pygame.sprite.spritecollide(player, powerups, True)
    for pu in powerup_collected:
        if pu.type == "rapid_fire":
            player.activate_rapid_fire()
            # Podrías añadir más tipos aquí
            # elif pu.type == "shield":
            # player.activate_shield()

    # --- Lógica de Oleadas ---
    if not enemies and not game_over: # Si no hay enemigos y el juego no ha terminado
        current_wave += 1
        player.score += 500 # Bonus por completar oleada
        spawn_enemy_wave(current_wave)
        # Pequeña curación entre oleadas si quieres
        # if player.lives < 3: player.lives +=1


    # --- Dibujar / Renderizar ---
    # Scroll del fondo
    background_y1 += 1
    background_y2 += 1
    if background_y1 >= HEIGHT:
        background_y1 = -HEIGHT
    if background_y2 >= HEIGHT:
        background_y2 = -HEIGHT

    screen.blit(background_img, (0, background_y1))
    screen.blit(background_img, (0, background_y2))

    all_sprites.draw(screen)

    # Mostrar UI (Puntuación, Vidas, Oleada)
    draw_text(screen, f"Score: {player.score}", 24, WIDTH / 2, 10)
    draw_text(screen, f"Lives: {player.lives}", 24, 60, 10)
    draw_text(screen, f"Wave: {current_wave + 1}", 24, WIDTH - 60, 10)
    if player.is_rapid_fire:
        time_left = (player.rapid_fire_end_time - pygame.time.get_ticks()) // 1000
        draw_text(screen, f"Rapid Fire: {time_left +1}s", 18, WIDTH / 2, 40, YELLOW)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()