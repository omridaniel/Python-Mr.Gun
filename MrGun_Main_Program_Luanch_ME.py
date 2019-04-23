#########################################
# Programmer: Omri
# Date: June 5th 2018
# File Name: mr_gun.py
# Description: This program is a game based of Ketchapp's mr.gun
#########################################
from mr_gun_classes import *
from random import randint
import pygame
pygame.init()
################
#-----Variables-----#
################

#-----Window Properties-----#
HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//20
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (192,192,192)

#-----Basic X,Y Cordinates-----# 
LEFT = 50                                
RIGHT = 700         
BADFLOOR = 290 
GOODFLOOR = 490

#-----Background-----#
back1 = pygame.image.load("back1.png")
back1H = HEIGHT
back1X = 0
back1Y = 0

back2 = pygame.image.load("back2.png")
back2H = 600
back2X = 0
back2Y = -600

scrollSpeed=10
stopLvl=200
scrollBack=False

#-----Gun Properties-----#
gunL=pygame.image.load("gunL.png")
gunL=pygame.transform.scale(gunL,(50,30))

gunR=pygame.image.load("gunR.png")
gunR=pygame.transform.scale(gunR,(50,30))

draw_bullet=False

objectX = WIDTH//8
objectY = HEIGHT//1.25
objectR = 10
objectAngle = 0

shot=Bullet(objectX,objectY,4,20,10)    #Bullet declared as object

score=0

#-----Intro/Outro Screens-----#
inPlay=0
infoScreen=False

introPic=pygame.image.load('intro.png')
info=pygame.image.load('instructions.png')
end=pygame.image.load('outro.png')

#-----Drawing Characters-----#
moveGuy=0                           #Diffrent positions 0=stopeed, 1=ladder, 2=other side, 3 and 4=final pos
draw_bad_guy=True
draw_bad_guy2=False
movesRight=True                 #Moves to right/ moves right first
movesLeft=False
check_collisions=True
spawn_guy=1                       #What side to spawn bad guy 1=right, -1=left

bad_colour=randint(1,5)         #Bad guy body colour
bad_guy=Block(RIGHT,BADFLOOR,bad_colour,80,70)      #Bad guy on right side
bad_guy2=Block(LEFT,BADFLOOR,bad_colour+1,80,70)    #Bad guy on left side

good_guy=Block(LEFT-10,GOODFLOOR,7,80,70) 

#-----Angle Properties-----#
CENTERX = WIDTH//8
CENTERY = HEIGHT//1.25
VELOCITY = 30
VECTOR = 175

vectorX = 0
vectorY = 0
vectorAngle = 0
rotationStep = 1
direction = 1

drawAngle=True
move=True #When false bullet is drawn and moved
side=1 #Side angle appears on 1=right, -1=left

#-----Sounds-----#
song=pygame.mixer.Sound('song.ogg')
song.play(-1)
shoot=pygame.mixer.Sound('shoot.wav')
bod_shot=pygame.mixer.Sound('bod_shot.ogg')
head_shot=pygame.mixer.Sound("head_shot.ogg")
dead=pygame.mixer.Sound("dead.ogg")

#-----Fonts-----#
font=pygame.font.SysFont("Arial Black",40)       #font declaration
font2=pygame.font.SysFont("Arial Black",80)       #font2 declaration
headShotTxt=font.render("HEADSHOT!",1,RED)
headshot=False                                                  #Detects when headshot was hit

#################
#-----Functions-----#
#################

def redraw():                                                                                                                                                       #Function for drawing game field
    screen.blit(back1, (back1X,back1Y))
    screen.blit(back2, (back2X,back2Y))
    scoreTxt=font.render("Score: "+ str(score),1,WHITE)
    screen.blit(scoreTxt,(10,0))
    good_guy.draw(screen)

def face_right():                                                                                                                                                   #Function for drawing angle facing the right side
    pygame.draw.line(screen,WHITE,(CENTERX,GOODFLOOR),(CENTERX+vectorX,GOODFLOOR-vectorY),1)
    screen.blit(gunR,(CENTERX-50,GOODFLOOR))

