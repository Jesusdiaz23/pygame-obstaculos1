import pygame
import random

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VIOLETA = (255, 0, 255)

# Número de estrellas en el fondo
NUMERO_ESTRELLAS = 200  # Aumenta este número para más estrellas

pygame.mixer.init()

# Cargar la música
pygame.mixer.music.load('start-263390.mp3')  # Reemplaza con la ruta de tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (de 0 a 1)
pygame.mixer.music.play(-1, 0.0)  # Reproduce la música en bucle

class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([2, 2])  # Estrella como un pequeño punto
        self.image.fill(BLANCO
                        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 600)

    def update(self):
        pass  # Si quieres animar las estrellas o hacerlas parpadear, puedes agregar aquí código

class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y, largo, alto, color, direccion=None, velocidad=1):
        super().__init__()
        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = direccion  # 'horizontal' o 'vertical'
        self.velocidad = velocidad  # Velocidad de movimiento

    def update(self):
        # Si la dirección es 'vertical', mover hacia arriba/abajo
        if self.direccion == 'vertical':
            self.rect.y += self.velocidad
            # Si la pared llega al borde superior o inferior de la pantalla, se mueve hacia el otro lado
            if self.rect.top < 0 or self.rect.bottom > 600:
                self.velocidad = -self.velocidad  # Cambiar dirección

        # Si la dirección es 'horizontal', mover hacia la izquierda/derecha
        elif self.direccion == 'horizontal':
            self.rect.x += self.velocidad
            # Si la pared llega al borde izquierdo o derecho de la pantalla, se mueve hacia el otro lado
            if self.rect.left < 0 or self.rect.right > 800:
                self.velocidad = -self.velocidad  # Cambiar dirección

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
        # Vuelve al inicio si colide con una pared
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
            [390, 50, 20, 500, AZUL, 'vertical', 1],  # Pared moviéndose verticalmente
            [150, 100, 20, 200, VERDE, 'horizontal', 2],  # Pared moviéndose horizontalmente
            [300, 100, 20, 200, VERDE, 'horizontal', 1],  # Pared moviéndose horizontalmente
            [500, 100, 20, 200, VERDE, 'vertical', 1],  # Pared moviéndose verticalmente
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

class Cuarto2(Cuarto):
    def __init__(self):
        super().__init__()
        paredes = [
            [0, 0, 20, 250, ROJO], [0, 350, 20, 250, ROJO],
            [780, 0, 20, 250, ROJO], [780, 350, 20, 250, ROJO],
            [20, 0, 760, 20, ROJO], [20, 580, 760, 20, ROJO],
            [190, 50, 20, 500, AZUL, 'vertical', 1],  # Pared moviéndose verticalmente
            [590, 50, 20, 500, AZUL, 'horizontal', 1],  # Pared moviéndose horizontalmente
            [100, 100, 20, 200, BLANCO], [200, 100, 20, 200, BLANCO],
            [300, 100, 20, 200, BLANCO], [400, 100, 20, 200, BLANCO],
            [500, 100, 20, 200, BLANCO], [600, 100, 20, 200, BLANCO],
            [100, 300, 20, 200, VIOLETA], [200, 300, 20, 200, VIOLETA],
            [300, 300, 20, 200, VIOLETA], [400, 300, 20, 200, VIOLETA],
            [500, 300, 20, 200, VIOLETA], [600, 300, 20, 200, VIOLETA],
            [200, 500, 20, 80, VERDE], [400, 500, 20, 80, VERDE],
            [600, 500, 20, 80, VERDE],
        ]
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4], item[5] if len(item) > 5 else None, item[6] if len(item) > 6 else 1)
            self.pared_lista.add(pared)

