import pygame
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 800))
mixer.music.load('l.ogg')
mixer.music.play(-1)
pygame.display.set_caption("Space Invader")
bg = pygame.image.load('background.png')
icon = pygame.image.load('Untitled.png')
pygame.display.set_icon(icon)
playerImg = pygame.image.load('d.png')
playerX = 340
playerY = 480
bx = 0
by = 12
bt_state = "ready"
over_font = pygame.font.Font('freesansbold.ttf', 64)
X = 0
Y = 0
btImg = pygame.image.load('bullet.png')
goImg = pygame.image.load('gop.png')
btY = playerY
btX = 0
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
enemyImg = []
enemyY = []
enemyX = []
ex = []
ey = []
ne = 6
for i in range(ne):
    enemyImg.append(pygame.image.load('e.png'))
    enemyY.append(random.randint(50, 150))
    enemyX.append(random.randint(0, 799))
    ex.append(10)
    ey.append(80)


def ss(x, y):
    scores = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(scores, (x, y))


def fire_bt(x, y):
    global bt_state
    bt_state = "fire"
    screen.blit(btImg, (x + 16, y - 20))
    clock.tick(100)
    pygame.display.update()


def game_over_text():
    screen.blit(goImg, (30, 50))
    mixer.music.load('death.ogg')

    mixer.music.play()


def exp(enemyX, enemyY, playerX, playerY):
    dist = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if dist < 27:
        return True
    else:
        return False


def col(enemyX, enemyY, btX, btY):
    dist = math.sqrt((math.pow(enemyX - btX, 2)) + (math.pow(enemyY - btY, 2)))
    if dist < 27:
        return True
    else:
        return False


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


running = True
while running:

    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))
    playerX += X
    playerY += Y

    player(playerX, playerY)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X = -10
            if event.key == pygame.K_RIGHT:
                X = +10
            if event.key == pygame.K_UP:
                Y = -10
            if event.key == pygame.K_DOWN:
                Y = +10
            if event.key == pygame.K_SPACE:
                if bt_state is "ready":
                    btX = playerX
                    fire_bt(btX, btY)
                    bts = mixer.Sound('fire_s.ogg')
                    bts.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                Y = 0
    if playerX <= 0:
        playerX = 0
    elif playerX >= 825:
        playerX = 825
    if playerY <= 0:
        playerY = 0
    elif playerY >= 700:
        playerY = 700

    for i in range(ne):
        # game over
        if enemyY[i] > 755:
            for j in range(ne):
                enemyY[j] = -20000
                game_over_text()

        enemyX[i] += ex[i]

        if enemyX[i] <= 0:
            ex[i] = 4
            enemyY[i] += ey[i]
        elif enemyX[i] >= 800:
            ex[i] = -4
            enemyY[i] += ey[i]

        cols = col(enemyX[i], enemyY[i], btX, btY)
        if cols:
            btY = playerY
            bt_state = "ready"
            pts = mixer.Sound('exe.ogg')
            pts.play()
            enemyY[i] = random.randint(50, 150)
            enemyX[i] = random.randint(0, 800)
            score += 1

        enemy(enemyX[i], enemyY[i], i)
        cols = col(enemyX[i], enemyY[i], btX, btY)
        expc = exp(enemyX[i], enemyY[i], playerX, playerY)
        if expc:
            for j in range(ne):
                enemyY[j] = -20000

                game_over_text()

    if btY <= -100:
        btY = playerY
        bt_state = "ready"
    if bt_state is "fire":
        fire_bt(btX, btY)
        btY -= by
    ss(textX, textY)

    pygame.display.update()
