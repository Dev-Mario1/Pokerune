import pygame
import sys

pygame.init()
pygame.font.init()

# Configuración general
IMAGE_FILENAME = "Pokerune-main/assets/Fondos/Pantalla de titulo.png"
FPS = 60

# Dimensiones deseadas de la ventana
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colores de los botones
BUTTON_COLOR = (230, 200, 60)
BUTTON_HOVER = (255, 220, 80)
TEXT_COLOR = (0, 0, 0)

# Fuente
font_button = pygame.font.SysFont(None, 32)

# Cargar y escalar fondo
try:
    bg_original = pygame.image.load(IMAGE_FILENAME)
    bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    raise

WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("POKERUNE - Title Screen")

clock = pygame.time.Clock()

# Botón Play
button_w, button_h = 260, 70
play_rect = pygame.Rect(WIDTH//2 - button_w//2, HEIGHT//2 + 150, button_w, button_h)

# Botón Exit
exit_rect = pygame.Rect(
    WIDTH//2 - button_w//2,
    play_rect.y + button_h + 20,
    button_w,
    button_h
)

# Función para dibujar botones
def draw_button(surface, rect, text, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    color = BUTTON_HOVER if hovered else BUTTON_COLOR

    pygame.draw.rect(surface, (0, 0, 0), rect.inflate(6, 6), border_radius=10)
    pygame.draw.rect(surface, color, rect, border_radius=10)

    txt = font_button.render(text, True, TEXT_COLOR)
    surface.blit(txt, txt.get_rect(center=rect.center))

    return hovered

# Loop principal
running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_rect.collidepoint(event.pos):
                print("INICIAR JUEGO")
                # Aquí puedes cambiar a la siguiente pantalla
            if exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    screen.blit(bg, (0, 0))

    h_play = draw_button(screen, play_rect, "PLAY", mouse_pos)
    h_exit = draw_button(screen, exit_rect, "EXIT", mouse_pos)

    pygame.mouse.set_cursor(
        pygame.SYSTEM_CURSOR_HAND if (h_play or h_exit) else pygame.SYSTEM_CURSOR_ARROW
    )

    pygame.display.flip()

pygame.quit()