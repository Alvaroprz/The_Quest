
import pygame
import sys
import random
from database import init_db, save_score, get_top_scores

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIP_SPEED = 5
OBSTACLE_SPEEDS = [4, 5, 6, 7, 8]
LEVEL_DURATION = 30  # segundos por nivel
TOTAL_LEVELS = 5

# Cargar imágenes
ship_img = pygame.image.load("assets/ship.png")
obstacle_img = pygame.image.load("assets/obstacle.png")
planet_img = pygame.image.load("assets/planet.png")
background_img = pygame.image.load("assets/background.png")

# Escalar imágenes
ship_img = pygame.transform.scale(ship_img, (60, 40))
obstacle_img = pygame.transform.scale(obstacle_img, (60, 60))
planet_img = pygame.transform.scale(planet_img, (100, 100))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Quest")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Clases
class Ship:
    def __init__(self):
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.centery = HEIGHT // 2
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= SHIP_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += SHIP_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

class Obstacle:
    def __init__(self, speed):
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

def show_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def show_start_screen():
    screen.blit(background_img, (0, 0))
    show_text("THE QUEST", WIDTH // 2 - 80, HEIGHT // 2 - 40)
    show_text("Pulsa cualquier tecla para empezar", WIDTH // 2 - 180, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(score):
    initials = input("Introduce tus iniciales (3 letras): ")[:3].upper()
    save_score(initials, score)
    top_scores = get_top_scores()
    screen.fill(BLACK)
    show_text("GAME OVER", WIDTH // 2 - 80, 50)
    show_text(f"Puntuación: {score}", WIDTH // 2 - 80, 100)
    show_text("Top 5 puntuaciones:", WIDTH // 2 - 100, 160)
    for i, (ini, sc) in enumerate(top_scores):
        show_text(f"{i+1}. {ini} - {sc}", WIDTH // 2 - 80, 200 + i*30)
    show_text("Pulsa cualquier tecla para salir", WIDTH // 2 - 150, 400)
    pygame.display.flip()
    wait_for_key()
    pygame.quit()
    sys.exit()

def main():
    init_db()
    show_start_screen()
    ship = Ship()
    score = 0

    for level in range(1, TOTAL_LEVELS + 1):
        obstacles = []
        timer = 0
        level_start = pygame.time.get_ticks()
        speed = OBSTACLE_SPEEDS[min(level - 1, len(OBSTACLE_SPEEDS) - 1)]

        while True:
            clock.tick(FPS)
            elapsed_time = (pygame.time.get_ticks() - level_start) / 1000
            if elapsed_time > LEVEL_DURATION:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            ship.move(keys)

            # Añadir nuevos obstáculos
            timer += 1
            if timer > 40:
                obstacles.append(Obstacle(speed))
                timer = 0

            # Actualizar obstáculos
            for ob in obstacles:
                ob.update()

            # Eliminar obstáculos que ya salieron de la pantalla
            obstacles = [ob for ob in obstacles if ob.rect.right > 0]

            # Colisiones
            for ob in obstacles[:]:
                if ob.rect.colliderect(ship.rect):
                    ship.lives -= 1
                    obstacles.remove(ob)
                    if ship.lives <= 0:
                        show_game_over_screen(score)

            # 🔄 LIMPIAR pantalla
            screen.blit(background_img, (0, 0))

            # 🔄 DIBUJAR elementos
            ship.draw()
            for ob in obstacles:
                ob.draw()

            score += 1
            show_text(f"Puntuación: {score}", 10, 10)
            show_text(f"Vidas: {ship.lives}", 10, 40)

            pygame.display.flip()


    # Final
    screen.blit(background_img, (0, 0))
    screen.blit(planet_img, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
    show_text("Has llegado al planeta", WIDTH // 2 - 100, HEIGHT // 2 + 70)
    pygame.display.flip()
    pygame.time.delay(3000)
    show_game_over_screen(score)

if __name__ == "__main__":
    main()
