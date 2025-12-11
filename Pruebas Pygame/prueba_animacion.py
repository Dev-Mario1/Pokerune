import pygame
import os

class AnimacionSprite:
    def __init__(self, carpeta_frames, escala=(45, 55), fps_animacion=10):
        """
        Crea una animación a partir de imágenes en una carpeta
        
        Args:
            carpeta_frames: Ruta a la carpeta con los frames
            escala: Tupla (ancho, alto) para escalar los sprites
            fps_animacion: Velocidad de la animación (frames por segundo)
        """
        self.frames = []
        self.frame_actual = 0
        self.escala = escala
        self.fps_animacion = fps_animacion
        self.tiempo_por_frame = 1.0 / fps_animacion  # Tiempo en segundos por frame
        self.tiempo_acumulado = 0
        
        # Cargar todos los frames de la carpeta
        self._cargar_frames(carpeta_frames)
    
    def _cargar_frames(self, carpeta):
        """Carga todos los frames de una carpeta ordenados alfabéticamente"""
        try:
            # Obtener todos los archivos de imagen en la carpeta
            archivos = sorted([f for f in os.listdir(carpeta) 
                             if f.endswith(('.png', '.jpg', '.jpeg'))])
            
            if not archivos:
                raise Exception(f"No se encontraron imágenes en {carpeta}")
            
            # Cargar y escalar cada frame
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta, archivo)
                frame = pygame.image.load(ruta_completa)
                frame = pygame.transform.scale(frame, self.escala)
                self.frames.append(frame)
            
            print(f"Cargados {len(self.frames)} frames desde {carpeta}")
            
        except Exception as e:
            print(f"Error al cargar frames de {carpeta}: {e}")
            # Crear un frame de respaldo (cuadrado rojo)
            frame_respaldo = pygame.Surface(self.escala)
            frame_respaldo.fill((255, 0, 0))
            self.frames.append(frame_respaldo)
    
    def actualizar(self, delta_time):
        """
        Actualiza la animación según el tiempo transcurrido
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame (en segundos)
        """
        if len(self.frames) <= 1:
            return  # No hay animación si solo hay 1 frame
        
        self.tiempo_acumulado += delta_time
        
        # Cambiar al siguiente frame si ha pasado suficiente tiempo
        if self.tiempo_acumulado >= self.tiempo_por_frame:
            self.tiempo_acumulado = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
    
    def get_frame_actual(self):
        """Retorna el frame actual de la animación"""
        return self.frames[self.frame_actual]
    
    def reiniciar(self):
        """Reinicia la animación al primer frame"""
        self.frame_actual = 0
        self.tiempo_acumulado = 0
    
    def set_fps(self, nuevo_fps):
        """Cambia la velocidad de la animación"""
        self.fps_animacion = nuevo_fps
        self.tiempo_por_frame = 1.0 / nuevo_fps


# Ejemplo de uso:
if __name__ == "__main__":
    pygame.init()
    
    # Crear ventana de prueba
    pantalla = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Test Animación")
    reloj = pygame.time.Clock()
    
    # Crear animación (ajusta la ruta a tu carpeta de sprites)
    animacion = AnimacionSprite(
        carpeta_frames="Pokerune-main/assets/Luigi/Caminando/Derecha",
        escala=(100, 120),
        fps_animacion=10
    )
    
    corriendo = True
    while corriendo:
        # Delta time en segundos
        dt = reloj.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        # Actualizar animación
        animacion.actualizar(dt)
        
        # Dibujar
        pantalla.fill((50, 50, 50))
        pantalla.blit(animacion.get_frame_actual(), (50, 40))
        
        pygame.display.flip()
    
    pygame.quit()
