import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10  # Velocidade do tiro para cima

    def update(self, *args, **kwargs):  # Aceitar argumentos adicionais
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # Remover o tiro se sair da tela