def face_left():                                                                                                                                                    #Function for drawing angle facing the left side
    pygame.draw.line(screen,WHITE,(CENTERX,GOODFLOOR),(CENTERX-vectorX,GOODFLOOR-vectorY),1)
    screen.blit(gunL,(CENTERX,GOODFLOOR))

def switch_direction(vectorAngle,move):                                                                                                         #Function to keep angle in motion up/down
    if vectorAngle>=60:
        return -1
    elif vectorAngle<=0:
        return 1
    else:
        return 1

def intro():                                                                                                                                                        #Intro screen
    screen.blit(introPic,(0,0))
    pygame.display.update()

def instructions():                                                                                                                                             #Instruction screen
    screen.blit(info,(0,0))
    pygame.display.update()
    
def outro():                                                                                                                                                        #End game screen
    screen.blit(end,(0,0))
    scoreTxt=font2.render(str(score),1,BLACK)
    screen.blit(scoreTxt,(400,410))
    pygame.display.update()

def scrolling(back1Y,back2Y,back2H,back1H,scrollSpeed):                                                                             #Function for scrolling background
    back1Y = back1Y + scrollSpeed
    if back1Y + scrollSpeed > back1H:
        back1Y = -back2H
    back2Y = back2Y + scrollSpeed
    if back2Y + scrollSpeed > back2H:
        back2Y = -back1H
    return (back1Y,back2Y,back2H,back1H,scrollSpeed)
#####################
#-----Main Program-----#
#####################

#-----Intro Screens-----#
while inPlay==0:
    pygame.event.get()
    for event in pygame.event.get():                                              #Check for any events
        if event.type == pygame.QUIT:                                            #If user clicked close
            inPlay= 4                                                                          #Flag that we are done so we exit this loop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:                                                     #If space pressed exit intro screen
        inPlay=2
    elif keys[pygame.K_i]:                                                          #if i is pressed go to information screen
        infoScreen=True
    elif keys[pygame.K_b]:                                                          #if b is pressed gp back to intro screen
        infoScreen=False
    if infoScreen:                                                                      #if infoScreen is true then show the game instructions
        instructions()
    else:                                                                                   #else show the intro screen
        intro()
#------Main Game-----#
while inPlay==2:                                                                    #Run main game
    redraw()                                                                                #Constantly redraw background and good guy

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:                        #ESC to quit game
                inPlay = 4
                
            if event.key == pygame.K_SPACE and drawAngle:       #Function for pressing space bar
                VELOCITY=30
                move=False
                drawAngle=False
                shot.x = CENTERX
                shot.y = CENTERY
                objectAngle =  -1*vectorAngle
                shoot.play()
                
                if side==1:                                                             #Checks what side the angle needs to appear on and draws it
                    CENTERX = WIDTH//2+300                                #
                    side=-1                                                             #
                    if drawAngle:                                                   #
                        face_left()                                                     #

                elif side==-1:                                                        #
                    CENTERX = WIDTH//2-300                                 #
                    side=1                                                              #
                    if drawAngle:                                                   #
                        face_right()                                                  #

    if side==1 and drawAngle:                                             #
        face_right()                                                                 #
    elif side==-1 and drawAngle:                                         #
        face_left()                                                                  #
        
    if vectorAngle <= 0 or vectorAngle >= 60  or flag==0:       #Checks when the angle goes over or less than 60 degrees and moves it back up/down
        flag = switch_direction(vectorAngle,move)
    vectorAngle = (vectorAngle + rotationStep*flag)
                                                                                          # rotate the vector (move its end point)
    vectorX = int(round(VECTOR*cos(vectorAngle*pi/180))) # sin and cos functions require argument angle
    vectorY = int(round(VECTOR*sin(vectorAngle*pi/180))) # to be in radians (360 degrees = 2*pi radians)
    
