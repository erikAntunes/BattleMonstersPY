import pygame
import random
import sys
import math

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 850, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Monsters")
clock = pygame.time.Clock()

# Cores
BG_COLOR = (200, 230, 200)
BUSH_COLOR = (34, 139, 34)
TEXT_COLOR = (0, 0, 0)
BATTLE_BG = (250, 250, 200)

# Fonte
font = pygame.font.SysFont("arial", 20)

# Definição da classe Monster
class Monster:
    def __init__(self, name, attack, defense, speed):
        self.name = name
        self.stats = {
            "attack": attack,
            "defense": defense,
            "speed": speed
        }
    
    def get_stat(self, stat_name):
        return self.stats.get(stat_name, 0)
    
    def get_info(self):
        return f"{self.name}\nATK: {self.stats['attack']}  DEF: {self.stats['defense']}  SPD:{self.stats['speed']}"

# Cria 10 monstros selvagens pré-definidos
wild_monsters = [
    Monster("Pyrodon", 12, 8, 10),
    Monster("Aquarion", 9, 11, 8),
    Monster("Leafy", 8, 10, 12),
    Monster("Stoneox", 11, 13, 6),
    Monster("Zappy", 13, 7, 14),
    Monster("Frostine", 10, 12, 9),
    Monster("Sandy", 7, 9, 11),
    Monster("Venomix", 12, 8, 13),
    Monster("Mystic", 9, 14, 7),
    Monster("Shadow", 14, 7, 10)
]

# Monstro do jogador (starter) e equipe inicial
player_starter = Monster("Starter", 10, 10, 10)
player_party = [player_starter]

# Criação do sprite do jogador (inspirado em Pokemon Fire Red)
player_sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.rect(player_sprite, (255, 0, 0), (4, 0, 24, 8))         # Chapéu
pygame.draw.rect(player_sprite, (0, 0, 0), (2, 8, 28, 4))           # Aba do chapéu
pygame.draw.rect(player_sprite, (255, 224, 189), (8, 12, 16, 8))      # Rosto
pygame.draw.rect(player_sprite, (50, 50, 240), (8, 20, 16, 12))       # Corpo
pygame.draw.rect(player_sprite, (50, 50, 240), (4, 20, 4, 8))         # Braço esquerdo
pygame.draw.rect(player_sprite, (50, 50, 240), (28, 20, 4, 8))        # Braço direito

# Posição e velocidade do jogador
player_rect = player_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 4

# Define áreas de floresta (áreas onde ocorrerão encontros e que terão árvores animadas)
forest_areas = [
    pygame.Rect(100, 100, 150, 150),
    pygame.Rect(550, 80, 200, 150),
    pygame.Rect(150, 400, 200, 150),
    pygame.Rect(500, 350, 250, 200)
]

# Para cada área de floresta, geramos posições fixas para algumas árvores
forest_trees = []
for area in forest_areas:
    # Geramos 3 árvores por área
    for i in range(3):
        tx = random.randint(area.x, area.x + area.width - 64)
        ty = random.randint(area.y, area.y + area.height - 64)
        forest_trees.append((tx, ty))

# Define áreas de mata onde podem ocorrer encontros
bushes = [
    pygame.Rect(100, 100, 150, 150),
    pygame.Rect(550, 80, 200, 150),
    pygame.Rect(150, 400, 200, 150),
    pygame.Rect(500, 350, 250, 200)
]

# Função para escrever textos na tela
def draw_text(text, pos, color=TEXT_COLOR):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        txt_surface = font.render(line, True, color)
        screen.blit(txt_surface, (pos[0], pos[1] + i * 22))

        # Função que cria um sprite animado inspirado em Pokémon Fire Red para uma árvore.
def get_tree_sprite():
    tree_width, tree_height = 64, 64
    tree = pygame.Surface((tree_width, tree_height), pygame.SRCALPHA)
    # Desenha o tronco da árvore
    pygame.draw.rect(tree, (101, 67, 33), (28, 32, 8, 32))
    # Calcula o balanço (sway) para a folhagem usando função seno
    sway = int(5 * math.sin(pygame.time.get_ticks() / 300))
    # Desenha a camada inferior da folhagem
    pygame.draw.ellipse(tree, (50, 205, 50), (8 + sway, 10, 48, 30))
    # Desenha a camada superior da folhagem
    pygame.draw.ellipse(tree, (34, 139, 34), (16 + sway, 0, 32, 40))
    return tree

