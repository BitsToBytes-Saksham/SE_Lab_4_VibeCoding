import pygame
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        
        # Initialize sound system
        self.sound_manager = SoundManager()

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, self.sound_manager)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.medium_font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 20)
        
        # Game state
        self.game_over = False
        self.winner = None
        self.winning_score = 5  # Default
        
        # Replay menu state
        self.show_replay_menu = False

    def check_game_over(self):
        """Check if either player has reached the winning score"""
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
            self.show_replay_menu = True
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"
            self.show_replay_menu = True

    def handle_input(self, events=None):
        # Handle M key for sound toggle FIRST (works anytime)
        if events:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        is_enabled = self.sound_manager.toggle()
                        status = "ON" if is_enabled else "OFF"
                        print(f"Sound: {status}")
        
        keys = pygame.key.get_pressed()
        
        # If showing replay menu, handle menu input
        if self.show_replay_menu:
            if keys[pygame.K_3]:
                self.start_new_game(3)
            elif keys[pygame.K_5]:
                self.start_new_game(5)
            elif keys[pygame.K_7]:
                self.start_new_game(7)
            # ESC is handled in main.py for clean exit
            return  # Don't process paddle movement
        
        # If game is over but menu not shown yet, wait
        if self.game_over:
            return
        
        # Normal gameplay controls
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def start_new_game(self, winning_score):
        """Start a new game with specified winning score"""
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.show_replay_menu = False
        
        # Reset positions
        self.ball.reset()
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def update(self):
        # Don't update game logic if game is over
        if self.game_over:
            return
        
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            # Play score sound
            if self.sound_manager:
                self.sound_manager.play('score')
            self.check_game_over()
            if not self.game_over:
                self.ball.reset()
                
        elif self.ball.x >= self.width:
            self.player_score += 1
            # Play score sound
            if self.sound_manager:
                self.sound_manager.play('score')
            self.check_game_over()
            if not self.game_over:
                self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw sound status indicator in bottom corner
        sound_status = "Sound: ON (M to toggle)" if self.sound_manager.enabled else "Sound: OFF (M to toggle)"
        sound_text = self.small_font.render(sound_status, True, GRAY)
        screen.blit(sound_text, (10, self.height - 30))

        # Draw replay menu if game has ended
        if self.show_replay_menu:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Winner announcement
            winner_text = self.big_font.render(f"{self.winner} Wins!", True, YELLOW)
            winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2 - 120))
            screen.blit(winner_text, winner_rect)
            
            # Final score
            score_text = self.font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 - 60))
            screen.blit(score_text, score_rect)
            
            # Replay options title
            replay_title = self.medium_font.render("Play Again?", True, WHITE)
            replay_rect = replay_title.get_rect(center=(self.width//2, self.height//2))
            screen.blit(replay_title, replay_rect)
            
            # Option buttons
            option_y_start = self.height//2 + 60
            option_spacing = 45
            
            best_of_3 = self.font.render("Press 3 - Best of 3", True, WHITE)
            best_of_3_rect = best_of_3.get_rect(center=(self.width//2, option_y_start))
            screen.blit(best_of_3, best_of_3_rect)
            
            best_of_5 = self.font.render("Press 5 - Best of 5", True, WHITE)
            best_of_5_rect = best_of_5.get_rect(center=(self.width//2, option_y_start + option_spacing))
            screen.blit(best_of_5, best_of_5_rect)
            
            best_of_7 = self.font.render("Press 7 - Best of 7", True, WHITE)
            best_of_7_rect = best_of_7.get_rect(center=(self.width//2, option_y_start + option_spacing * 2))
            screen.blit(best_of_7, best_of_7_rect)
            
            # Exit option
            exit_text = self.font.render("Press ESC - Exit Game", True, GRAY)
            exit_rect = exit_text.get_rect(center=(self.width//2, option_y_start + option_spacing * 3 + 20))
            screen.blit(exit_text, exit_rect)