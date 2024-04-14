#huge shotout to Tech with Tim "pygame in 90 minutes" video for teaching most of the stuff I used here 
#also, I'm so fking proud of this, even if it sucks, it took like 3 days afterall (WOW!! 3 WHOLE DAYS NO WAY!!!)
#to "customize" difficulty just change a bit crear_tuberias() or the VEL variables/constants
import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Flappy Navidad")

CHOQUE = pygame.USEREVENT + 1

TIMESNEWROMAN_40 = pygame.font.SysFont('timesnewroman', 40)

BLANCO = (255, 255, 255)
NEGRO = (0, 0 ,0)

ANCHO, ALTURA = 300, 500
WIN = pygame.display.set_mode((ANCHO, ALTURA))

#imagenes y audios
FONDO = pygame.image.load(os.path.join('Assets','flappy_fondo.png'))
FLAPPY_ANCHO, FLAPPY_ALTO = 35, 30
FLAPPY_IMAGEN = pygame.image.load(os.path.join('Assets','flappy.png'))
FLAPPY_SONIDO = pygame.mixer.Sound(os.path.join('Sonido','flap.mp3'))
TUBERIA_ANCHO, TUBERIA_ALTO = 40, 300
TUBERIA_IMAGEN = pygame.image.load(os.path.join('Assets','regalo.png'))
TUBERIA_SONIDO = pygame.mixer.Sound(os.path.join('Sonido','puntaje.mp3'))
TUBERIA_SONIDO.set_volume(0.1)
PERDISTE_IMAGEN = pygame.image.load(os.path.join('Assets','perdiste.png'))
PRESENTACION_IMAGEN = pygame.image.load(os.path.join('Assets','presentacion.png'))
MUSICA_DE_FONDO = pygame.mixer.music.load(os.path.join('Sonido','musicafondo.mp3'))
# objeto -> tuberias/ estrellas, etc
MIN_OBJETO_X = 500
MAX_OBJETO_X = 500

tiempo_inicial = pygame.time.get_ticks()
FPS = 60

#variables del pajarraco
flappy_vel_y = 0
FLAPPY_MAX_VEL_Y = 15 
FLAPPY_ACC_Y = 0.4
flappy_flap_vel = -6
TUBERIA_VEL = 2

#variables del estado del juego que no pude poner en main xdxdxd
muerte = False
puntaje = 0

def crear_tuberias(tuberias_arriba, tuberias_abajo): 
    global tuberia
    global tuberia_abajo
    global tiempo_inicial
    
    posicion_x = random.randint(MIN_OBJETO_X, MAX_OBJETO_X)
    posicion_arriba_y = random.randint(-270, 0)

    tuberia = pygame.Rect(posicion_x, posicion_arriba_y, TUBERIA_ANCHO, TUBERIA_ALTO)
    tuberia_abajo = pygame.Rect(posicion_x, posicion_arriba_y + 470, TUBERIA_ANCHO, TUBERIA_ALTO)
    
    if pygame.time.get_ticks() - tiempo_inicial >= 1500:
        tuberias_arriba.append(tuberia)
        tuberias_abajo.append(tuberia_abajo)
        tiempo_inicial = pygame.time.get_ticks()
    
    return tuberia, tuberia_abajo

def flappyflap(flappy):
    global flappy_vel_y

    flappy_vel_y = flappy_flap_vel

    FLAPPY_SONIDO.play()

    if flappy.y < 0 - FLAPPY_ALTO:
        flappy.y = 0 - FLAPPY_ALTO
        
    return flappy_vel_y

def comprobar_choque(flappy, tuberias_arriba, tuberias_abajo):
    global tuberia
    global tuberia_abajo

    for tuberia in tuberias_arriba:
        if flappy.colliderect(tuberia):
            pygame.event.post(pygame.event.Event(CHOQUE))

    for tuberia_abajo in tuberias_abajo:
        if flappy.colliderect(tuberia_abajo):
            pygame.event.post(pygame.event.Event(CHOQUE))
        
def gravedad(flappy):
    global flappy_vel_y 

    if flappy_vel_y < FLAPPY_MAX_VEL_Y: 
        flappy_vel_y += FLAPPY_ACC_Y 
    elif flappy.y >= ALTURA - FLAPPY_ALTO:
        pygame.event.post(pygame.event.Event(CHOQUE))

    if flappy.y + FLAPPY_ACC_Y < ALTURA - FLAPPY_ALTO:
        flappy.y += flappy_vel_y

    return flappy_vel_y

def crear_ventana(flappy, tuberia, tuberias_arriba, tuberia_abajo, tuberias_abajo):
    global muerte
    global puntaje

    WIN.blit(FONDO, (0, 0))
    WIN.blit(FLAPPY_IMAGEN, (flappy.x, flappy.y))

    for tuberia in tuberias_arriba:
        WIN.blit(TUBERIA_IMAGEN, (tuberia.x, tuberia.y))
        tuberia.x -= TUBERIA_VEL
        if tuberia.x < -40:
            tuberias_arriba.remove(tuberia)
        if tuberia.x == 60:
            TUBERIA_SONIDO.play()
            puntaje += 1

    for tuberia_abajo in tuberias_abajo:
        WIN.blit(TUBERIA_IMAGEN, (tuberia_abajo.x, tuberia_abajo.y))
        tuberia_abajo.x -= TUBERIA_VEL
        if tuberia.x < 40:
            tuberias_abajo.remove(tuberia_abajo)

    puntaje_texto = TIMESNEWROMAN_40.render("Puntuación: " + str(puntaje), 1, NEGRO)
    WIN.blit(puntaje_texto, (10, 10))

    pygame.display.update()
    return puntaje

def gameover():
    global puntaje
    WIN.blit(PERDISTE_IMAGEN, ((ANCHO- PERDISTE_IMAGEN.get_width())//2,
                                (ALTURA - PERDISTE_IMAGEN.get_height())//2)) 
    pygame.display.update()
    puntaje = 0
    pygame.time.delay(2000)

def presentacion():
    WIN.blit(PRESENTACION_IMAGEN, (0, 0))
    pygame.display.update()
    pygame.time.delay(100)

def main():
    flappy = pygame.Rect(60, 200, FLAPPY_ANCHO, FLAPPY_ALTO)

    tuberias_arriba = []
    tuberias_abajo = []

    clock = pygame.time.Clock()
    pygame.mixer.music.play()
    correr = False
    muerte = False

    #presentacion
    while not correr:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
                pygame.quit() 
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        correr = True
                        muerte = False
        presentacion()
    #corrida
    while correr:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flappyflap(flappy)

            if event.type == CHOQUE:
                muerte = True
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

        if muerte != False:
            gameover()
            break
        
        comprobar_choque(flappy, tuberias_arriba, tuberias_abajo)
        crear_tuberias(tuberias_arriba, tuberias_abajo)
        gravedad(flappy)
        crear_ventana(flappy, tuberia, tuberias_arriba, tuberia_abajo, tuberias_abajo)

    main()

if __name__ == "__main__":
    main()

#POR HACER:
#Hacer que se pueda cambiar el fondo o la música?
#DA IGUAL VERSION 1 FINAL LETSGOOO