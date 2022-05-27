from distutils.ccompiler import show_compilers
from os import X_OK
from re import X
import pygame
from pygame import *
import random
import time

pygame.init()
clock = pygame.time.Clock()

screenWidth = 1200
screenHeight = 700

font = pygame.font.SysFont('Bauhaus 93', 60)

white = (255, 255, 255)

gameOver = False
tileSize = 50
fps = 60
movingLeft = False
movingRight = False
movingUp = False
movingDown = False
interact = False
shoot = False
pause = False
accessedShop = False
bulletUpgrade1 = False
bulletUpgrade2 = False
bulletUpgrade3 = False
totalCoins = 0
delay = 0.5
timer = False
buyU1 = False
buyU2 = False
buyU3 = False
floor = 'None'
room = 'None'
mainMenu = True
overallKills = 0
overallCoins = 0
overallDeaths = 0
HighscoreKills = 0
statsMenu = False
settingsMenu = False
creditsMenu = False
tutorialImgs = False
WHITE = (255, 255, 255)

tileImg = pygame.image.load('tile.png')
bgImg = pygame.image.load('black.jpg')
blackBG = pygame.transform.scale(bgImg, (1200, 700))
tutorial = pygame.image.load('tutorial.png')
coin = pygame.image.load('coin.png')
coinImg = pygame.transform.scale(coin, (50, 50))
chestCoin = pygame.transform.scale(coin, (25, 25))
health = pygame.image.load('life.png')
healthImg = pygame.transform.scale(health, (50, 50))
chestHealth = pygame.transform.scale(health, (25, 25))
enemyImg = pygame.image.load('enemy1.png')
enemyImg = pygame.transform.scale(enemyImg, (50, 50))
exitShopBtn = pygame.image.load('exitShop.png')
exitShopBtn = pygame.transform.scale(exitShopBtn, (50, 50))
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (25, 25))
skullImg = pygame.image.load('skullImg.png')
skullImg = pygame.transform.scale(skullImg, (50, 50))
pwr1 = pygame.image.load('powerUp1.png')
pwr2 = pygame.image.load('powerUp2.png')
pwr3 = pygame.image.load('powerUp3.png')
pwr1Shop = pygame.transform.scale(pwr1, (100, 100))
pwr2Shop = pygame.transform.scale(pwr2, (100, 100))
pwr3Shop = pygame.transform.scale(pwr3, (100, 100))
pwr1 = pygame.transform.scale(pwr1, (25, 25))
pwr2 = pygame.transform.scale(pwr2, (25, 25))
pwr3 = pygame.transform.scale(pwr3, (25, 25))
attackTutorial = pygame.image.load('attackTutorial.png')
moveTutorial = pygame.image.load('moveTutorial.png')
interactTutorial = pygame.image.load('interactTutorial.png')
spaceTutorial = pygame.image.load('spaceTutorial.png')
eTutorial = pygame.image.load('eTutorial.png')
wasdTutorial = pygame.image.load('wasdTutorial.png')
attackTutorial = pygame.transform.scale(attackTutorial, (100, 100))
moveTutorial = pygame.transform.scale(moveTutorial, (100, 100))
interactTutorial = pygame.transform.scale(interactTutorial, (100, 100))
eTutorial = pygame.transform.scale(eTutorial, (100, 100))
spaceTutorial = pygame.transform.scale(spaceTutorial, (100, 100))
wasdTutorial = pygame.transform.scale(wasdTutorial, (100, 100))
newRunImg = pygame.image.load('newRun.png')
settingsImg = pygame.image.load('settings.png')
statsImg = pygame.image.load('stats.png')
creditsImg = pygame.image.load('credits.png')
newRunImg = pygame.transform.scale(newRunImg, (200, 200))
settingsImg = pygame.transform.scale(settingsImg, (200, 200))
statsImg = pygame.transform.scale(statsImg, (200, 200))
creditsImg = pygame.transform.scale(creditsImg, (200, 200))
returnImg = pygame.image.load('returnImg.png')
returnImg = pygame.transform.scale(returnImg, (100, 100))
resetImg = pygame.image.load('resetImg.png')
resetImg = pygame.transform.scale(resetImg, (100, 50))
menuBtnImg = pygame.image.load('menuBtnImg.png')
menuBtnImg = pygame.transform.scale(menuBtnImg, (100, 50))


screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Adventure Game')


class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        global shopBtns
        shopBtns = False

    def drawShopBtns(self):
        if shopBtns == True:

            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, self.rect)

            return action

        else:
            pass

    def draw(self):

        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        self.draw_point(screen, self.rect.topleft, self.collision[0])
        self.draw_point(screen, self.rect.topright, self.collision[1])
        self.draw_point(screen, self.rect.bottomleft, self.collision[2])
        self.draw_point(screen, self.rect.bottomright, self.collision[3])

        self.draw_point(screen, self.rect.midleft, self.collision[4])
        self.draw_point(screen, self.rect.midright, self.collision[5])
        self.draw_point(screen, self.rect.midtop, self.collision[6])
        self.draw_point(screen, self.rect.midbottom, self.collision[7])

        self.draw_point(screen, self.rect.center, self.collision[8])

    def update(self):
        global timer
        if pause == False:
            dx = 0
            dy = 0
            if movingLeft == True:

                dx -= 2
                self.direction = "Left"
                img = pygame.image.load('ghostLeft.png')
                self.image = pygame.transform.scale(img, (40, 80))

            if movingRight == True:

                dx += 2
                self.direction = "Right"
                img = pygame.image.load('ghostRight.png')
                self.image = pygame.transform.scale(img, (40, 80))

            if movingUp == True:

                dy -= 2
                self.direction = "Up"
                img = pygame.image.load('ghostUp.png')
                self.image = pygame.transform.scale(img, (40, 80))

            if movingDown == True:

                dy += 2
                self.direction = "Down"
                img = pygame.image.load('ghostDown.png')
                self.image = pygame.transform.scale(img, (40, 80))

            for tile in room.tileList:

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = 0

            for enemy in enemyGroup:
                if pygame.sprite.spritecollide(enemy, playerGroup, False):

                    self.time = time.time()
                    timer = True
                    if self.invincible == False:
                        self.health -= 1
                    self.invincible = True
                    enemy.playerCollide = True

                    self.collision[0] = enemy.rect.collidepoint(self.rect.topleft)
                    self.collision[1] = enemy.rect.collidepoint(self.rect.topright)
                    self.collision[2] = enemy.rect.collidepoint(self.rect.bottomleft)
                    self.collision[3] = enemy.rect.collidepoint(self.rect.bottomright)

                    self.collision[4] = enemy.rect.collidepoint(self.rect.midleft)
                    self.collision[5] = enemy.rect.collidepoint(self.rect.midright)
                    self.collision[6] = enemy.rect.collidepoint(self.rect.midtop)
                    self.collision[7] = enemy.rect.collidepoint(self.rect.midbottom)

                    self.collision[8] = enemy.rect.collidepoint(self.rect.center)

                    if self.collision[6]:
                        enemy.update(0.000000001, -1)
                        self.collisionx = 0.000000001
                        self.collisiony = -1

                    if self.collision[4] or self.collision[0] or self.collision[2]:
                        enemy.update(-1, 0.000000001)
                        self.collisionx = -1
                        self.collisiony = 0.000000001

                    if self.collision[7]:
                        enemy.update(0.000000001, 1)
                        self.collisionx = 0.000000001
                        self.collisiony = 1

                    if self.collision[5] or self.collision[1] or self.collision[3]:
                        enemy.update(1, 0.000000001)
                        self.collisionx = 1
                        self.collisiony = 0.000000001

            if pygame.sprite.spritecollide(self, merchantGroup, False):
                self.accessMerchant = True

            else:
                self.accessMerchant = False

            if self.rect.right > screenWidth:
                self.rect.right = screenWidth
                dx = 0

            self.rect.x += dx
            self.rect.y += dy

            screen.blit(self.image, self.rect)

    def reset(self, x, y):
        global totalCoins

        img = pygame.image.load('ghost1.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision = [False] * 9
        self.direction = "None"
        self.accessMerchant = False
        self.invincible = False
        self.collisionx = 1
        self.collisiony = 1
        self.health = 3
        self.time = 0
        self.highscoreKills = 0
        totalCoins = 0

    def action(self, x, y, health, coins):
        img = pygame.image.load('ghost1.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision = [False] * 9
        self.direction = "None"
        self.accessMerchant = False
        self.invincible = False
        self.collisionx = 1
        self.collisiony = 1
        self.health = health
        self.coins = coins
        self.time = 0


class Room():

    def __init__(self, data):

        self.tileList = []
        self.enemyTotal = 0
        self.merchantTotal = 0
        self.chestTotal = 0

        wallLeft = pygame.image.load('wallLeft.png')
        wallRight = pygame.image.load('wallRight.png')
        topWall = pygame.image.load('topWall.png')
        bottomWall = pygame.image.load('bottomWall.png')
        topRightWall = pygame.image.load('topRightWall.png')
        topLeftWall = pygame.image.load('topLeftWall.png')
        bottomLeftWall = pygame.image.load('bottomLeftWall.png')
        bottomRightWall = pygame.image.load('bottomRightWall.png')

        rowCount = 0
        for row in data:

            colCount = 0
            for tile in row:

                if tile == 2:
                    img = pygame.transform.scale(
                        wallLeft, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 3:
                    img = pygame.transform.scale(
                        bottomWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 4:
                    img = pygame.transform.scale(topWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 5:
                    img = pygame.transform.scale(
                        wallRight, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 6:
                    img = pygame.transform.scale(
                        topLeftWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 7:
                    img = pygame.transform.scale(
                        bottomLeftWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 8:
                    img = pygame.transform.scale(
                        topRightWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 9:
                    img = pygame.transform.scale(
                        bottomRightWall, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)

                if tile == 12:
                    global chest
                    chest = Chest(colCount * tileSize, rowCount * tileSize)
                    chestGroup.add(chest)
                    self.chestTotal += 1

                if tile == 13:
                    global enemyWidth
                    global enemyHeight
                    global enemyRect
                    global enemy
                    enemy_img = enemyImg
                    enemyRect = enemy_img.get_rect()
                    enemyRect.x = colCount * tileSize
                    enemyRect.y = rowCount * tileSize
                    enemyWidth = enemy_img.get_width()
                    enemyHeight = enemy_img.get_height()
                    enemy = Enemy(enemyRect.x, enemyRect.y, enemy_img)
                    enemyGroup.add(enemy)
                    self.enemyTotal += 1

                if tile == 14:
                    global merchant
                    merchant = Merchant(colCount * tileSize, rowCount * tileSize)
                    merchantGroup.add(merchant)
                    self.merchantTotal += 1

                colCount += 1
            rowCount += 1
    def draw(self):

        for tile in self.tileList:
            screen.blit(tile[0], tile[1])


class Floor():

    def __init__(self, data):

        self.tileList = []

        rowCount = 0
        for row in data:

            colCount = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(tileImg, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)
                if tile == 0:
                    img = pygame.transform.scale(bgImg, (tileSize, tileSize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tileSize
                    imgRect.y = rowCount * tileSize
                    tile = (img, imgRect)
                    self.tileList.append(tile)
                colCount += 1
            rowCount += 1

    def draw(self):

        for tile in self.tileList:
            screen.blit(tile[0], tile[1])

def RandRoom():
    global floor
    global room
    newRoomData = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 6, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 8, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Merchant/Chest', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [1, 7, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 9, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

    newFloorData = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

    for i1, subList in enumerate(newRoomData):
        for i2, item in enumerate(subList):
            if item == 'Merchant/Chest':
                merchantChestChance = random.randint(1, 4)

                if merchantChestChance == 1:
                    newRoomData[i1][i2] = 14

                if merchantChestChance == 2 or merchantChestChance == 3:
                    newRoomData[i1][i2] = 12
            
            if item == 0:

                if buyU1 == False and buyU2 == False and buyU3 == False:
                    enemyChance = random.randint(1, 40)

                if buyU1:
                    enemyChance = random.randint(1, 35)

                if buyU2:
                    enemyChance = random.randint(1, 30)

                if buyU3:
                    enemyChance = random.randint(1, 25)

                if enemyChance == 1:
                    newRoomData[i1][i2] = 13

    floor = Floor(newFloorData)
    room = Room(newRoomData)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):

        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 10
        self.moveLRUD = "None"
        self.hit = False
        if direction == "Left":
            self.moveLRUD = "Left"
        if direction == "Right":
            self.moveLRUD = "Right"
        if direction == "Up":
            self.moveLRUD = "Up"
        if direction == "Down":
            self.moveLRUD = "Down"

    def update(self):

        if pause == False:
            if self.moveLRUD == "Up":
                self.rect.y = self.rect.y - self.speed

            if self.moveLRUD == "Down":
                self.rect.y = self.rect.y + self.speed

            if self.moveLRUD == "Left":
                self.rect.x = self.rect.x - self.speed

            if self.moveLRUD == "Right":
                self.rect.x = self.rect.x + self.speed

            for tile in room.tileList:

                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    self.kill()

                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    self.kill()

            if self.rect.x >= 1200 or self.rect.y >= 700 or self.rect.x <= 0 or self.rect.y <= 0:
                self.kill()

            if self.hit == True:
                self.kill()
                self.hit = False
            if bulletUpgrade1 == True:
                self.image = pwr1
            if bulletUpgrade2 == True:
                self.image = pwr2
            if bulletUpgrade3 == True:
                self.image = pwr3

        else:
            pass


class Chest(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.reset(x, y)

    def update(self):
        global totalCoins
        global overallCoins

        img = pygame.image.load('chestOpened.png')
        self.image = pygame.transform.scale(img, (tileSize, tileSize))
        self.opened = True
        if player.health >= 3:
            self.item = random.randint(1, 2)

        elif player.health < 3:
            self.item = random.randint(1, 3)

        if self.item == 1:
            totalCoins += 1
            overallCoins += 1

        if self.item == 2:
            totalCoins += 2
            overallCoins += 2
        
        if self.item == 3:
            player.health += 1

    def reset(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('closedChest.png')
        self.image = pygame.transform.scale(img, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.opened = False
        self.item = 0


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.width = enemyWidth
        self.height = enemyHeight
        self.rect = enemyRect
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.moved = 0
        self.health = 1
        self.alive = True
        self.wallCollide = False
        self.playerCollide = False
        self.hit = False

    def update(self, x, y):
        global hit
        if pause == False:

            for tile in room.tileList:

                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    self.wallCollide = True

                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    self.wallCollide = True
                        
            if self.playerCollide == False:
                directionVector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
                directionVector.normalize()
                directionVector.scale_to_length(self.speed)
                self.rect.move_ip(directionVector)

            if self.playerCollide == True:
                directionVector = pygame.math.Vector2(x, y)
                directionVector.normalize()
                directionVector.scale_to_length(self.speed * 2)
                self.rect.move_ip(directionVector)
                self.moved += 1

                if self.moved > 50:
                    self.moved = 0
                    self.playerCollide = False

            if self.hit == True:
                global overallKills
                self.alive = False
                overallKills += 1
                player.highscoreKills += 1

            if self.wallCollide == True:
                self.moved = 50
                self.wallCollide = False

class Merchant(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagesRight = []
        self.imagesLeft = []
        self.index = 0
        for num in range(1, 7):
            imgRight = pygame.image.load(f"merchant{num}.png")
            imgRight = pygame.transform.scale(imgRight, (46, 77))
            imgLeft = pygame.transform.flip(imgRight, True, False)
            self.imagesRight.append(imgRight)
            self.imagesLeft.append(imgLeft)
        self.image = self.imagesRight[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moveDirection = 1
        self.moveCounter = 0
        self.direction = 1
        self.turnCounter = 0

    def update(self):

        if pause == False:

            walkCoolDown = 10
            self.rect.x += self.moveDirection
            self.moveCounter += 1
            self.turnCounter += 1
            if self.moveCounter > walkCoolDown:
                self.moveCounter = 0
                self.index += 1
                if self.index >= len(self.imagesRight):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.imagesRight[self.index]
                if self.direction == -1:
                    self.image = self.imagesLeft[self.index]
            if abs(self.turnCounter) > 100:
                self.moveDirection *= -1
                self.moveCounter *= -1
                self.direction *= -1
                self.turnCounter *= -1


class MerchantInv():

    def __init__(self):
        global exitShop
        global buyHeart
        global Powerup1
        global Powerup2
        global Powerup3
        global shopBtns
        shopBtns = True
        shopHeart = pygame.transform.scale(healthImg, (150, 150))
        exitShop = Button(800, 100, exitShopBtn)
        self.exitShop = exitShop
        buyHeart = Button(75, 100, shopHeart)
        self.buyHeart = buyHeart
        if buyU1 == False:
            Powerup1 = Button(100, 250, pwr1Shop)
            self.Powerup1 = Powerup1
        if buyU2 == False:
            Powerup2 = Button(100, 400, pwr2Shop)
            self.Powerup2 = Powerup2
        if buyU3 == False:
            Powerup3 = Button(100, 550, pwr3Shop)
            self.Powerup3 = Powerup3

    def remove():
        global shopBtns
        shopBtns = False


def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))


def shopText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))


enemyGroup = pygame.sprite.Group()
chestGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
merchantGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()

player = Player(int(screenWidth / 2), int(screenHeight / 2))
playerGroup.add(player)

startRoomData = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 2, 0, 0, 0, 0, 12, 0, 0, 0, 0, 12, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 7, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

startFloorData = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

room = Room(startRoomData)
floor = Floor(startFloorData)

newRunBtn = Button(300, 100, newRunImg)
statsBtn = Button(600, 100, statsImg)
settingsBtn = Button(300, 400, settingsImg)
creditsBtn = Button(600, 400, creditsImg)
returnBtn = Button(800, 100, returnImg)
resetBtn = Button(screenWidth / 2 - 200, screenHeight / 2, resetImg)
menuBtn = Button(screenWidth / 2 + 100, screenHeight / 2, menuBtnImg)

run = True
while run:

    clock.tick(fps)

    if mainMenu == True:
        screen.blit(blackBG, (0, 0))

        if newRunBtn.draw():
            player.reset(int(screenWidth / 2), int(screenHeight / 2))
            room = Room(startRoomData)
            floor = Floor(startFloorData)
            room.draw()
            floor.draw()
            for enemy in enemyGroup:
                enemy.kill()
            for merchant in merchantGroup:
                merchant.kill()
            for chest in chestGroup:
                chest.kill()
            gameOver = False
            mainMenu = False
            tutorialImgs = True

        if statsBtn.draw():
            statsMenu = True
            mainMenu = False

        if settingsBtn.draw():
            settingsMenu = True
            mainMenu = False

        if creditsBtn.draw():
            creditsMenu = True
            mainMenu = False

    if statsMenu == True:
        screen.blit(blackBG, (0, 0))
        drawText("Total Kills: " + str(overallKills), font, white, 150, 150)
        drawText("Total Coins Collected: " + str(overallCoins), font, white, 150, 300)
        drawText("Total Deaths: " + str(overallDeaths), font, white, 150, 450)
        drawText("Kills Highscore: " + str(HighscoreKills), font, white, 150, 600)
        screen.blit(enemyImg, (75, 157))
        screen.blit(coinImg, (75, 307))
        screen.blit(skullImg, (75, 457))
        if returnBtn.draw():
            statsMenu = False
            mainMenu = True

    if creditsMenu == True:
        screen.blit(blackBG, (0, 0))
        drawText("Credits", font, white, (screenWidth / 2) - 100, 100)
        drawText("Programmer: Jacob Matte-Kubecka", font, white, 150, 300)
        drawText("Designer: Jacob Matte-Kubecka", font, white, 150, 500)

        if returnBtn.draw():
            creditsMenu = False
            mainMenu = True

    if settingsMenu == True:
        screen.blit(blackBG, (0, 0))
        drawText("Empty Settings Menu :)", font, white, (screenWidth / 2) - 300, 300)

        if returnBtn.draw():
            settingsMenu = False
            mainMenu = True

    if mainMenu == False and statsMenu == False and settingsMenu == False and creditsMenu == False:

        if player.rect.right >= 1199:
            tutorialImgs = False

            player.action(50, int(screenHeight / 2), player.health, totalCoins)
            for enemy in enemyGroup:
                enemy.kill()
            for merchant in merchantGroup:
                merchant.kill()
            for chest in chestGroup:
                chest.kill()
            RandRoom()

        if player.rect.bottom >= 699:
            tutorialImgs = False

            player.action(int(screenWidth / 2), 50, player.health, totalCoins)
            for enemy in enemyGroup:
                enemy.kill()
            for merchant in merchantGroup:
                merchant.kill()
            for chest in chestGroup:
                chest.kill()
            RandRoom()

        if player.rect.top <= 1:
            tutorialImgs = False

            player.action(int(screenWidth / 2), 650, player.health, totalCoins)
            for enemy in enemyGroup:
                enemy.kill()
            for merchant in merchantGroup:
                merchant.kill()
            for chest in chestGroup:
                chest.kill()
            RandRoom()

        if player.rect.left <= 1:
            tutorialImgs = False

            player.action(1150, int(screenHeight / 2), player.health, totalCoins)
            for enemy in enemyGroup:
                enemy.kill()
            for merchant in merchantGroup:
                merchant.kill()
            for chest in chestGroup:
                chest.kill()
            RandRoom()

        if timer:

            if time.time() - player.time >= delay:
                player.invincible = False
                player.time = 0

        floor.draw()
        room.draw()

        if tutorialImgs == True:
            screen.blit(moveTutorial, (screenWidth / 2 - 250, screenHeight / 2 - 150))
            screen.blit(wasdTutorial, (screenWidth / 2 - 250, screenHeight / 2))
            screen.blit(attackTutorial, (screenWidth / 2 - 50, screenHeight / 2 - 150))
            screen.blit(spaceTutorial, (screenWidth / 2 - 50, screenHeight / 2))
            screen.blit(interactTutorial, (screenWidth / 2 + 150, screenHeight / 2 - 150))
            screen.blit(eTutorial, (screenWidth / 2 + 150, screenHeight / 2))

        if room.chestTotal > 0:

            if chest.opened == True:

                if chest.item == 1:
                    screen.blit(chestCoin, (chest.rect.x + 12, chest.rect.y - 30))

                if chest.item == 2:
                    screen.blit(chestCoin, (chest.rect.x + 12, chest.rect.y - 30))

                if chest.item == 3:
                    screen.blit(chestHealth, (chest.rect.x + 12, chest.rect.y - 30))

        chestGroup.draw(screen)
        merchantGroup.draw(screen)

        if gameOver == False:

            if room.merchantTotal > 0:
                merchant.update()
            player.update()

            if accessedShop == True:
                global shopBtns
                shopBtns = True

                screen.blit(blackBG, (0, 0))
                drawText("+1 Heart", font, white, 250, 112)
                drawText("Cost: 3", font, white, 250, 165)
                screen.blit(coinImg, (450, 175))

                if exitShop.drawShopBtns():
                    pause = False
                    accessedShop = False
                    MerchantInv.remove()

                if buyHeart.drawShopBtns():
                    if totalCoins >= 3:
                        totalCoins -= 3
                        player.health += 1

                if buyU1 == True:
                    drawText("Bought!", font, white, 250, 270)
                    screen.blit(pwr1Shop, (100, 250))

                if buyU2 == True:
                    drawText("Bought!", font, white, 250, 415)
                    screen.blit(pwr2Shop, (100, 400))

                if buyU3 == True:
                    drawText("Bought!", font, white, 250, 570)
                    screen.blit(pwr3Shop, (100, 550))

                if buyU1 == False:
                    if Powerup1.drawShopBtns():
                        if totalCoins >= 5:
                            totalCoins -= 5
                            bulletUpgrade1 = True
                            buyU1 = True
                    drawText("+1 Max Shots", font, white, 250, 250)
                    drawText("Cost: 5", font, white, 250, 303)
                    screen.blit(coinImg, (450, 313))

                if buyU2 == False:
                    if Powerup2.drawShopBtns():
                        if totalCoins >= 10:
                            totalCoins -= 10
                            bulletUpgrade2 = True
                            buyU2 = True
                    drawText("+1 Max Shots", font, white, 250, 395)
                    drawText("Cost: 10", font, white, 250, 448)
                    screen.blit(coinImg, (480, 458))

                if buyU3 == False:
                    if Powerup3.drawShopBtns():
                        if totalCoins >= 15:
                            totalCoins -= 15
                            bulletUpgrade3 = True
                            buyU3 = True
                    drawText("+1 Max Shots", font, white, 250, 550)
                    drawText("Cost: 15", font, white, 250, 603)
                    screen.blit(coinImg, (480, 613))

            if shoot == True and accessedShop == False:

                if player.direction == "Up":
                    bullet = Bullet(player.rect.centerx, player.rect.centery - 25, player.direction)
                    bulletGroup.add(bullet)
                    shoot = False

                if player.direction == "Down":
                    bullet = Bullet(player.rect.centerx, player.rect.centery + 12, player.direction)
                    bulletGroup.add(bullet)
                    shoot = False

                if player.direction == "Left":
                    bullet = Bullet(player.rect.centerx, player.rect.centery - 10, player.direction)
                    bulletGroup.add(bullet)
                    shoot = False

                if player.direction == "Right":
                    bullet = Bullet(player.rect.centerx, player.rect.centery - 10, player.direction)
                    bulletGroup.add(bullet)
                    shoot = False

            if pause == False:

                for enemy in enemyGroup:
                    enemyGroup.draw(screen)
                    enemy.update(player.collisionx, player.collisiony)
                    if pygame.sprite.spritecollide(enemy, bulletGroup, False):
                        bullet.hit = True
                        enemy.hit = True
                    if enemy.alive == False:
                        enemy.kill()


        bulletGroup.update()
        bulletGroup.draw(screen)

        screen.blit(coinImg, (80, 18))
        drawText(str(totalCoins), font, white, int(screenWidth / 8), 10)

        if player.health > 3:

            screen.blit(healthImg, (900, 20))
            screen.blit(healthImg, (950, 20))
            screen.blit(healthImg, (1000, 20))
            drawText("+" + str(player.health - 3), font, white, 1050, 10)

        if player.health == 3:

            screen.blit(healthImg, (900, 20))
            screen.blit(healthImg, (950, 20))
            screen.blit(healthImg, (1000, 20))

        if player.health == 2:

            screen.blit(healthImg, (900, 20))
            screen.blit(healthImg, (950, 20))

        if player.health == 1:

            screen.blit(healthImg, (900, 20))

        if player.health < 1:

            gameOver = True
            buyU1 = False
            buyU2 = False
            buyU3 = False
            bulletUpgrade1 = False
            bulletUpgrade2 = False
            bulletUpgrade3 = False

            if player.highscoreKills > HighscoreKills:
                HighscoreKills = player.highscoreKills

            if resetBtn.draw():
                player.reset(int(screenWidth / 2), int(screenHeight / 2))
                room = Room(startRoomData)
                floor = Floor(startFloorData)
                room.draw()
                floor.draw()
                for enemy in enemyGroup:
                    enemy.kill()
                for merchant in merchantGroup:
                    merchant.kill()
                for chest in chestGroup:
                    chest.kill()
                overallDeaths += 1
                gameOver = False
                tutorialImgs = True

            if menuBtn.draw():
                mainMenu = True
                overallDeaths += 1

    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            run = False

        if shoot == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if bulletUpgrade1 == True:
                        if len(bulletGroup) < 2:
                            shoot = True
                    if bulletUpgrade2 == True:
                        if len(bulletGroup) < 3:
                            shoot = True
                    if bulletUpgrade3 == True:
                        if len(bulletGroup) < 4:
                            shoot = True
                    else:
                        if len(bulletGroup) < 1:
                            shoot = True

                if event.key == pygame.K_w:
                    movingUp = True

                if event.key == pygame.K_a:
                    movingLeft = True

                if event.key == pygame.K_s:
                    movingDown = True

                if event.key == pygame.K_d:
                    movingRight = True

                if event.key == pygame.K_e and pygame.sprite.spritecollide(player, chestGroup, False) and chest.opened == False:
                    chestGroup.update()
                        
                if event.key == pygame.K_e and player.accessMerchant == True:
                    MerchantInv()
                    accessedShop = True
                    pause = True

                if event.key == pygame.K_c:
                    totalCoins += 1

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE:
                shoot = False

            if event.key == pygame.K_w:
                movingUp = False

            if event.key == pygame.K_a:
                movingLeft = False

            if event.key == pygame.K_s:
                movingDown = False

            if event.key == pygame.K_d:
                movingRight = False

    pygame.display.update()

pygame.quit()
