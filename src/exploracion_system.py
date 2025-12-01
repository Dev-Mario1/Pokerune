import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema de Exploración")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# FPS
reloj = pygame.time.Clock()
FPS = 60

class Personaje:
    def __init__(self, x, y, nombre, color_debug=(255, 0, 0)):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.color_debug = color_debug
        self.velocidad = 3
        self.direccion = "abajo"
        
        # Historial de posiciones para seguimiento
        self.historial_posiciones = []
        self.max_historial = 20  # Cuántas posiciones recordar
        
        # Cargar sprites
        self.sprites = {}
        try:
            # Rutas de los sprites
            if nombre == "Kris":
                self.sprites["arriba"] = pygame.image.load("Pokerune-main/assets/Kris/Caminando/Arriba/kris arriba 1.png")
                self.sprites["abajo"] = pygame.image.load("Pokerune-main/assets/Kris/Caminando/Abajo/kris abajo 1.png")
                self.sprites["izquierda"] = pygame.image.load("Pokerune-main/assets/Kris/Caminando/Izquierda/kris izquierda 1.png")
                self.sprites["derecha"] = pygame.image.load("Pokerune-main/assets/Kris/Caminando/Derecha/kris derecha 1.png")
            elif nombre == "Luigi":
                self.sprites["arriba"] = pygame.image.load("Pokerune-main/assets/Luigi/Caminando/Arriba/luigi arriba 1.png")
                self.sprites["abajo"] = pygame.image.load("Pokerune-main/assets/Luigi/Caminando/Abajo/luigi abajo 1.png")
                self.sprites["izquierda"] = pygame.image.load("Pokerune-main/assets/Luigi/Caminando/Izquierda/luigi izquierda 1.png")
                self.sprites["derecha"] = pygame.image.load("Pokerune-main/assets/Luigi/Caminando/Derecha/luigi derecha 1.png")
            elif nombre == "Garchomp":
                # CAMBIA ESTAS RUTAS según donde tengas los sprites de Ralsei
                self.sprites["arriba"] = pygame.image.load("Pokerune-main/assets/Garchomp/Caminando/Arriba/garchomp arriba 1.png")
                self.sprites["abajo"] = pygame.image.load("Pokerune-main/assets/Garchomp/Caminando/Abajo/garchomp abajo 1.png")
                self.sprites["izquierda"] = pygame.image.load("Pokerune-main/assets/Garchomp/Caminando/Izquierda/garchomp izquierda 1.png")
                self.sprites["derecha"] = pygame.image.load("Pokerune-main/assets/Garchomp/Caminando/Derecha/garchomp derecha 1.png")
            
            for direccion in self.sprites:
                self.sprites[direccion] = pygame.transform.scale(self.sprites[direccion], (45, 55))
        except:
            print(f"No se pudieron cargar los sprites de {nombre}. Usando sprite de prueba.")
            self.sprites["arriba"] = pygame.Surface((32, 32))
            self.sprites["abajo"] = pygame.Surface((32, 32))
            self.sprites["izquierda"] = pygame.Surface((32, 32))
            self.sprites["derecha"] = pygame.Surface((32, 32))
            for direccion in self.sprites:
                self.sprites[direccion].fill(self.color_debug)
        
        self.surface = self.sprites[self.direccion]
        self.ancho = self.surface.get_width()
        self.alto = self.surface.get_height()
    
    def actualizar_historial(self):
        """Guarda la posición actual en el historial"""
        self.historial_posiciones.append((self.x, self.y, self.direccion))
        if len(self.historial_posiciones) > self.max_historial:
            self.historial_posiciones.pop(0)
    
    def seguir_posicion(self, x, y, direccion):
        """Mueve el personaje a una posición específica"""
        self.x = x
        self.y = y
        self.direccion = direccion
        self.surface = self.sprites[self.direccion]
    
    def dibujar(self, superficie):
        superficie.blit(self.surface, (self.x, self.y))

