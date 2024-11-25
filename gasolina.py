import pygame
import random

class Gasolina:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.speed = 0.5  # Velocidade dos objetos de gasolina

    def update(self):
        self.y += self.speed
        if self.y > 600:  # Remover objeto de gasolina quando sair da tela
            self.y = -50
            self.x = random.randint(50, 7500 - self.rect.width)  # Gerar em uma posição aleatória no topo
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
