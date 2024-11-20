import pygame
import random
import sys  # Necesitamos importar sys para salir del juego

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VIOLETA = (255, 0, 255)

NUMERO_ESTRELLAS = 200

# Clase Estrella
class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([2, 2])  # Estrella como un pequeño punto
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 600)

    def update(self):
        pass

# Clase Pared
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
        # Mover paredes
        if self.direccion == 'vertical':
            self.rect.y += self.velocidad
            if self.rect.top < 0 or self.rect.bottom > 600:
                self.velocidad = -self.velocidad
        elif self.direccion == 'horizontal':
            self.rect.x += self.velocidad
            if self.rect.left < 0 or self.rect.right > 800:
                self.velocidad = -self.velocidad

# Clase Protagonista
class Protagonista(pygame.sprite.Sprite):
    VELOCIDAD = 5  # Velocidad base para el movimiento

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.cambio_x = 0
        self.cambio_y = 0

    def cambiovelocidad(self, x, y):
        """Ajusta la velocidad del personaje."""
        self.cambio_x = x
        self.cambio_y = y

    def mover(self, paredes):
        """Mueve al personaje y detecta colisiones con las paredes."""
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
        """Reinicia la posición del protagonista a la inicial."""
        self.rect.x = 50
        self.rect.y = 50

# Clase Cuarto base
class Cuarto():
    pared_lista = None
    sprites_enemigos = None

    def __init__(self):
        self.pared_lista = pygame.sprite.Group()
        self.sprites_enemigos = pygame.sprite.Group()

# Cuarto1
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

# Cuarto2
class Cuarto2(Cuarto):
    def __init__(self):
        super().__init__()
        paredes = [
            [0, 0, 20, 250, ROJO], [0, 350, 20, 250, ROJO],
            [780, 0, 20, 250, ROJO], [780, 350, 20, 250, ROJO],
            [20, 0, 760, 20, ROJO], [20, 580, 760, 20, ROJO],
            [190, 50, 20, 500, AZUL, 'vertical', 1],  
            [590, 50, 20, 500, AZUL, 'horizontal', 1],  
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

# Cuarto3
class Cuarto3(Cuarto):
    def __init__(self):
        super().__init__()
        paredes = [
            [0, 0, 20, 250, ROJO], [0, 350, 20, 250, ROJO],
            [780, 0, 20, 250, ROJO], [780, 350, 20, 250, ROJO],
            [20, 0, 760, 20, ROJO], [20, 580, 760, 20, ROJO],
            [100, 50, 20, 500, VERDE, 'horizontal', 1],
            [200, 50, 20, 500, VERDE, 'vertical', 1],  
            [300, 50, 20, 500, VERDE, 'horizontal', 1],  
            [400, 50, 20, 500, VERDE, 'vertical', 1],  
            [500, 50, 20, 500, VERDE, 'horizontal', 1],  
            [600, 50, 20, 500, VERDE, 'vertical', 1],  
        ]
        for item in paredes:
            pared = Pared(item[0], item[1], item[2], item[3], item[4], item[5] if len(item) > 5 else None, item[6] if len(item) > 6 else 1)
            self.pared_lista.add(pared)

# Función para mostrar el mensaje final y cerrar el juego
def mostrar_mensaje_final():
    # Configura la pantalla
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 55)  # Fuente más grande
    mensaje = font.render("¡Has ganado! El juego terminará en breve...", True, BLANCO)
    
    # Calcula la posición para centrar el mensaje en la pantalla
    mensaje_rect = mensaje.get_rect()
    mensaje_rect.center = (400, 300)  # Centrado en el medio de la pantalla
    
    screen.fill(NEGRO)  # Fondo negro
    screen.blit(mensaje, mensaje_rect)  # Dibuja el mensaje en la pantalla
    pygame.display.update()
    
    # Espera 2 segundos antes de cerrar
    pygame.time.wait(2000)
    
    # Cierra pygame y termina el juego
    pygame.quit()
    sys.exit()

# Función principal
def main():
    pygame.init()
    pantalla = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Laberinto')

    fuente = pygame.font.Font(None, 40)
    texto_finalizado = fuente.render('¡Felicidades! Has completado los obstáculos.', True, BLANCO)
    texto_rect = texto_finalizado.get_rect(center=(400, 300))

    texto_inicio = fuente.render('Presiona "A" para comenzar', True, BLANCO)
    texto_inicio_rect = texto_inicio.get_rect(center=(400, 250))

    protagonista = Protagonista(50, 50)
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(protagonista)

    habitaciones = [Cuarto1(), Cuarto2(), Cuarto3()]
    habitacion_actual_no = 0
    habitacion_actual = habitaciones[habitacion_actual_no]

    estrellas = pygame.sprite.Group()
    for _ in range(NUMERO_ESTRELLAS):
        estrella = Estrella()
        estrellas.add(estrella)

    pygame.joystick.init()
    joystick_conectado = False
    if pygame.joystick.get_count() > 0:
        joystick_conectado = True
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    reloj = pygame.time.Clock()
    hecho = False
    juego_terminado = False
    en_inicio = True

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN:
                if en_inicio:
                    en_inicio = False
                elif evento.key == pygame.K_LEFT:
                    protagonista.cambiovelocidad(-protagonista.VELOCIDAD, 0)
                elif evento.key == pygame.K_RIGHT:
                    protagonista.cambiovelocidad(protagonista.VELOCIDAD, 0)
                elif evento.key == pygame.K_UP:
                    protagonista.cambiovelocidad(0, -protagonista.VELOCIDAD)
                elif evento.key == pygame.K_DOWN:
                    protagonista.cambiovelocidad(0, protagonista.VELOCIDAD)
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    protagonista.cambiovelocidad(0, protagonista.cambio_y)
                elif evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    protagonista.cambiovelocidad(protagonista.cambio_x, 0)

            elif evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0:  # Botón "A" del joystick
                    en_inicio = False

        if en_inicio:
            pantalla.fill(NEGRO)
            pantalla.blit(texto_inicio, texto_inicio_rect)
            pygame.display.flip()
            continue

        if joystick_conectado:
            eje_x = joystick.get_axis(0)
            eje_y = joystick.get_axis(1)
            velocidad_ajustada_x = int(eje_x * protagonista.VELOCIDAD)
            velocidad_ajustada_y = int(eje_y * protagonista.VELOCIDAD)
            protagonista.cambiovelocidad(velocidad_ajustada_x, velocidad_ajustada_y)

        protagonista.mover(habitacion_actual.pared_lista)
        habitacion_actual.pared_lista.update()

        lista_impactos_bloques = pygame.sprite.spritecollide(protagonista, habitacion_actual.pared_lista, False)
        if lista_impactos_bloques:
            protagonista.reiniciar()

        # Avance de niveles
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
                # Cuando el jugador termine el último nivel, mostramos el mensaje final
                mostrar_mensaje_final()  # Esta función cierra el juego

        if not juego_terminado:
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
