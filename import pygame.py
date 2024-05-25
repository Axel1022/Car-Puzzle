import pygame
import sys
from PIL import Image

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Park Puzzle")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Clase para los autos
class Car(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

# Crear autos
red_car = Car(RED, 120, 60, 200, 300)
green_cars = [
    Car(GREEN, 60, 120, 100, 100),
    Car(GREEN, 120, 60, 300, 100),
    Car(GREEN, 120, 60, 300, 500),
    Car(GREEN, 60, 120, 350, 300),
    Car(GREEN, 60, 120, 500, 250),

]

# Crear la salida
exit_rect = pygame.Rect(740, 300, 65, 60)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(red_car)
all_sprites.add(*green_cars)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for car in green_cars:
                    if car.rect.collidepoint(event.pos):
                        x_change = event.pos[0] - car.rect.centerx
                        y_change = event.pos[1] - car.rect.centery
                        if 0 <= car.rect.x + x_change <= 800 - car.rect.width\
                            and 0 <= car.rect.y + y_change <= 600 - car.rect.height\
                            and not any(car.rect.colliderect(other_car.rect) for other_car in green_cars if other_car != car):
                            car.move(x_change, y_change)


    # Movimiento del auto rojo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        red_car.rect.x -= 1
        if pygame.sprite.spritecollideany(red_car, green_cars):
            red_car.rect.x += 1
    if keys[pygame.K_RIGHT]:
        red_car.rect.x += 1
        if pygame.sprite.spritecollideany(red_car, green_cars):
            red_car.rect.x -= 1
    if keys[pygame.K_UP]:
        red_car.rect.y -= 1
        if pygame.sprite.spritecollideany(red_car, green_cars):
            red_car.rect.y += 1
    if keys[pygame.K_DOWN]:
        red_car.rect.y += 1
        if pygame.sprite.spritecollideany(red_car, green_cars):
            red_car.rect.y -= 1

    # Comprobar si el carro rojo está en la salida
    if red_car.rect.colliderect(exit_rect):
        print("¡Has llegado a la salida!")
        running = False

    # Asegurar que el auto no salga de la pantalla
    if red_car.rect.left < 0:
        red_car.rect.left = 0
    if red_car.rect.right > 800:
        red_car.rect.right = 800
    if red_car.rect.top < 0:
        red_car.rect.top = 0
    if red_car.rect.bottom > 600:
        red_car.rect.bottom = 600

    # Dibujar todo
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, exit_rect)  # Dibujar la salida
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()