class Party:
    def __init__(self, x, y):
        # Crear los 3 personajes del party
        self.personajes = [
            Personaje(x, y, "Kris", (255, 0, 0)),      # Líder (rojo)
            Personaje(x, y, "Luigi", (255, 0, 255)),   # Segundo (magenta)
            Personaje(x, y, "Garchomp", (0, 255, 0))     # Tercero (verde)
        ]
        
        self.lider = self.personajes[0]
        self.velocidad = 3
        
        # Inicializar historial de todos
        for personaje in self.personajes:
            for _ in range(personaje.max_historial):
                personaje.actualizar_historial()
    
    def mover(self, teclas, mapa):
        # Guardar posición anterior del líder
        pos_anterior_x = self.lider.x
        pos_anterior_y = self.lider.y
        pos_anterior_dir = self.lider.direccion
        
        # Movimiento del líder
        moviendo = False
        
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.lider.y -= self.velocidad
            self.lider.direccion = "arriba"
            moviendo = True
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.lider.y += self.velocidad
            self.lider.direccion = "abajo"
            moviendo = True
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.lider.x -= self.velocidad
            self.lider.direccion = "izquierda"
            moviendo = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.lider.x += self.velocidad
            self.lider.direccion = "derecha"
            moviendo = True
        
        # Actualizar sprite del líder
        if moviendo:
            self.lider.surface = self.lider.sprites[self.lider.direccion]
        
        # Mantener al líder dentro de la pantalla
        self.lider.x = max(0, min(self.lider.x, ANCHO - self.lider.ancho))
        self.lider.y = max(0, min(self.lider.y, ALTO - self.lider.alto))
        
        # Verificar colisiones del líder
        if mapa.hay_colision(self.lider.x, self.lider.y, self.lider.ancho, self.lider.alto):
            self.lider.x = pos_anterior_x
            self.lider.y = pos_anterior_y
            return  # No actualizar seguidores si hay colisión
        
        # Si el líder se movió, actualizar historial y seguidores
        if moviendo:
            # Actualizar historial del líder
            self.lider.actualizar_historial()
            
            # Hacer que los seguidores sigan al líder
            for i in range(1, len(self.personajes)):
                personaje_anterior = self.personajes[i - 1]
                personaje_actual = self.personajes[i]
                
                # El seguidor sigue la posición retrasada del anterior
                distancia_retraso = 15
                if len(personaje_anterior.historial_posiciones) > distancia_retraso:
                    pos_historica = personaje_anterior.historial_posiciones[-distancia_retraso]
                    personaje_actual.seguir_posicion(
                        pos_historica[0],
                        pos_historica[1],
                        pos_historica[2]
                    )
                    personaje_actual.actualizar_historial()
    
    def dibujar(self, superficie):
        # Dibujar en orden inverso para que el líder esté adelante
        for personaje in reversed(self.personajes):
            personaje.dibujar(superficie)
    
    def get_lider(self):
        return self.lider

class Mapa:
    def __init__(self, ruta_imagen, ruta_colisiones=None):
        try:
            self.imagen = pygame.image.load(ruta_imagen)
            self.imagen = pygame.transform.scale(self.imagen, (ANCHO, ALTO))
        except:
            print("No se pudo cargar la imagen. Usando fondo de prueba.")
            self.imagen = pygame.Surface((ANCHO, ALTO))
            self.imagen.fill((50, 100, 50))
            for i in range(0, ANCHO, 32):
                pygame.draw.line(self.imagen, (40, 80, 40), (i, 0), (i, ALTO))
            for i in range(0, ALTO, 32):
                pygame.draw.line(self.imagen, (40, 80, 40), (0, i), (ANCHO, i))
        
        self.mapa_colisiones = None
        if ruta_colisiones:
            try:
                self.mapa_colisiones = pygame.image.load(ruta_colisiones)
                self.mapa_colisiones = pygame.transform.scale(self.mapa_colisiones, (ANCHO, ALTO))
                print("Mapa de colisiones cargado correctamente.")
            except:
                print("No se pudo cargar el mapa de colisiones.")
    
    def hay_colision(self, x, y, ancho, alto):
        if self.mapa_colisiones is None:
            return False
        
        esquinas = [
            (int(x), int(y)),
            (int(x + ancho - 1), int(y)),
            (int(x), int(y + alto - 1)),
            (int(x + ancho - 1), int(y + alto - 1))
        ]
        
        for px, py in esquinas:
            if 0 <= px < ANCHO and 0 <= py < ALTO:
                color = self.mapa_colisiones.get_at((px, py))
                if color[0] < 50 and color[1] < 50 and color[2] < 50:
                    return True
        
        return False
    
    def dibujar(self, superficie):
        superficie.blit(self.imagen, (0, 0))

# Crear objetos del juego
mapa = Mapa("Pokerune-main/assets/Mapa_Inicial/Secciones/seccion 1/mapa inicial seccion 1.jpeg", "Pokerune-main/assets/Mapa_Inicial/Secciones/seccion 1/colisiones.png")
party = Party(ANCHO // 2, ALTO // 2)

# Loop principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
    
    teclas = pygame.key.get_pressed()
    
    # Actualizar
    party.mover(teclas, mapa)
    
    # Dibujar
    mapa.dibujar(pantalla)
    party.dibujar(pantalla)
    
    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(FPS)

# Salir
pygame.quit()
sys.exit()