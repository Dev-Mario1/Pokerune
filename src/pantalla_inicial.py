import pygame
import sys

class PantallaTitulo:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.WIDTH = pantalla.get_width()
        self.HEIGHT = pantalla.get_height()
        
        # Colores de los botones
        self.BUTTON_COLOR = (230, 200, 60)
        self.BUTTON_HOVER = (255, 220, 80)
        self.TEXT_COLOR = (0, 0, 0)
        
        # Fuente
        self.font_button = pygame.font.SysFont(None, 32)
        
        # Cargar fondo
        try:
            bg_original = pygame.image.load("Pokerune-main/assets/Fondos/Pantalla de titulo.png")
            self.bg = pygame.transform.scale(bg_original, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Error al cargar la imagen de título: {e}")
            # Crear un fondo de respaldo
            self.bg = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg.fill((20, 20, 50))
            titulo = pygame.font.SysFont(None, 72).render("POKERUNE", True, (255, 255, 255))
            self.bg.blit(titulo, titulo.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 100)))
        
        # Botones
        button_w, button_h = 260, 70
        self.play_rect = pygame.Rect(
            self.WIDTH//2 - button_w//2, 
            self.HEIGHT//2 + 150, 
            button_w, 
            button_h
        )
        self.exit_rect = pygame.Rect(
            self.WIDTH//2 - button_w//2,
            self.play_rect.y + button_h + 20,
            button_w,
            button_h
        )
    
    def draw_button(self, rect, text, mouse_pos):
        """Dibuja un botón y retorna si está hover"""
        hovered = rect.collidepoint(mouse_pos)
        color = self.BUTTON_HOVER if hovered else self.BUTTON_COLOR
        
        pygame.draw.rect(self.pantalla, (0, 0, 0), rect.inflate(6, 6), border_radius=10)
        pygame.draw.rect(self.pantalla, color, rect, border_radius=10)
        
        txt = self.font_button.render(text, True, self.TEXT_COLOR)
        self.pantalla.blit(txt, txt.get_rect(center=rect.center))
        
        return hovered
    
    def actualizar(self, eventos):
        """Actualiza la lógica de la pantalla de título"""
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                print(f"Click detectado en: {evento.pos}")  # Debug
                if self.play_rect.collidepoint(evento.pos):
                    print("Botón PLAY presionado")  # Debug
                    return "jugar"
                if self.exit_rect.collidepoint(evento.pos):
                    print("Botón EXIT presionado")  # Debug
                    return "salir"
            
        
        # Actualizar cursor
        h_play = self.play_rect.collidepoint(mouse_pos)
        h_exit = self.exit_rect.collidepoint(mouse_pos)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if (h_play or h_exit) else pygame.SYSTEM_CURSOR_ARROW
        )
        
        return None
    
    def dibujar(self):
        """Dibuja la pantalla de título"""
        mouse_pos = pygame.mouse.get_pos()
        
        self.pantalla.blit(self.bg, (0, 0))
        self.draw_button(self.play_rect, "PLAY", mouse_pos)
        self.draw_button(self.exit_rect, "EXIT", mouse_pos)
