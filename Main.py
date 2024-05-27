import pygame
import pygame_menu
import sys
import time

import pygame_menu.widgets

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
YELLOW = (255, 255, 0)  # Color para el borde del auto seleccionado
GRAY = (128, 128, 128)

red_car = None
green_cars = []

# Clase para los autos
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

def set_dificultad(value,dificultad):
    global red_car,green_cars
    if dificultad == 1:
        # Crear autos
        red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
        green_cars = [
        Car(GREEN, 60, 120, 100, 100, 'vertical'),
        Car(GREEN, 120, 60, 300, 100, 'horizontal'),
        Car(GREEN, 120, 60, 300, 500, 'horizontal'),
        Car(GREEN, 60, 120, 350, 300, 'vertical'),
        Car(GREEN, 60, 120, 500, 250, 'vertical'),
        ]

    if dificultad == 2:
    # Nivel 2:
        red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
        green_cars = [
            Car(GREEN, 60, 120, 200, 40, 'vertical'),
            Car(GREEN, 60, 120, 200, 170, 'vertical'),
            Car(GREEN, 120, 60, 300, 220, 'horizontal'),
            Car(GREEN, 120, 60, 300, 450, 'horizontal'),
            Car(GREEN, 60, 120, 350, 300, 'vertical'),
            Car(GREEN, 60, 120, 500, 250, 'vertical'),
        ]    
    pass



def start_the_game():
    global red_car,green_cars
    # Crear la salida
    exit_rect = pygame.Rect(740, 300, 65, 60)


# Definir las paredes
    walls = [
        pygame.Rect(0, 0, 800, 10),  # Pared superior
        pygame.Rect(0, 10, 10, 600),  # Pared izquierda
        pygame.Rect(0, 590, 800, 10), # Pared inferior
        pygame.Rect(790, 0, 10, 600), # Pared derecha superior
    ]

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(red_car)
    all_sprites.add(*green_cars)

    # Mensaje de victoria:
    font = pygame.font.Font(None,53)
    win_text = font.render("¡Has llegado a la salida!",True,WHITE)
    size = win_text.get_rect(center=(400, 300))

    # Auto seleccionado
    selected_car = red_car

    # Bucle principal
    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Seleccionar un auto
                pos = pygame.mouse.get_pos()
                for car in all_sprites:
                    if car.rect.collidepoint(pos):
                        selected_car = car
                        break

        # Movimiento del auto seleccionado
        keys = pygame.key.get_pressed()
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

            # Mover el auto y verificar colisiones
            if x_change != 0 or y_change != 0:
                selected_car.move(x_change, y_change)
                collision = pygame.sprite.spritecollideany(selected_car, all_sprites, collided=lambda x, y: x != y and pygame.sprite.collide_rect(x, y))
                if collision:
                    selected_car.move(-x_change, -y_change)

        # Comprobar si el carro rojo está en la salida
        if red_car.rect.colliderect(exit_rect):
            screen.blit(win_text, size)
            pygame.display.flip()
            time.sleep(2)
            running = False

        # Asegurar que los autos no salgan de la pantalla
        for car in all_sprites:
            
            if car.rect.left < 10:
                car.rect.left = 10
            if car.rect.right > 790:
                car.rect.right = 790
            if car.rect.top < 10:
                car.rect.top = 10
            if car.rect.bottom > 590:
                car.rect.bottom = 590

        # Dibujar todo
        screen.fill(BLACK)

        for wall in walls:
            pygame.draw.rect(screen, GRAY, wall)  # Dibujar las paredes
        
        pygame.draw.rect(screen, WHITE, exit_rect)  # Dibujar la salida
        all_sprites.draw(screen)

        # Dibujar un borde alrededor del auto seleccionado
        if selected_car:
            pygame.draw.rect(screen, YELLOW, selected_car.rect, 3)


           
        pygame.display.flip()
 
    pygame.quit()
    sys.exit()


# Apariencia del menu:
apariencia = pygame_menu.Theme(
    background_color=(0, 0, 128), 
    title_background_color=(0, 0, 0), 
    title_font_shadow=True,
    title_font=pygame_menu.font.FONT_BEBAS,
    widget_font=pygame_menu.font.FONT_FRANCHISE,
    widget_font_color=(255, 255, 255),  
    widget_margin=(0, 30),
    selection_color=(255,165,0)
)

menu = pygame_menu.Menu('Car Puzzle',800, 600, theme=apariencia)
menu.add.dropselect('Difficulty :', [('Nivel 1', 1), ('Nivel 2', 2)], onchange=set_dificultad)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Bucle principal del menú
while True:
    screen.fill(BLACK)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
    pygame.display.flip()
