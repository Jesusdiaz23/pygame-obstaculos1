import pygame
import random

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VIOLETA = (255, 0, 255)

NUMERO_ESTRELLAS = 200

# Inicializar joysticks
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([2, 2])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 600)

class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y, largo, alto, color, direccion=None, velocidad=1):
        super().__init__()
        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = direccion
        self.velocidad = velocidad

    def update(self):
        if self.direccion == 'vertical':
            self.rect.y += self.velocidad
            if self.rect.top < 0 or self.rect.bottom > 600:
                self.velocidad = -self.velocidad
        elif self.direccion == 'horizontal':
            self.rect.x += self.velocidad
            if self.rect.left < 0 or self.rect.right > 800:
                self.velocidad = -self.velocidad

class Protagonista(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def cambiovelocidad(self, x, y):
        self.cambio_x += x
        self.cambio_y += y

    def mover(self, paredes):
        self.rect.x += self.cambio_x
        lista_impactos_bloques = pygame.sprite.spritecollide(self, paredes, False)
        for bloque in lista_impactos_bloques:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                self.rect.left = bloque.rect.right
        self.rect.y += self.cambio_y
        lista_impactos_bloques = pygame.sprite.spritecollide(self, paredes, False)
        for bloque in lista_impactos_bloques:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top
            else:
                self.rect.top = bloque.rect.bottom

    def reiniciar(self):
        self.rect.x = 50
        self.rect.y = 50

class Cuarto():
    pared_lista = None
    sprites_enemigos = None

    def __init__(self):
        self.pared_lista = pygame.sprite.Group()
        self.sprites_enemigos = pygame.sprite.Group()

class Cuarto1(Cuarto):
    def __init__(self):
        super().__init__()
        paredes = [
            [0, 0, 20, 250, BLANCO], [0, 350, 20, 250, BLANCO],
            [780, 0, 20, 250, BLANCO], [780, 350, 20, 250, BLANCO],
            [20, 0, 760, 20, BLANCO], [20, 580, 760, 20, BLANCO],
            [390, 50, 20, 500, AZUL, 'vertical', 1],
            [150, 100, 20, 200, VERDE, 'horizontal', 2],
            [300, 100, 20, 200, VERDE, 'horizontal', 1],
            [500, 100, 20, 200, VERDE, 'vertical', 1],
            [150, 300, 20, 200, VERDE, 'vertical', 1],
            [300, 300, 20, 200, VERDE, 'vertical', 1],
            [500, 300, 20, 200, VERDE, 'vertical', 1],
            [250, 450, 20, 100, VIOLETA, 'horizontal', 1],
            [400, 450, 20, 100, VIOLETA, 'horizontal', 1],
            [550, 450, 20, 100, VIOLETA, 'horizontal', 1],
        ]
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4], item[5] if len(item) > 5 else None, item[6] if len(item) > 6 else 1)
            self.pared_lista.add(pared)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Laberinto')

    fuente = pygame.font.Font(None, 40)
    texto_finalizado = fuente.render('¡Felicidades! Has completado los obstáculos.', True, BLANCO)
    texto_rect = texto_finalizado.get_rect(center=(400, 300))

    texto_inicio = fuente.render('Presiona cualquier tecla para comenzar', True, BLANCO)
    texto_inicio_rect = texto_inicio.get_rect(center=(400, 250))

    protagonista = Protagonista(50, 50)
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(protagonista)

    habitaciones = [Cuarto1()]
    habitacion_actual_no = 0
    habitacion_actual = habitaciones[habitacion_actual_no]

    estrellas = pygame.sprite.Group()
    for _ in range(NUMERO_ESTRELLAS):
        estrella = Estrella()
        estrellas.add(estrella)

    reloj = pygame.time.Clock()
    hecho = False
    juego_terminado = False
    en_inicio = True

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN and en_inicio:
                en_inicio = False

        if joystick:
            protagonista.cambiovelocidad(joystick.get_axis(0) * 3, joystick.get_axis(1) * 3)

        if en_inicio:
            pantalla.fill(NEGRO)
            pantalla.blit(texto_inicio, texto_inicio_rect)
            pygame.display.flip()
            continue

        protagonista.mover(habitacion_actual.pared_lista)
        habitacion_actual.pared_lista.update()
        
        if pygame.sprite.spritecollide(protagonista, habitacion_actual.pared_lista, False):
            protagonista.reiniciar()

        pantalla.fill(NEGRO)
        estrellas.update()
        estrellas.draw(pantalla)
        todos_los_sprites.draw(pantalla)
        habitacion_actual.pared_lista.draw(pantalla)
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