#-----Drawing Functions-----#
    if move==False:                                                          #Checks if bullet needs to be drawn/moved when space is pressed
        shot.draw(screen)
        shot.move_bul(side,VELOCITY,objectAngle)
        
    if draw_bad_guy:                                                        #Checks when to draw guy on right side
        bad_guy.draw(screen)
        
    if draw_bad_guy2:                                                      #Checks when to draw guy on left side
        bad_guy2.draw(screen)
        
#-----Collisions-----#
    if check_collisions:                                                    #Variable for when to check for collisions (False after firsst collision detected)
        if shot.collidesBod(bad_guy)==(0,40):                    #Collisions for body of bad guy on right side
            draw_bullet=False
            draw_bad_guy=False
            moveGuy=1
            score+=1
            bod_shot.play()
            headshot=False
            check_collisions=False
            VELOCITY=0
            shot.x=WIDTH
            rotationStep+=0.25
                                                                                          
        elif shot.collidesBod(bad_guy)==(-20, -70):             #Collisions for head of guy on right
            draw_bullet=False
            draw_bad_guy=False
            moveGuy=1
            score+=2
            head_shot.play()
            headshot=True
            check_collisions=False
            VELOCITY=0
            shot.x=WIDTH
            rotationStep-=0.25

        elif shot.collidesBod(bad_guy2)==(0,40):             #Collisions for bod of guy on left
            draw_bullet=False       
            draw_bad_guy2=False
            moveGuy=1
            score+=1
            bod_shot.play()
            headshot=False
            check_collisions=False
            VELOCITY=0
            shot.x=WIDTH
            rotationStep+=0.25
 
        elif  shot.collidesBod(bad_guy2)==(-20,-70):        #Collision for head of guy on left
            draw_bullet=False
            draw_bad_guy2=False
            moveGuy=1
            score+=2
            head_shot.play()
            headshot=True
            check_collisions=False
            VELOCITY=0
            shot.x=WIDTH
            rotationStep-=0.25

        if shot.x>WIDTH or shot.x<0:                            #Checks if bullet is out of screen/missed
            inPlay=3
            dead.play()

        if rotationStep<=0.25:                                      #Resistricts roation step of angle from reachin 0/not moving
            rotationStep=0.5
            
#-----Movement Stages for Right Side------#
    if movesRight:
        if moveGuy==1:
            scrollBack=good_guy.moveR1()
            if headshot:
                screen.blit(headShotTxt,(300,HEIGHT//2))  
            if back1Y==stopLvl or back2Y==stopLvl:
                scrollBack=False                
                if scrollBack==False:
                    moveGuy=2
                    stopLvl+=200                    
                if stopLvl==600:
                    stopLvl=0
                    
        if moveGuy==2:
            good_guy.moveR2()            
            if good_guy.x==700:
                moveGuy=3
                movesLeft=True
                drawAngle=True
                check_collisions=True

    if moveGuy==3:
        draw_bad_guy2=True
        movesRight=False
        
#-----Movement Stages for Left Side------#
    if movesLeft:
        if moveGuy==1:
            scrollBack=good_guy.moveL1()
            if headshot:
                screen.blit(headShotTxt,(300,HEIGHT//2))                
            if back1Y==stopLvl or back2Y==stopLvl:
                scrollBack=False                
                if scrollBack==False:
                    moveGuy=2
                    stopLvl+=200                    
                if stopLvl==600:
                    stopLvl=0
                    
        if moveGuy==2:
            good_guy.moveL2()            
            if good_guy.x==40:
                moveGuy=4
                movesRight=True
                drawAngle=True
                check_collisions=True
                
    if moveGuy==4:
        draw_bad_guy=True
        movesLeft=False
        
#------Scrolling Background-----#
    if scrollBack:
        (back1Y,back2Y,back2H,back1H,scrollSpeed)=scrolling(back1Y,back2Y,back2H,back1H,scrollSpeed)
        
    pygame.display.update()         #Constantly update game screen
    
#-----Game Over Screen-----#
while inPlay==3:
    outro()
    pygame.time.delay(5000)                                            
    inPlay=4
    
#-----Quit Pygame-----#
pygame.quit()
