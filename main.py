#Check how to teach in this video; Space Invader game: https://www.youtube.com/watch?v=FfWpgLFMI7w&t=1370s
import pygame 
#Initialise the pygame
pygame.init()
#create the screen: width 800, height 600
screen=pygame.display.set_mode((800,600))

#Title & Icon
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyImg=pygame.image.load('enemy.png')
enemyX=370
enemyY= 490
enemyX_change=0

def player(x,y):
    #Draws the player on the screen
    screen.blit(playerImg, (x, y))

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

    
#Game loop
#Checking for QUIT button pressed
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    #if keystroke is pressed check whether its right or left
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_LEFT:
            playerX_change=-0.3
        if event.key==pygame.K_RIGHT:
            playerX_change=0.3
    if event.type==pygame.KEYUP:
        if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
            playerX_change=0


    #Background color
    screen.fill((0,0,0))
   
   #Change the position of the player horizontally
    playerX+=playerX_change

    #Adding boundaries to the movement of the player.
    if playerX<=0:
        playerX=0
    elif playerX>=736:  #736=800(total width of screen)-64(size of spaceship 64x64)
        playerX=736

    enemy(enemyX, enemyY)
    player(playerX, playerY)
    pygame.display.update()

