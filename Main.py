import pygame
import sys
from music import MusicPlayer  # Asegúrate de que el archivo se llame `music_player.py`

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
YELLOW = (255, 255, 0)  # Color para el borde del carro seleccionado

# Inicializar el reproductor de música
music_player = MusicPlayer()

# Clase para los carros
class Car(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # 'horizontal' o 'vertical'

    def move(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

# Crear carros
red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
green_cars = [
    Car(GREEN, 60, 120, 100, 100, 'vertical'),
    Car(GREEN, 120, 60, 300, 100, 'horizontal'),
    Car(GREEN, 120, 60, 300, 500, 'horizontal'),
    Car(GREEN, 60, 120, 350, 300, 'vertical'),
    Car(GREEN, 60, 120, 500, 250, 'vertical'),
]

# Crear la salida
exit_rect = pygame.Rect(740, 300, 65, 60)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(red_car)
all_sprites.add(*green_cars)

# carro seleccionado
selected_car = red_car


# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Seleccionar un carro
            pos = pygame.mouse.get_pos()
            for car in all_sprites:
                if car.rect.collidepoint(pos):
                    selected_car = car
                    break

    # Movimiento del carro seleccionado y volumen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP2]: #Bajar volumen
        music_player.vol_Down()
    if keys[pygame.K_KP8]: #Subir volumen
        music_player.vol_Up()
    if keys[pygame.K_KP5]: #Mutear y desmutear volumen
        music_player.muteORdemue()

    if selected_car:
        x_change = 0
        y_change = 0
        if selected_car.direction == 'horizontal':
            if keys[pygame.K_LEFT]:
                x_change = -1
            if keys[pygame.K_RIGHT]:
                x_change = 1
        elif selected_car.direction == 'vertical':
            if keys[pygame.K_UP]:
                y_change = -1
            if keys[pygame.K_DOWN]:
                y_change = 1

        # Mover el carro y verificar colisiones
        if x_change != 0 or y_change != 0:
            selected_car.move(x_change, y_change)
            collision = pygame.sprite.spritecollideany(selected_car, all_sprites, collided=lambda x, y: x != y and pygame.sprite.collide_rect(x, y))
            if collision:
                selected_car.move(-x_change, -y_change)

    # Comprobar si el carro rojo está en la salida
    if red_car.rect.colliderect(exit_rect):
        print("¡Has llegado a la salida!")
        running = False

    # Asegurar que los carros no salgan de la pantalla
    for car in all_sprites:
        if car.rect.left < 0:
            car.rect.left = 0
        if car.rect.right > 800:
            car.rect.right = 800
        if car.rect.top < 0:
            car.rect.top = 0
        if car.rect.bottom > 600:
            car.rect.bottom = 600

    # Dibujar todo
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, exit_rect)  # Dibujar la salida
    all_sprites.draw(screen)

    # Dibujar un borde alrededor del carro seleccionado
    if selected_car:
        pygame.draw.rect(screen, YELLOW, selected_car.rect, 3)

    pygame.display.flip()

pygame.quit()
sys.exit()