# Função que cria um sprite pixel art animado para o monstro,
# fazendo-o lembrar um pássaro, cachorro ou dragão.
def get_monster_sprite(monster):
    sprite = pygame.Surface((64, 64), pygame.SRCALPHA)
    # Mapeia cada monstro para uma categoria
    categories = {
        "Pyrodon": "dragon",
        "Aquarion": "bird",
        "Leafy": "dog",
        "Stoneox": "dragon",
        "Zappy": "dog",
        "Frostine": "bird",
        "Sandy": "dog",
        "Venomix": "dragon",
        "Mystic": "bird",
        "Shadow": "dragon",
        "Starter": "dog"
    }
    category = categories.get(monster.name, "dog")
    # Valor de oscilação para animação (varia entre -5 e 5)
    t = pygame.time.get_ticks() / 200.0
    anim = math.sin(t) * 5

    if category == "dragon":
        if monster.name == "Pyrodon":
            base_color = (255, 100, 0)
        elif monster.name == "Stoneox":
            base_color = (120, 120, 120)
        elif monster.name == "Venomix":
            base_color = (75, 0, 130)
        elif monster.name == "Shadow":
            base_color = (30, 30, 30)
        else:
            base_color = (200, 50, 50)
        pygame.draw.ellipse(sprite, base_color, (12, 20, 40, 24))  # Corpo
        pygame.draw.circle(sprite, base_color, (32, 20), 10)         # Cabeça
        pygame.draw.polygon(sprite, base_color, [(32,10), (32 + int(anim), 0), (42, 10)])  # Horn 1
        pygame.draw.polygon(sprite, base_color, [(32,10), (32 - int(anim), 0), (22, 10)])  # Horn 2
        wing_points = [(20,30), (5, 20 + int(anim)), (20, 40)]      # Asa
        pygame.draw.polygon(sprite, base_color, wing_points)
        tail_start = (52, 32)
        tail_end = (62, 32 + int(anim))
        pygame.draw.line(sprite, base_color, tail_start, tail_end, 4)  # Cauda

    elif category == "bird":
        if monster.name == "Aquarion":
            base_color = (0, 150, 255)
        elif monster.name == "Frostine":
            base_color = (150, 220, 255)
        elif monster.name == "Mystic":
            base_color = (192, 192, 192)
        else:
            base_color = (100, 100, 255)
        pygame.draw.circle(sprite, base_color, (32, 32), 20)         # Corpo
        pygame.draw.circle(sprite, base_color, (32, 18), 10)          # Cabeça
        bico = [(42,18), (42,22), (52,20)]                            # Bico
        pygame.draw.polygon(sprite, (255, 200, 0), bico)
        wing = [(32,32), (20,32 + int(anim)), (32,44)]              # Asa
        wing_color = tuple(max(0, c - 30) for c in base_color)
        pygame.draw.polygon(sprite, wing_color, wing)
        pygame.draw.circle(sprite, (0, 0, 0), (28,16), 2)            # Olho

    elif category == "dog":
        if monster.name == "Leafy":
            base_color = (160, 82, 45)
        elif monster.name == "Zappy":
            base_color = (210, 180, 140)
        elif monster.name == "Sandy":
            base_color = (222, 184, 135)
        elif monster.name == "Starter":
            base_color = (180, 180, 180)
        else:
            base_color = (200, 150, 100)
        pygame.draw.rect(sprite, base_color, (16, 24, 32, 20), border_radius=8)  # Corpo
        pygame.draw.circle(sprite, base_color, (32, 16), 10)                      # Cabeça
        pygame.draw.polygon(sprite, base_color, [(22,10), (18, int(10 + anim)), (26,14)])  # Orelha esquerda
        pygame.draw.polygon(sprite, base_color, [(42,10), (46, int(10 - anim)), (38,14)])  # Orelha direita
        pygame.draw.line(sprite, base_color, (48,34), (58, 34 + int(anim)), 4)     # Rabo
        pygame.draw.circle(sprite, (0,0,0), (28,14), 2)                           # Olho
    return sprite

