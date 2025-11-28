import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema de Exploración - Deltarune")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# FPS
reloj = pygame.time.Clock()
FPS = 60

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 3
        self.direccion = "abajo"  # Dirección inicial
        
        # Cargar sprites para cada dirección
        self.sprites = {}
        try:
            # Intenta cargar sprites para cada dirección
            self.sprites["arriba"] = pygame.image.load("assets\Kris\Caminando\Arriba\kris arriba 1.png")
            self.sprites["abajo"] = pygame.image.load("assets\Kris\Caminando\Abajo\kris abajo 1.png")
            self.sprites["izquierda"] = pygame.image.load("assets\Kris\Caminando\Izquierda\kris izquierda 1.png")
            self.sprites["derecha"] = pygame.image.load("assets\Kris\Caminando\Derecha\kris derecha 1.png")
            
            # Escalar sprites (ajusta el tamaño según necesites)
            for direccion in self.sprites:
                self.sprites[direccion] = pygame.transform.scale(self.sprites[direccion], (45, 55))
        except:
            # Si no se pueden cargar las imágenes, usar cuadrado rojo
            print("No se pudieron cargar los sprites. Usando sprite de prueba.")
            self.sprites["arriba"] = pygame.Surface((32, 32))
            self.sprites["abajo"] = pygame.Surface((32, 32))
            self.sprites["izquierda"] = pygame.Surface((32, 32))
            self.sprites["derecha"] = pygame.Surface((32, 32))
            for direccion in self.sprites:
                self.sprites[direccion].fill((255, 0, 0))
        
        self.surface = self.sprites[self.direccion]
        self.ancho = self.surface.get_width()
        self.alto = self.surface.get_height()
        
    def mover(self, teclas, mapa):
        # Guardar posición anterior
        pos_anterior_x = self.x
        pos_anterior_y = self.y
        
        # Movimiento en 4 direcciones
        moviendo = False
        
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidad
            self.direccion = "arriba"
            moviendo = True
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidad
            self.direccion = "abajo"
            moviendo = True
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidad
            self.direccion = "izquierda"
            moviendo = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidad
            self.direccion = "derecha"
            moviendo = True
        
        # Actualizar el sprite según la dirección
        if moviendo:
            self.surface = self.sprites[self.direccion]
        
        # Mantener al jugador dentro de la pantalla
        self.x = max(0, min(self.x, ANCHO - self.ancho))
        self.y = max(0, min(self.y, ALTO - self.alto))
        
        # Verificar colisiones con el mapa
        if mapa.hay_colision(self.x, self.y, self.ancho, self.alto):
            # Si hay colisión, volver a la posición anterior
            self.x = pos_anterior_x
            self.y = pos_anterior_y
    
    def dibujar(self, superficie):
        superficie.blit(self.surface, (self.x, self.y))

class Mapa:
    def __init__(self, ruta_imagen, ruta_colisiones=None):
        try:
            # Cargar la imagen del mapa
            self.imagen = pygame.image.load(ruta_imagen)
            # Escalar la imagen al tamaño de la pantalla si es necesario
            self.imagen = pygame.transform.scale(self.imagen, (ANCHO, ALTO))
        except:
            # Si no se puede cargar la imagen, crear un fondo de prueba
            print("No se pudo cargar la imagen. Usando fondo de prueba.")
            self.imagen = pygame.Surface((ANCHO, ALTO))
            self.imagen.fill((50, 100, 50))
            # Dibujar un patrón de cuadrícula
            for i in range(0, ANCHO, 32):
                pygame.draw.line(self.imagen, (40, 80, 40), (i, 0), (i, ALTO))
            for i in range(0, ALTO, 32):
                pygame.draw.line(self.imagen, (40, 80, 40), (0, i), (ANCHO, i))
        
        # Cargar mapa de colisiones
        self.mapa_colisiones = None
        if ruta_colisiones:
            try:
                self.mapa_colisiones = pygame.image.load(ruta_colisiones)
                self.mapa_colisiones = pygame.transform.scale(self.mapa_colisiones, (ANCHO, ALTO))
                print("Mapa de colisiones cargado correctamente.")
            except:
                print("No se pudo cargar el mapa de colisiones.")
    
    def hay_colision(self, x, y, ancho, alto):
        """
        Verifica si hay colisión en la posición dada.
        Revisa los píxeles negros (0, 0, 0) en el mapa de colisiones.
        """
        if self.mapa_colisiones is None:
            return False
        
        # Verificar las 4 esquinas del personaje
        esquinas = [
            (int(x), int(y)),  # Superior izquierda
            (int(x + ancho - 1), int(y)),  # Superior derecha
            (int(x), int(y + alto - 1)),  # Inferior izquierda
            (int(x + ancho - 1), int(y + alto - 1))  # Inferior derecha
        ]
        
        for px, py in esquinas:
            # Verificar que esté dentro de los límites
            if 0 <= px < ANCHO and 0 <= py < ALTO:
                color = self.mapa_colisiones.get_at((px, py))
                # Si el píxel es negro (o muy oscuro), hay colisión
                if color[0] < 50 and color[1] < 50 and color[2] < 50:
                    return True
        
        return False
    
    def dibujar(self, superficie):
        superficie.blit(self.imagen, (0, 0))

# Crear objetos del juego
mapa = Mapa("assets\Mapa_Inicial\Secciones\seccion 1\mapa inicial seccion 1.jpeg", "assets\Mapa_Inicial\Secciones\seccion 1\colisiones.png")
jugador = Jugador(ANCHO // 2, ALTO // 2)

# Loop principal del juego
corriendo = True
while corriendo:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
    
    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()
    
    # Actualizar
    jugador.mover(teclas, mapa)
    
    # Dibujar
    mapa.dibujar(pantalla)
    jugador.dibujar(pantalla)
    
    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(FPS)

# Salir
pygame.quit()
sys.exit()
