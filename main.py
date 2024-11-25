import pygame
import sys
import random
from player import Player
from inimigo import Inimigo
from gasolina import Gasolina

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("River Raid")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Fonte
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Função para desenhar o texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Função para a tela de início
def main_menu():
    click = False
    while True:
        screen.fill(green)
        draw_text('River Raid', font, black, screen, screen_width // 2, screen_height // 4)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()

        pygame.draw.rect(screen, black, button_1)
        draw_text('Iniciar', font, white, screen, screen_width // 2, screen_height // 2 + 25)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

# Função principal do jogo
def game():
    player = Player("images/player.png", screen_width // 2, screen_height - 100)
    inimigos = []
    gasolinas = []
    inimigo_timer = 0
    gasolina_timer = 0
    gasolina = 60 * 60  # 60 segundos em frames (60 FPS)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Atualizar o jogador
        player.update()

        # Gerar inimigos aleatoriamente
        inimigo_timer += 1
        if inimigo_timer > random.randint(30, 100):
            inimigo_timer = 0
            inimigos.append(Inimigo("images/barco.png", random.randint(50, screen_width - 100), -50))

        # Gerar objetos de gasolina aleatoriamente
        gasolina_timer += 1
        if gasolina_timer > random.randint(300, 600):
            gasolina_timer = 0
            gasolinas.append(Gasolina("images/gasolina.png", random.randint(50, screen_width - 100), -50))

        # Atualizar inimigos
        for inimigo in inimigos:
            inimigo.update()
            if player.rect.colliderect(inimigo.rect):
                game_over()

        # Atualizar objetos de gasolina
        for gasolina_obj in gasolinas:
            gasolina_obj.update()
            if player.rect.colliderect(gasolina_obj.rect):
                gasolina = 60 * 60  # Reabastecer gasolina
                gasolinas.remove(gasolina_obj)

        # Atualizar gasolina
        gasolina -= 1
        if gasolina <= 0:
            game_over()

        # Desenhar na tela
        screen.fill(white)
        pygame.draw.rect(screen, blue, (50, 0, screen_width - 100, screen_height))  # Área azul
        player.draw(screen)
        for inimigo in inimigos:
            inimigo.draw(screen)
        for gasolina_obj in gasolinas:
            gasolina_obj.draw(screen)

        # Desenhar bordas físicas
        pygame.draw.rect(screen, green, (0, 0, 50, screen_height))  # Borda esquerda
        pygame.draw.rect(screen, green, (screen_width - 50, 0, 50, screen_height))  # Borda direita

        # Desenhar barra de gasolina
        pygame.draw.rect(screen, red, (10, 10, 200, 20))
        pygame.draw.rect(screen, green, (10, 10, gasolina * 200 // (60 * 60), 20))
        draw_text(f'Gasolina: {gasolina // 60}', small_font, black, screen, 110, 20)

        pygame.display.update()

def game_over():
    screen.fill(red)
    draw_text('Game Over', font, black, screen, screen_width // 2, screen_height // 2)
    pygame.display.update()
    pygame.time.wait(2000)
    main_menu()

# Iniciar o jogo
if __name__ == "__main__":
    main_menu()