class Cuarto3(Cuarto):
    def __init__(self):
        super().__init__()
        paredes = [
            [0, 0, 20, 250, VIOLETA], [0, 350, 20, 250, VIOLETA],
            [780, 0, 20, 250, VIOLETA], [780, 350, 20, 250, VIOLETA],
            [20, 0, 760, 20, VIOLETA], [20, 580, 760, 20, VIOLETA]
        ]
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4], item[5] if len(item) > 5 else None, item[6] if len(item) > 6 else 1)
            self.pared_lista.add(pared)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                pared = Pared(x, y, 20, 200, ROJO, 'vertical', 1)
                self.pared_lista.add(pared)

        for x in range(150, 700, 100):
            pared = Pared(x, 200, 20, 200, BLANCO, 'horizontal', 1)
            self.pared_lista.add(pared)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Laberinto')

    fuente = pygame.font.Font(None, 40)
    texto_finalizado = fuente.render('¡Felicidades! Has completado los obstáculos.', True, BLANCO)
    texto_rect = texto_finalizado.get_rect(center=(400, 300))

    # Pantalla de inicio
    texto_inicio = fuente.render('Presiona cualquier tecla para comenzar', True, BLANCO)
    texto_inicio_rect = texto_inicio.get_rect(center=(400, 250))

    protagonista = Protagonista(50, 50)
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(protagonista)

    habitaciones = []
    habitaciones.append(Cuarto1())
    habitaciones.append(Cuarto2())
    habitaciones.append(Cuarto3())

    habitacion_actual_no = 0
    habitacion_actual = habitaciones[habitacion_actual_no]

    # Crear fondo de estrellas
    estrellas = pygame.sprite.Group()
    for _ in range(NUMERO_ESTRELLAS):
        estrella = Estrella()
        estrellas.add(estrella)

    reloj = pygame.time.Clock()
    hecho = False
    juego_terminado = False
    en_inicio = True  # Variable para saber si estamos en la pantalla de inicio

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN:
                if en_inicio:
                    # Al presionar cualquier tecla, empezar el juego
                    en_inicio = False
                else:
                    if evento.key == pygame.K_LEFT:
                        protagonista.cambiovelocidad(-3, 0)
                    elif evento.key == pygame.K_RIGHT:
                        protagonista.cambiovelocidad(3, 0)
                    elif evento.key == pygame.K_UP:
                        protagonista.cambiovelocidad(0, -3)
                    elif evento.key == pygame.K_DOWN:
                        protagonista.cambiovelocidad(0, 3)

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    protagonista.cambiovelocidad(3, 0)
                elif evento.key == pygame.K_RIGHT:
                    protagonista.cambiovelocidad(-3, 0)
                elif evento.key == pygame.K_UP:
                    protagonista.cambiovelocidad(0, 3)
                elif evento.key == pygame.K_DOWN:
                    protagonista.cambiovelocidad(0, -3)

        if en_inicio:
            # Mostrar la pantalla de inicio
            pantalla.fill(NEGRO)
            pantalla.blit(texto_inicio, texto_inicio_rect)
            pygame.display.flip()
            continue  # Salir del ciclo actual para evitar actualizar el juego

        # Mover al protagonista y verificar si choca con las paredes
        protagonista.mover(habitacion_actual.pared_lista)

        # Actualizar las paredes (moverlas)
        habitacion_actual.pared_lista.update()

        # Verifica si el protagonista toca cualquier borde o pared
        lista_impactos_bloques = pygame.sprite.spritecollide(protagonista, habitacion_actual.pared_lista, False)
        if lista_impactos_bloques:
            protagonista.reiniciar()  # Reinicia al protagonista si hay colisión

        # Verifica si se ha llegado al último cuarto
        if protagonista.rect.x < -15:
            if habitacion_actual_no > 0:
                habitacion_actual_no -= 1
                habitacion_actual = habitaciones[habitacion_actual_no]
                protagonista.rect.x = 790
        elif protagonista.rect.x > 801:
            if habitacion_actual_no < len(habitaciones) - 1:
                habitacion_actual_no += 1
                habitacion_actual = habitaciones[habitacion_actual_no]
                protagonista.rect.x = 0
            else:
                # Mostrar mensaje de finalización solo al final del juego
                pantalla.fill(NEGRO)
                pantalla.blit(texto_finalizado, texto_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar el juego
                juego_terminado = True

        if not juego_terminado:
            pantalla.fill(NEGRO)
            estrellas.update()  # Actualizar las estrellas (si tienes animaciones, las manejas aquí)
            estrellas.draw(pantalla)  # Dibujar las estrellas primero
            todos_los_sprites.draw(pantalla)  # Dibujar los sprites del juego
            habitacion_actual.pared_lista.draw(pantalla)  # Dibujar las paredes
            pygame.display.flip()
            reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()