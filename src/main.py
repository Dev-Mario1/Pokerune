import pygame

import pantalla_inicial
import exploracion_system

pygame.init()

# Configuración general
ANCHO = 1280
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("POKERUNE")

clock = pygame.time.Clock()
FPS = 60

class GameManager:
    def __init__(self):
        self.pantalla_actual = "titulo"  # Puede ser: "titulo", "juego"
        self.pantalla_titulo = pantalla_inicial(pantalla)
        self.juego = None
        
    def cambiar_pantalla(self, nueva_pantalla):
        """Cambia entre pantallas del juego"""
        self.pantalla_actual = nueva_pantalla
        
        if nueva_pantalla == "juego" and self.juego is None:
            # Crear el juego la primera vez que se accede
            self.juego = exploracion_system(pantalla)
    
    def actualizar(self):
        """Actualiza la pantalla actual"""
        if self.pantalla_actual == "titulo":
            accion = self.pantalla_titulo.actualizar()
            
            if accion == "jugar":
                self.cambiar_pantalla("juego")
            elif accion == "salir":
                return False
                
        elif self.pantalla_actual == "juego":
            continuar = self.juego.actualizar()
            
            if not continuar:
                # Si presionan ESC en el juego, volver al título
                self.cambiar_pantalla("titulo")
        
        return True
    
    def dibujar(self):
        """Dibuja la pantalla actual"""
        if self.pantalla_actual == "titulo":
            self.pantalla_titulo.dibujar()
        elif self.pantalla_actual == "juego":
            self.juego.dibujar()

def main():
    """Función principal del juego"""
    game_manager = GameManager()
    corriendo = True
    
    while corriendo:
        clock.tick(FPS)
        
        # Manejar eventos generales
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        # Actualizar
        if not game_manager.actualizar():
            corriendo = False
        
        # Dibujar
        game_manager.dibujar()
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()