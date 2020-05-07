import pygame
import random
import math

# Initialize Game
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 5

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_speed = 3
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_speed = 10
bulletY_change = bullet_speed
bullet_state = "ready"

# background
background = pygame.image.load("background.jpg")


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(firstX, firstY, secondX, secondY):
    distance = math.sqrt(math.pow(firstX - secondX, 2) + (math.pow(firstY - secondY, 2)))
    if distance < 32:
        return True
    return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change += player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_state = "fire"
                    bulletX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # player movement
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for i in range(no_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # score
    show_score(textX, textY)

    player(playerX, playerY)

    pygame.display.update()
