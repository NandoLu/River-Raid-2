import pygame
import random

class Gasoline(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 5)

    def update(self, *args, **kwargs):  # Aceitar argumentos adicionais
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 800)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 5)

