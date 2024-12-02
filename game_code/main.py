import pygame
import sys
import requests
import json
import time
from player import Player
from enemy import Enemy
from gasoline import Gasoline

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("River Raid")
clock = pygame.time.Clock()

def create_player_interface():
    input_active = False
    player_name = ""
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
                color = color_active if input_active else color_inactive
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        create_player(player_name)
                        return player_name
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        screen.fill((0, 0, 0))
        txt_surface = font.render(player_name, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)
        
def select_player_interface():
    players = get_players()
    selected_option = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(players)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(players)
                elif event.key == pygame.K_RETURN:
                    return players[selected_option]['name']

        screen.fill((0, 0, 0))
        for i, player in enumerate(players):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font.render(player['name'], True, color)
            screen.blit(text, (300, 200 + i * 50))
        pygame.display.flip()

def create_player(name):
    url = "http://localhost:8000/api/players/"
    data = {"name": name}
    print(data)  # Adicione esta linha
    response = requests.post(url, data=data)
    return response.status_code

def send_score(player_name, score):
    player_id = get_player_id(player_name)
    if player_id is None:
        print(f"Player {player_name} not found.")
        return None

    url = "http://localhost:8000/api/scores/"
    data = {"player": player_id, "score": score}
    print(data)  # Adicione esta linha para depuração
    response = requests.post(url, data=data)
    return response.status_code

def get_player_id(player_name):
    url = "http://localhost:8000/api/players/"
    response = requests.get(url)
    players = response.json()
    for player in players:
        if player['name'] == player_name:
            return player['id']
    return None

def get_ranking():
    url = "http://localhost:8000/api/scores/"
    response = requests.get(url)
    scores = response.json()

    # Filtra para obter a maior pontuação de cada jogador
    player_scores = {}
    for score in scores:
        player_id = score['player']
        if player_id not in player_scores or score['score'] > player_scores[player_id]:
            player_scores[player_id] = score['score']

    # Ordena as pontuações do maior para o menor
    sorted_scores = sorted(player_scores.items(), key=lambda item: item[1], reverse=True)

    # Busca os nomes dos jogadores
    players = get_players()
    player_names = {player['id']: player['name'] for player in players}

    # Cria uma lista de tuplas (nome do jogador, pontuação)
    ranking = [(player_names[player_id], score) for player_id, score in sorted_scores]

    return ranking

def draw_ranking(ranking):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    title = font.render("Ranking", True, (255, 255, 255))
    screen.blit(title, (350, 50))

    for i, (name, score) in enumerate(ranking):
        text = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 255))
        screen.blit(text, (300, 100 + i * 40))

    pygame.display.flip()

def get_players():
    url = "http://localhost:8000/api/players/"
    response = requests.get(url)
    return response.json()

def show_menu():
    menu = True
    selected_option = 0
    options = ["Start Game", "Create Player", "Select Player", "View Ranking", "Exit"]

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return "start"
                    elif selected_option == 1:
                        return "create_player"
                    elif selected_option == 2:
                        return "select_player"
                    elif selected_option == 3:
                        return "view_ranking"
                    elif selected_option == 4:
                        pygame.quit()
                        sys.exit()

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (300, 200 + i * 50))
        pygame.display.flip()

def game_loop(player_name):
    score = 0
    start_time = time.time()
    running = True
    gasoline_time = 20  # Duração inicial da gasolina em segundos

    player = Player(400, 500, 'player_sprite.png')
    enemies = pygame.sprite.Group()
    gasolines = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemy_count = 5
    for _ in range(enemy_count):
        enemy = Enemy('enemy_sprite.png')
        enemies.add(enemy)
        all_sprites.add(enemy)

    gasoline_count = 3  # Quantidade inicial de gasolinas no mapa
    for _ in range(gasoline_count):
        gasoline = Gasoline('gas.png')
        gasolines.add(gasoline)
        all_sprites.add(gasoline)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update(all_sprites, bullets)

        # Atualizar pontuação
        if time.time() - start_time >= 5:
            score += 5
            start_time = time.time()

        # Atualizar gasolina
        gasoline_time -= 1 / 60  # Reduzir a gasolina a cada frame (assumindo 60 FPS)
        if gasoline_time <= 0:
            send_score(player_name, score)
            running = False

        # Verificar colisões com gasolina
        if pygame.sprite.spritecollideany(player, gasolines):
            gasoline_time = 20  # Reabastecer a gasolina
            for gasoline in gasolines:
                gasoline.kill()  # Remover a gasolina coletada
            # Adicionar nova gasolina
            for _ in range(gasoline_count):
                gasoline = Gasoline('gas.png')
                gasolines.add(gasoline)
                all_sprites.add(gasoline)

        # Verificar colisões com inimigos
        if pygame.sprite.spritecollideany(player, enemies):
            send_score(player_name, score)
            running = False

        # Verificar colisões de tiros com inimigos
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10  # Adicionar 10 pontos para cada inimigo destruído
            enemy = Enemy('enemy_sprite.png')
            enemies.add(enemy)
            all_sprites.add(enemy)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Desenhar barra de gasolina
        pygame.draw.rect(screen, (255, 0, 0), (10, 50, 200, 20))  # Barra de fundo
        pygame.draw.rect(screen, (0, 255, 0), (10, 50, 200 * (gasoline_time / 20), 20))  # Barra de gasolina

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    # Voltar ao menu após o jogo terminar
    show_menu()



def main():
    player_name = None
    while True:
        action = show_menu()
        if action == "start" and player_name:
            game_loop(player_name)
        elif action == "create_player":
            player_name = create_player_interface()
        elif action == "select_player":
            player_name = select_player_interface()
        elif action == "view_ranking":
            ranking = get_ranking()
            draw_ranking(ranking)
            time.sleep(5)  # Exibe o ranking por 5 segundos antes de voltar ao menu


if __name__ == "__main__":
    main()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    pygame.display.flip()

