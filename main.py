#Check how to teach in this video; Space Invader game: https://www.youtube.com/watch?v=FfWpgLFMI7w&t=1370s
#Format document: Ctrl+Shift+I, Format selection: Ctrl+K, Ctrl+F.
import pygame 
import random
import math
import time
from pygame import mixer

#Initialise the pygame
pygame.init()

#CONSTANTS
COLLISION_DISTANCE = 27 
WIDTH=736 #736=800(total width of screen)-64(size of spaceship/enemy 64x64)
HEIGHT=600
PLAYERX_START = 370
PLAYERY_START=480
NUMBER_OF_ENEMIES = 6
SCORE_X=10
SCORE_Y=10

#Variables
score=0
score_font=pygame.font.Font('freesansbold.ttf',12)

#create the screen: width 800, height 600
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#Background
background=pygame.image.load("background.jpg")

#Background sound
mixer.music.load('background.mp3')
mixer.music.play(-1) #-1 to play the background in a loop, not just once

#Title & Icon
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Initial state of the Player
playerImg=pygame.image.load('player.png')
playerX=PLAYERX_START
playerY=PLAYERY_START
playerX_change=0

#Initial state of the Enemy
#Creating  multiple enemies
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

for i in range(NUMBER_OF_ENEMIES):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,WIDTH))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.1)
    enemyY_change.append(10)

#Initial state of the Bullet
#bullet_state="ready" You can't see the bullet on the screen
#bullet_state="fire", The bullet is currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX=playerX
bulletY= playerY
bulletX_change=0
bulletY_change=-0.3
global bullet_state
bullet_state="ready"

"""
FUNCTIONS
"""
def player(x,y):
    #Draws the player on the screen
    screen.blit(playerImg, (x, y))
#end def

def enemy(enemyImg, x,y):
    screen.blit(enemyImg,(x,y))
#end def

def fire_bullet(x,y):
    #Place the  bullet relative to the spaceship
    #x+16 & y+10 The bullet should appear on the centre of the spaceship
    screen.blit(bulletImg,(x+16,y+10))

    
#end def

#Collision Detection
# Distance between two points and the midpoint: D= square root of(square of (x2-x1)+square of(y2-y1))
def is_collision(enemyX, enemyY, bulletX, bulletY):     
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY, 2))) #Calculation for collision 
    
    if distance <= COLLISION_DISTANCE:  

        return True
    else:
        return False
    #end if
    
def show_score(score):
    score_text=score_font.render("Score:"+str(score),True,'#FFFFFF')
    screen.blit(score_text, (SCORE_X,SCORE_Y))#draws the score on the top-left corner
    pygame.display.update()
    time.sleep(2)
# end def

#Game loop
#Checking for QUIT button pressed
running = True
while running: 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #end if

        #if keystroke is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.3
            #end if
            if event.key==pygame.K_RIGHT:
                playerX_change=0.3
            #end if

            #If the spacebar is pressed, the bullet should fire
            if event.key==pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletY_change = -0.3
                    bulletX=playerX  
                    bullet_state="fire"
                    bullet_sound=mixer.Sound('shoot.mp3')
                    bullet_sound.play()
                #end if
            #end if
        #end if
                       
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            #end if
        #end if

    #Background color
    screen.fill((0,0,0))
    screen.blit(background, (0,0))

   
   #Change the position of the player horizontally
    playerX+=playerX_change

    #Adding boundaries to the movement of the player.
    if playerX<=0:
        playerX=0
    elif playerX>=736:  #736=800(total width of screen)-64(size of spaceship 64x64)
        playerX=736
    #end if 

    for i in range(NUMBER_OF_ENEMIES):

        #Change the position of the enemy horizontally
        enemyX[i]+=enemyX_change[i]

        #Adding boundaries to the movement of the enemy.
        if enemyX[i]<=0:
            enemyX_change[i]=0.1 #When the enemy reaches the left boundary, the position of x should be positive i.e. it should move right
            enemyY[i]+=enemyY_change[i]
            
        elif enemyX[i]>=736:
            enemyX_change[i]=-0.1  #When the enemy reaches the right boundary, the position of x should be negative i.e. it should move left
            enemyY[i]+=enemyY_change[i]    
        #end if

        #Check for Collision detection
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            mixer.music.load('explosion.mp3')
            mixer.music.play(fade_ms=500) 
            bulletX = playerX
            bullet_state = "ready"
            score+=1
            show_score(score)

            #Generate new position of the enemy
            enemyX[i]=random.randint(0,WIDTH)
            enemyY[i]= random.randint(50,150)
        #end if
    
        enemy(enemyImg[i],enemyX[i], enemyY[i])
      #end for loop

    #To fire the bullet
    if bullet_state == "fire":
        bulletY +=bulletY_change             
        fire_bullet(bulletX, bulletY)
    #end if

    #To re-fire the bullet
    if bulletY <=0:
        bulletY = playerY
        bullet_state = "ready"
    #end if
    
    player(playerX, playerY)
    pygame.display.update()
   
#end while