# Função que desenha um Card para o monstro (usado nas batalhas)
def draw_monster_card(monster, pos):
    card_width, card_height = 200, 200
    card = pygame.Surface((card_width, card_height))
    card.fill((255, 255, 255))
    pygame.draw.rect(card, (0, 0, 0), card.get_rect(), 2)  # Borda preta
    monster_sprite = get_monster_sprite(monster)
    sprite_rect = monster_sprite.get_rect(center=(card_width // 2, card_height // 3))
    card.blit(monster_sprite, sprite_rect)
    name_text = font.render(monster.name, True, (0, 0, 0))
    card.blit(name_text, (card_width // 2 - name_text.get_width() // 2, card_height // 2))
    stat_text = f"ATK:{monster.stats['attack']} DEF:{monster.stats['defense']} SPD:{monster.stats['speed']}"
    stats_surface = font.render(stat_text, True, (0, 0, 0))
    card.blit(stats_surface, (card_width // 2 - stats_surface.get_width() // 2, card_height // 2 + 25))
    screen.blit(card, pos)

# Função para desenhar um Card reduzido (metade do tamanho) para exibir a lista horizontal dos monstros
def draw_monster_card_small(monster, pos):
    card_width, card_height = 75, 100
    card = pygame.Surface((card_width, card_height))
    card.fill((255, 255, 255))
    pygame.draw.rect(card, (0, 0, 0), card.get_rect(), 2)
    monster_sprite = pygame.transform.smoothscale(get_monster_sprite(monster), (32, 32))
    sprite_rect = monster_sprite.get_rect(center=(card_width // 2, card_height // 3))
    card.blit(monster_sprite, sprite_rect)
    # Desenha o nome do monstro centralizado
    name_text = font.render(monster.name, True, (0, 0, 0))
    name_rect = name_text.get_rect(center=(card_width // 2, card_height // 2))
    card.blit(name_text, name_rect)
    # Exibe o valor de ataque com uma margem vertical a partir do nome
    stat_text = f"ATK: {monster.stats['attack']}"
    stats_surface = font.render(stat_text, True, (0, 0, 0))
    stats_rect = stats_surface.get_rect(center=(card_width // 2, name_rect.bottom + 5 + stats_surface.get_height() // 2))
    card.blit(stats_surface, stats_rect)
    screen.blit(card, pos)

# Função que executa a batalha.
def battle(player_monster, wild_monster):
    battle_running = True
    battle_timer = 0
    stat_choice = random.choice(["attack", "defense", "speed"])
    player_value = player_monster.get_stat(stat_choice)
    wild_value = wild_monster.get_stat(stat_choice)
    if player_value == wild_value:
        win = random.choice([True, False])
    else:
        win = player_value > wild_value

    result_displayed = False

    # Centraliza verticalmente os Cards (e define o posicionamento horizontal)
    card_height = 200
    y_center = (HEIGHT - card_height) // 2
    # Jogador à esquerda, monstro selvagem à direita.
    player_card_x = WIDTH // 4 - 75   # 150/2 = 75 (para centralizar o card de 150px de largura)
    wild_card_x = 3 * WIDTH // 4 - 75

    while battle_running:
        dt = clock.tick(60)
        battle_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BATTLE_BG)
        title = font.render("Batalha!", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        # Desenha os Cards centralizados verticalmente
        draw_monster_card(player_monster, (player_card_x, y_center))
        draw_monster_card(wild_monster, (wild_card_x, y_center))
        stat_text = font.render(f"Comparando: {stat_choice.upper()}", True, TEXT_COLOR)
        screen.blit(stat_text, (WIDTH // 2 - stat_text.get_width() // 2, y_center - 40))

        if battle_timer > 2000 and not result_displayed:
            if win:
                result_text = "Você venceu!\nMonstro capturado!"
            else:
                result_text = "Você perdeu a batalha!"
            draw_text(result_text, (WIDTH // 2 - 100, y_center + card_height + 10))
            result_displayed = True

        if battle_timer > 3000:
            battle_running = False

        pygame.display.flip()

    return win

# Variável para evitar encontros consecutivos
encounter_cooldown = 0

# Loop principal do jogo (mapa)
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

       # Mantém o jogador dentro da tela
    player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))
    player_rect.y = max(0, min(HEIGHT - player_rect.height, player_rect.y))

    # Verifica se o jogador está em alguma área de floresta
    in_forest = any(area.collidepoint(player_rect.center) for area in forest_areas)
    if encounter_cooldown <= 0:
        if in_forest and random.random() < 0.01:
            wild_monster = random.choice(wild_monsters)
            result = battle(player_starter, wild_monster)
            if result and wild_monster not in player_party:
                player_party.append(wild_monster)
            encounter_cooldown = 120  # 2 segundos de cooldown
    else:
        encounter_cooldown -= 1

    # Desenha o cenário do mapa com fundo e árvores animadas
    screen.fill(BG_COLOR)
    # Desenha as áreas de floresta (opcional para visualização das áreas)
    for area in forest_areas:
        pygame.draw.rect(screen, (180, 230, 180), area, 2)

    # Desenha as árvores dentro da floresta
    tree_sprite = get_tree_sprite()
    for pos in forest_trees:
        screen.blit(tree_sprite, pos)

    # Desenha o jogador
    screen.blit(player_sprite, player_rect)

    # Exibe a party do jogador na parte inferior
    party_offset_x = 10
    party_offset_y = HEIGHT - 110
    for monster in player_party:
        draw_monster_card_small(monster, (party_offset_x, party_offset_y))
        party_offset_x += 80

    pygame.display.flip()
sys.exit()
