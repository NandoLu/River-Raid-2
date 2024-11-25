import pygame

movement_speed = 0.6  # Diminuir a velocidade pela metade

class Player:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= movement_speed
        if keys[pygame.K_d]:
            self.x += movement_speed

        # Limitar o movimento do jogador dentro das bordas
        if self.x < 50:
            self.x = 50
        if self.x > 750 - self.rect.width:
            self.x = 750 - self.rect.width

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
