import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_shot = pygame.time.get_ticks()  # Tempo do último tiro

    def update(self, all_sprites, bullets):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Lógica de tiro
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > 1000:  # Intervalo de 1 segundo
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, 'fire.png')
            all_sprites.add(bullet)
            bullets.add(bullet)
