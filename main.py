import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Initialize mixer for sound support
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        
        # Collect events
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # Add ESC key handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Pass events to engine for proper key handling
        engine.handle_input(events)
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()