import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_manager=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # Sound manager reference
        self.sound_manager = sound_manager

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls with sound
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.sound_manager:
                self.sound_manager.play('wall_bounce')
                
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if self.sound_manager:
                self.sound_manager.play('wall_bounce')

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check player paddle collision (left side)
        if ball_rect.colliderect(player_rect):
            if self.velocity_x < 0:  # Only bounce if moving toward paddle
                # Calculate hit position for angle
                paddle_center = player_rect.y + player_rect.height / 2
                ball_center = ball_rect.y + ball_rect.height / 2
                relative_intersect = (paddle_center - ball_center) / (player_rect.height / 2)
                
                # Adjust angle
                self.velocity_y = -relative_intersect * 7
                
                # Reverse direction
                self.velocity_x = abs(self.velocity_x)
                
                # Push ball outside paddle
                self.x = player_rect.x + player_rect.width + 1
                
                # Play paddle hit sound
                if self.sound_manager:
                    self.sound_manager.play('paddle_hit')
        
        # Check AI paddle collision (right side)
        elif ball_rect.colliderect(ai_rect):
            if self.velocity_x > 0:  # Only bounce if moving toward paddle
                # Calculate hit position for angle
                paddle_center = ai_rect.y + ai_rect.height / 2
                ball_center = ball_rect.y + ball_rect.height / 2
                relative_intersect = (paddle_center - ball_center) / (ai_rect.height / 2)
                
                # Adjust angle
                self.velocity_y = -relative_intersect * 7
                
                # Reverse direction
                self.velocity_x = -abs(self.velocity_x)
                
                # Push ball outside paddle
                self.x = ai_rect.x - self.width - 1
                
                # Play paddle hit sound
                if self.sound_manager:
                    self.sound_manager.play('paddle_hit')

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)