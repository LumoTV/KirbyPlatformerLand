import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Kirby Platformer Land Alpha Version')

# Chargement de l'image de fond avec le sol
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Chargement de l'image de Kirby
kirby_image = pygame.image.load('kirby.png')
kirby_image = pygame.transform.scale(kirby_image, (50, 50))

# Chargement de l'image de l'ennemi
enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

# Position initiale de Kirby
kirby_x = 50
kirby_y = window_height - 150
kirby_speed = 5
jump = False
jump_count = 10  # Augmenter le nombre de sauts

# Position initiale des ennemis et leurs vitesses
enemy1_x, enemy1_y = 600, kirby_y
enemy2_x, enemy2_y = 200, kirby_y
enemy1_speed = 3
enemy2_speed = 2

# Points de vie de Kirby
health = 12
font = pygame.font.Font(None, 36)  # Police et taille de la police pour afficher les PV

# Temps d'invincibilité après avoir été touché
invincibility_time = 2000  # 2 secondes (en millisecondes)
is_invincible = False
last_hit_time = pygame.time.get_ticks()  # Temps du dernier coup reçu

clock = pygame.time.Clock()

# Fonction pour détecter la collision entre Kirby et les ennemis
def check_collision(kirby_x, kirby_y, enemy_x, enemy_y):
    if (kirby_x < enemy_x + enemy_image.get_width() and
        kirby_x + kirby_image.get_width() > enemy_x and
        kirby_y < enemy_y + enemy_image.get_height() and
        kirby_y + kirby_image.get_height() > enemy_y):
        return True
    return False

# Fonction pour afficher l'écran de Game Over
def game_over():
    game_over_text = font.render('Game Over', True, (255, 0, 0))  # Texte en rouge
    text_rect = game_over_text.get_rect()
    text_rect.center = (window_width // 2, window_height // 2)
    window.blit(game_over_text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Pause de 2 secondes avant de quitter
    pygame.quit()
    sys.exit()

# Boucle principale du jeu
running = True
while running:
    window.blit(background_image, (0, 0))  # Affiche l'image de fond avec le sol

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and kirby_x > 0:
        kirby_x -= kirby_speed
    if keys[pygame.K_RIGHT] and kirby_x < window_width - kirby_image.get_width():
        kirby_x += kirby_speed

    # Saut de Kirby
    if jump:
        if jump_count >= -10:  # Maintenir le nombre de sauts à -10
            neg = 1
            if jump_count < 0:
                neg = -1
            kirby_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jump = False
            jump_count = 10

    # Gestion de l'invincibilité
    current_time = pygame.time.get_ticks()
    if is_invincible and current_time - last_hit_time >= invincibility_time:
        is_invincible = False

    # Déplacement des ennemis (de gauche à droite)
    enemy1_x += enemy1_speed
    if enemy1_x >= window_width - enemy_image.get_width() or enemy1_x <= 0:
        enemy1_speed = -enemy1_speed

    enemy2_x += enemy2_speed
    if enemy2_x >= window_width - enemy_image.get_width() or enemy2_x <= 0:
        enemy2_speed = -enemy2_speed

    window.blit(kirby_image, (kirby_x, kirby_y))  # Affiche l'image de Kirby
    window.blit(enemy_image, (enemy1_x, enemy1_y))  # Affiche l'ennemi 1
    window.blit(enemy_image, (enemy2_x, enemy2_y))  # Affiche l'ennemi 2

    # Vérification de la collision entre Kirby et les ennemis
    if not is_invincible and (check_collision(kirby_x, kirby_y, enemy1_x, enemy1_y) or check_collision(kirby_x, kirby_y, enemy2_x, enemy2_y)):
        health -= 1
        print("Kirby a été touché ! Points de vie restants :", health)
        # Définit Kirby comme invincible et met à jour le temps du dernier coup reçu
        is_invincible = True
        last_hit_time = current_time

        if health <= 0:
            game_over()

    # Affichage des points de vie de Kirby en bas de la fenêtre en noir
    health_text = font.render(f'PV: {health}', True, (0, 0, 0))  # Couleur noire
    text_rect = health_text.get_rect()
    text_rect.bottomleft = (10, window_height - 10)
    window.blit(health_text, text_rect)  # Affiche le texte des PV en bas à gauche

    pygame.display.update()
    clock.tick(60)  # Limite le jeu à 60 FPS

pygame.quit()
sys.exit()
