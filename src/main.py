import pygame
import sys

# Importar las pantallas
from pantalla_inicial import PantallaTitulo
from exploracion_system import JuegoExploracion

pygame.init()

# Configuración general
ANCHO = 1280
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pokérune")

clock = pygame.time.Clock()
FPS = 60

class GameManager:
    def __init__(self):
        self.pantalla_actual = "titulo"
        self.pantalla_titulo = PantallaTitulo(pantalla)
        self.juego = None

    def cambiar_pantalla(self, nueva_pantalla):
        """Cambia entre pantallas del juego"""
        self.pantalla_actual = nueva_pantalla

        if nueva_pantalla == "juego":
            self.juego = JuegoExploracion(self.pantalla_titulo.pantalla)
        print("Cambiando a pantalla de juego")

    def actualizar(self, eventos):
        """Actualiza la pantalla actual"""
        if self.pantalla_actual == "titulo":
            accion = self.pantalla_titulo.actualizar(eventos)

            if accion == "jugar":
                self.cambiar_pantalla("juego")
                return True
            elif accion == "salir":
                return False
            
        elif self.pantalla_actual == "juego":
            continuar = self.juego.actualizar(eventos)

            if not continuar:
                # Si presionan ESC en el juego, volver al título
                self.cambiar_pantalla("titulo")
                return True

        return True
    
    def dibujar(self):
        """Dibuja la pantalla actual"""
        if self.pantalla_actual == "titulo":
            self.pantalla_titulo.dibujar()
        elif self.pantalla_actual == "juego" and self.juego is not None:
            self.juego.dibujar()

def main():
    """Función principal del juego"""
    game_manager = GameManager()
    corriendo = True

    while corriendo:
        clock.tick(FPS)
        
        # Manejar eventos generales
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Actualizar
        resultado = game_manager.actualizar(eventos)
        if resultado == False:
            corriendo = False
            
        # Dibujar
        game_manager.dibujar()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
