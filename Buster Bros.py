#Akeen Zhong
#January 18, 2014
#Buster Bros Remake
#One of my favourite games as a child, remade on pygame (Pop balloons to win)

#Import modules
import pygame
import time
from random import choice,randint
from pygame.locals import *
pygame.init()
pygame.mixer.init()

#Set colour variables and width / height
display_width = 1055
display_height = 660

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue=(0,0,200)
bright_red = (255,0,0)
bright_green = (0,255,0)

#Assign variables for sounds
popsound = pygame.mixer.Sound('pop.wav')
music = pygame.mixer.music.load('sunrise.wav')


#Set up clock caption and images
gameDisplay= pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Buster Bros. Remake')
clock = pygame.time.Clock()
playerface = pygame.image.load('sprite.png')
framework = pygame.image.load('framework.png').convert()
background = pygame.image.load('fuji1.jpg').convert()
lifeimage = pygame.image.load('sparelives.png')
happyplace = pygame.image.load('skies.png')
pausescreen=pygame.image.load('pause comic.jpg')
startscreen=pygame.image.load('pangstartscreen.png')
userfile = open('leaderboard.txt','a')

#These are the bullet, level and balloon variables
fire = False
level=2

startspeed=[-3,3]

largex=[]
largey=[]

medx=[]
medy=[]

smallx=[]
smally=[]


largexdir=[]
largeydir=[]

medxdir=[]
medydir=[]

smallxdir=[]
smallydir=[]

lives=3
popcount=0
lives=3
pause=True


#This function allows the user to enter their name, which is later stored to a file
#Parts of function taken from Pygame Example 10, Type Input
def entername():
    global textvalue
    #Heading is Arial
    headingfont = pygame.font.SysFont('Arial',20)
    myfont=pygame.font.SysFont('Times New Roman',25)
    #Set up variable and prompt user to type name
    textvalue=''
    head=headingfont.render('Type your Name Below',True,(255,255,255))
    myname=myfont.render(textvalue,True,(0,0,0))
    #Blit the header
    gameDisplay.blit(head,(520,540))
    #Blit the surface and give it a white colour
    typearea=pygame.Surface((429,35)).convert()
    typearea.fill((255,255,255))
    
    gameDisplay.blit(typearea,(402,581))
    #Draw the border around the rectangle
    pygame.draw.rect(gameDisplay,(255,0,255),(400,580,434,38),3)
    #Refresh the display
    pygame.display.update()
    typing=True
    #Set up loop
    while typing:
        clock.tick(60)
        events=pygame.event.get()
        for ev in events:
            if ev.type == QUIT:
                pygame.quit()
                quit()
            if ev.type==KEYDOWN:
                #Delete one letter if backspace is pressed
                if ev.key==K_BACKSPACE and len(textvalue)>0:
                    textvalue=textvalue[:-1]
                #Break out of function is enter is pressed and there is a suitable value for textvalue
                elif ev.key==K_RETURN and len(textvalue)>1:
                    return textvalue
                elif ev.unicode and len(textvalue)<19:
                    textvalue=textvalue+ev.unicode
                #Show typed text on screen
                text = myfont.render(textvalue,True,(0,0,0))
                gameDisplay.blit(typearea,(400,581))
                gameDisplay.blit(text,(400,581))
                pygame.display.update()


                
#Button taken from sentdex tutorial on youtube: https://www.youtube.com/watch?v=jh_m-Eytq0Q
#Button message, coordinates, length / width, colour if left alone, and colour if hovered over are the the parameters
def button(msg,x,y,w,h,ic,ac,action=None):
    #Detect mouse position and presses
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        #Quit or start the game, depending on the button
        if click[0]==1 and action!=None:
            action()
    #Draw the buttons if left alone
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
    #Type the text onto the buttons, find the rectangle and blit it
    smallText = pygame.font.Font('freesansbold.ttf',20)
    textSurf,textRect = text_objects(msg,smallText)
    textRect.center = ((x+(w/2)),y+(h/2))
    gameDisplay.blit(textSurf,textRect)


#This function advances the level
def nextlevel():
    #Allows the variable to be used anywhere
    global level
    #Advance level
    level+=1
    #Show user the next level has arrived
    message_display('Level '+str(level))



#Text code taken from another sentdex tutorial: https://www.youtube.com/watch?v=dX57H9qecCU
    
#This function will create a surface and a rectangle
def text_objects(text,font):
    
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()



def message_display(text):
    #Select the font used to displa the message
    largeText = pygame.font.Font('freesansbold.ttf',115)
    #Take the variables returned by the text_objects()
    TextSurf, TextRect = text_objects(text, largeText)
    #Center the text
    TextRect.center = ((display_width/2),(display_height/2))
    #Blit it onto screen, refresh display
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    #Pause for a few seconds
    time.sleep(2)
    #Resume game
    game_loop()



def gameover(text):
    pygame.mixer.quit()
    #Open reference variable
    userfile = open('leaderboard.txt','a')
    #Write name and score
    userfile.write(textvalue+'\n')
    userfile.write(str(popcount)+'\n')
    #Close reference variable
    userfile.close()
    #Select the font telling you Game OVer
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    #Center the text
    TextRect.center = ((display_width/2),(display_height/2))
    #Blit it onto screen and refresh display
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(3)
    #Calls leaderboard function
    leaderboard()



def leaderboard():
    #Create empty lists, user 1 is the order of the people playing
    #User 2 correlates player with score
    user1=[]
    user2=[]
    #Score, in chronological order
    unsortedscore=[]
    #Open leaderboard file, this time to read
    leaderfile = open('leaderboard.txt','r')
    #Create large list
    leaderlist = leaderfile.readlines()
    #Fill up user1 and unsortedscore by stripping '\n' and distributing elements by index position
    for index in range(len(leaderlist)):
        leaderlist[index]=leaderlist[index].rstrip("\n")
    for index in range(len(leaderlist)):
        if index==0:
            user1.append(leaderlist[index])
        elif index%2==0:
            user1.append(leaderlist[index])
        else:
            unsortedscore.append(leaderlist[index])
    #User 2 has to be the same length as user 1 for the next operation, so fill it with empty strigs
    for filler in range(len(user1)):
        user2.append('')
    #Change unsortedscore elements to integers, and create a sorted score list
    unsortedscore = [int(intchange)for intchange in unsortedscore]
    score=sorted(unsortedscore,reverse=True)
    #This code will fill user2 ranking from highest to lowest score
    for scorecycle in range(len(user1)):
        for usercycle in range(len(user1)):
            if unsortedscore[usercycle]==score[scorecycle]:
                user2[scorecycle]=user1[usercycle]
    #Show leaderboard screen
    gameDisplay.fill(white)
    #Blit image
    gameDisplay.blit(happyplace,(0,0))
    #Choose font for title 
    leaderboardfont=pygame.font.SysFont('Times New Roman',118)
    #Choose leaderboard font
    genericfont = pygame.font.SysFont('Courier',64)
    #Render the title text
    leaderboarddisplay=leaderboardfont.render('Leaderboard',True,(0,0,0))
    if len(user2)<5:
        #Display the users and the score, up to the top five
        for top in range(len(user2)):
            if 1<=len(user2[topfive])<=5:
                genericfontdisplay=genericfont.render(user2[topfive]+'       '+str(score[topfive]),True,(0,0,0))
            if 6<=len(user2[topfive])<=9:
                genericfontdisplay=genericfont.render(user2[topfive]+'    '+str(score[topfive]),True,(0,0,0))
            gameDisplay.blit(genericfontdisplay,(300,200+topfive*80))

    else:
        #Display the users and the score, up to the top five
        for topfive in range(5):
            if 1<=len(user2[topfive])<=5:
                genericfontdisplay=genericfont.render(user2[topfive]+'       '+str(score[topfive]),True,(0,0,0))
            if 6<=len(user2[topfive])<=9:
                genericfontdisplay=genericfont.render(user2[topfive]+'    '+str(score[topfive]),True,(0,0,0))
            gameDisplay.blit(genericfontdisplay,(300,200+topfive*80))

    #Blitthe title text onto the screen, refresh display
    gameDisplay.blit(leaderboarddisplay,(260,40))
    pygame.display.update()
    #Quit the game
    pygame.quit()
    quit()



def death():
    pygame.mixer.music.stop()                          
    #Subtracts a life, then gets back into game
    message_display('OW!')




def showlives():
    #Blit lives icon depending on the quantity
    if lives>0:
        gameDisplay.blit(lifeimage,(30,615))
    if lives>1:
        gameDisplay.blit(lifeimage,(70,615))
    if lives>2:
        gameDisplay.blit(lifeimage,(110,615))



#This function draws the large balls
def largeballoons():
        #Fill the x coords with random integers
        while len(largex)!=len(largeballs):
                largex.append(randint(70,390))
        #Fill the y coords with random integers
        while len(largey)!=len(largeballs):
                largey.append(randint(60,350))
        #Fill the xdirection with a choice of -3 or 3
        while len(largexdir)!=len(largeballs):
                largexdir.append(choice(startspeed))
        #Fill the ydirection with a choice of -3 or 3
        while len(largeydir)!=len(largeballs):
                largeydir.append(choice(startspeed))
        #Draw the circles
        for largeindex in range(len(largeballs)):
            if largeballs[largeindex]:
                pygame.draw.circle(gameDisplay,red,(largex[largeindex],largey[largeindex]),50)



#This function draws the medium balls
def medballoons():
    #Fill the x coords with random integers
    while len(medx)!=len(medballs):
        medx.append(randint(70,390))
    #Fill the y coords with random integers    
    while len(medy)!=len(medballs):
        medy.append(randint(60,350))
    #Fill the xdirection with a choice of -3 or 3
    while len(medxdir)!=len(medballs):
        medxdir.append(choice(startspeed))
    #Fill the ydirection with a choice of -3 or 3
    while len(medydir)!=len(medballs):
        medydir.append(choice(startspeed))
    #Draw the circles
    for medindex in range(len(medballs)):
        if medballs[medindex]:
            pygame.draw.circle(gameDisplay,green,(medx[medindex],medy[medindex]),25)



#This function draws the small balls
def smallballoons():
    #Fill the x coords with random integers
    while len(smallx)!=len(smallballs):
        smallx.append(randint(70,390))
    #Fill the y coords with random integers  
    while len(smally)!=len(smallballs):
        smally.append(randint(60,350))
    #Fill the xdirection with a choice of -3 or 3
    while len(smallxdir)!=len(smallballs):
        smallxdir.append(choice(startspeed))
    #Fill the ydirection with a choice of -3 or 3
    while len(smallydir)!= len(smallballs):
        smallydir.append(choice(startspeed))
    #Draw the circles
    for smallindex in range(len(smallballs)):
        pygame.draw.circle(gameDisplay,blue,(smallx[smallindex],smally[smallindex]),12)


        
#Display the blue brick border
def border():
    gameDisplay.blit(framework,(0,0))



#Display the scenery, Mount Fuji
def nature():
    gameDisplay.blit(background,(20,20))


#Display the player's sprite
def sprite(x,y):
    gameDisplay.blit(playerface,(x,y))


#Quit game if button is pressed
def quitgame():
    pygame.quit()
    quit()


#Unpause function allows gameloop to resume
def unpause():
    #Unpause music
    pygame.mixer.music.unpause()
    global pause
    pause = False


#Pause function 
def paused():
    #Pause music
    pygame.mixer.music.pause()
    #Set up loop
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #Fill the screen
        gameDisplay.fill(white)
        #Blit the comic
        gameDisplay.blit(pausescreen,(100,5))
        #Get paused screen font and center it onto a rect 
        largeText = pygame.font.SysFont('Comic Sans MS',115)
        TextSurf, TextRect = text_objects('Paused', largeText)
        TextRect.center = ((display_width/2),(display_height/2)+175)
        #Blit onto screen
        gameDisplay.blit(TextSurf, TextRect)
        #Draw buttons, green and red
        button('Continue',200,580,100,50,green,bright_green,unpause)
        button('Quit',750,580,100,50,red,bright_red,quitgame)
        #Refresh display
        pygame.display.update()
        clock.tick(60)



def game_intro():
    #Start the game up
    global Pause
    intro = True
    #Quit if the user needs to
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #Display the start image
        gameDisplay.blit(startscreen,(0,0))
        #Draw two buttons, green and red
        button('Start',200,580,100,50,green,bright_green,game_loop)
        button('Run Away',750,580,100,50,red,bright_red,quitgame)
        #Refresh display
        pygame.display.update()
        clock.tick(60)


   
def game_loop():
    #Declare many variables as global
    global lives,popcount
    global fire
    global bulletprogress, bulletcorner
    global startspeed
    global player_height,player_width,largeballpop,largeballs
    global level,largeballs,medballs,smallballs
    global largexdir,medxdir,smallxdir
    global largeydir,medydir,smallydir
    global largex,medx,smallx
    global largey,medy,smally,pause,textvalue

    #Loop music
    pygame.mixer.music.play(-1)
    #Ask for user name during end of intro
    if level==0:
        entername()
        level+=1
    #Set up balls depending on the level
    if level==1:
        largeballs=[]
        medballs=[]
        smallballs=[True,True,True,True,True,True]

    if level==2:
        largeballs=[True]
        medballs=[]
        smallballs=[]

    if level==3:
        largeballs=[]
        medballs=[True,True,True,True,True,True]
        smallballs=[]

    if level==4:
        largeballs=[True,True]
        medballs=[]
        smallballs=[True,True,True,True,True]

    if level==5:
        largeballs=[True,True,True,True,True,True]
        medballs=[]
        smallballs=[]
    if level==6:
        gameover('You Win!')

    #Set up variables for the sprite and the bullet
    
    bulletcorner=550
    x = (display_width * 0.45)
    y = (display_height * 0.723)
    player_height=74
    player_width = 67

    bulletprogress=0
    x_change = 0

    #Start the game
    gameExit = False

    while not gameExit:
        
        #Draw a rect around player for collision purposes
        playerbox=pygame.Rect(int(x),int(y),player_width,player_height)
        #Move the character back if it tries to go past border
        if int(x)<18:
            x=18
        if int(x)>967:
            x=967
        for event in pygame.event.get():
            #Quit if the user wants to
            if event.type == pygame.QUIT:
                gameExit = True
                quit()
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                #Pause if p is pressed
                if keys[K_p]:
                    pause = True
                    paused()
                #Move left if the left arrow is pressed
                if keys[K_LEFT]:
                    x_change = -3.5
                #Move right if the right arrow is pressed
                if keys[K_RIGHT]:
                        x_change = 3.5
                #Fire bullet, only one can be fired at a time, takes position of player when fired
                if keys[K_SPACE] and fire==False:
                    fire = True
                    bulletx=int(x)
                    bullety=int(y)
            #Stop the character if keys are not pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        #Move character
        x+=x_change
        #Fill the remainder of the screen
        gameDisplay.fill(black)
        #Set the border and the background
        border()
        nature()
        #Run the balloon functions
        if largeballs:
            largeballoons()
        if medballs:
            medballoons()
        if smallballs:
            smallballoons()


        #Happens if spacebar is pressed
        if fire:
            #Draw rectangle for visual aid
            pygame.draw.rect(gameDisplay,bright_red,[bulletx+60/2,bulletcorner,8,bulletprogress])
            #As time goes on, the height of the bullet increases
            if bulletprogress<=458+72:
                bulletprogress+=5
                bulletcorner-=5
            #It bullet hits the roof, it disappears
            if bulletprogress>530:
                fire=False
                #Reset bullet variables
                bulletprogress=0
                bulletcorner=550
            if largeballs:
                largelength = len(largeballs)
                #Check for collison with the largeballs
                for largeballpop in range(largelength):
                        #Bullet right over red rectangle
                        bullet=pygame.Rect(bulletx+60/2,bulletcorner,8,bulletprogress)
                        popped=largeballpop
                        #Try function for avoiding index error (happens if index position 0 is popped)
                        try:
                            #pygame.draw.rect(gameDisplay,blue,(100,200,3,40))
                            
                            #pygame.draw.rect(gameDisplay,black,(largex[popped]-50, largey[popped]-25, 100,50))
                            largeRectCenter = pygame.Rect(largex[popped]-50, largey[popped]-25, 100,50)
                            #sin60 * 2R
                            largeRectMiddle = pygame.Rect(largex[popped]-50+(100-86)/2,largey[popped]-37.5,86,75)
                            #sin48.6 * 2R
                            largeRectEnd = pygame.Rect(largex[popped]-50+(100-75)/2,largey[popped]-49.5,75,100)
                            #pygame.draw.rect(gameDisplay,black,[largex[popped]-50+(100-86)/2,largey[popped]-37.5,86,75])
                            #pygame.draw.rect(gameDisplay,black,[largex[popped]-50+(100-75)/2,largey[popped]-49.5,75,100])
                            #if bullet.colliderect(largex[popped]-50,largey,100,25) or bullet.colliderect(largex[popped]-50,largey-75,100,25):
                            #if bullet.collide_circle:
                            #if bullet.colliderect(largex[popped]-50,largey[popped]-50,100,100):
                            if bullet.colliderect(largeRectCenter or largeRectMiddle or largeRectEnd):
                                #If bullet collides with ball:
                                #Add 1 to score
                                #Play Sound
                                pygame.mixer.Sound.play(popsound)
                                popcount+=1
                                #Bullet disappears
                                fire=False
                                #Reset bullet variables
                                bulletprogress=0
                                bulletcorner=550
                                #Two medium balls spawn
                                for largechildren in range(2):
                                    #Add to medium ball list
                                    medballs.append(True)
                                    #Spawn from radius
                                    medx.append(largex[popped])
                                    medy.append(largey[popped])
                                    #Add the directions manually, so they go off into different directions
                                    if largechildren==0:
                                        medxdir.append(-3)
                                        medydir.append(-3)
                                    if largechildren==1:
                                        medxdir.append(-3)
                                        medydir.append(3)
                                        #Remove the popped ball from lists when finished
                                        largeballs.remove(largeballs[popped])
                                        largex.remove(largex[popped])
                                        largey.remove(largey[popped])
                                        largexdir.remove(largexdir[popped])
                                        largeydir.remove(largeydir[popped])
                                        largelength-=1
                                        
                        except IndexError: pass
                     

            #Check for medium ball collision
            if medballs:
                medlength=len(medballs)
                for medballpop in range(medlength):
                    #Bullet right over red rectangle
                    bullet=pygame.Rect(bulletx+60/2,bulletcorner,8,bulletprogress)
                    popped=medballpop
                    #Try function to avoid index error
                    try:
                        medRectCenter = pygame.Rect(medx[popped]-25, medy[popped]-12, 50,25)
                        #sin60 * 2R
                        medRectMiddle = pygame.Rect(medx[popped]-25+(50-43)/2,medy[popped]-(14),43,38)
                        #sin48.6 * 2R
                        medRectEnd = pygame.Rect(medx[popped]-25+(50-38)/2,medy[popped]-25,38,49)

                        #pygame.draw.rect(gameDisplay, black, (medx[popped]-25, medy[popped]-12, 50,25))
                        #pygame.draw.rect(gameDisplay, black, (medx[popped]-25+(50-43)/2,medy[popped]-(19*3/4),43,38))
                        #pygame.draw.rect(gameDisplay, black, (medx[popped]-25+(50-38)/2,medy[popped]-25,38,49))

                        if bullet.colliderect(medRectCenter or medRectMiddle or medRectEnd):
                            #If medium ball is popped:
                            #Add 1 to score
                            #Play Sound
                            pygame.mixer.Sound.play(popsound)
                            popcount+=1
                            #Bullet disappears
                            fire=False
                            #Reset bullet variables
                            bulletprogress=0
                            bulletcorner=550
                            #Small balls spawn out of medium balls
                            for medchildren in range(2):
                                smallballs.append(True)
                                #Spawn from radius
                                smallx.append(medx[popped])
                                smally.append(medy[popped])
                                #Add direction so they go off in different directions
                                if medchildren==0:
                                    smallxdir.append(-3)
                                    smallydir.append(-3)
                                if medchildren==1:
                                    smallxdir.append(-3)
                                    smallydir.append(3)
                                    #Remove the medium balls from the lists when finished
                                    medballs.remove(medballs[popped])
                                    medx.remove(medx[popped])
                                    medy.remove(medy[popped])
                                    medxdir.remove(medxdir[popped])
                                    medydir.remove(medydir[popped])
                                    medlength-=1

                                    
                    except IndexError: pass
                    
            #Checks for small ball collision
            if smallballs:

                smalllength=len(smallballs)
                for smallballpop in range(smalllength):
                    #pygame.draw.rect(gameDisplay, black, (smallx[popped]-12, smally[popped]-6, 24,12))
                    #pygame.draw.rect(gameDisplay, black, (smallx[popped]-12+(24-21)/2,smally[popped]-(9),21,18))
                    #pygame.draw.rect(gameDisplay, black, (smallx[popped]-12+(24-18)/2,smally[popped]-12,18,24))
                    #Bullet over red rectangle
                    bullet=pygame.Rect(bulletx+60/2,bulletcorner,8,bulletprogress)
                    popped=smallballpop
                    #Try function to avoid index error
                    try:
                        smallRectCenter = pygame.Rect(smallx[popped]-12, smally[popped]-6, 24,12)
                        #sin60 * 2R
                        smallRectMiddle = pygame.Rect(smallx[popped]-12+(24-21)/2,smally[popped]-(9),21,18)
                        #sin48.6 * 2R
                        smallRectEnd = pygame.Rect(smallx[popped]-12+(24-18)/2,smally[popped]-12,18,24)
                        if bullet.colliderect(smallRectCenter or smallRectMiddle or smallRectEnd):
                            #If bullet collides with smallball:
                            #Add 1 to score
                            #Play Sound
                            pygame.mixer.Sound.play(popsound)
                            popcount+=1
                            #Bullet disappears
                            fire=False
                            #Reset bullet variables
                            bulletprogress=0
                            bulletcorner=550
                            #Remove smallballs from lsit
                            smallballs.remove(smallballs[popped])
                            smallx.remove(smallx[popped])
                            smally.remove(smally[popped])
                            smallxdir.remove(smallxdir[popped])
                            smallydir.remove(smallydir[popped])
                            smalllength-=1

                            
                    except IndexError: pass


        #This code changes the direction of the large balls if they hit a wall
        for indexlargedir in range(len(largeballs)):
            if largex[indexlargedir]>=1032-50 or largex[indexlargedir]<=20+50:
                #Direction becomes subtracted and goes on the opposite direction (left / right)
                largexdir[indexlargedir]=largexdir[indexlargedir]*-1

            if largey[indexlargedir]>=550-50 or largey[indexlargedir]<=20+50:
                #Direction becomes subtracted and goes on the opposite direction (up / down)
                largeydir[indexlargedir]=largeydir[indexlargedir]*-1

        #This code moves the large balls depending on the direction variable
        for largeindexmove in range(len(largeballs)):
            largex[largeindexmove]=largex[largeindexmove]+largexdir[largeindexmove]
            largey[largeindexmove]=largey[largeindexmove]+largeydir[largeindexmove]



        #This code changes the direction of the medium balls if they hit a wall
        for indexmeddir in range(len(medballs)):
            if medx[indexmeddir]>=1032-25 or medx[indexmeddir]<=20+25:
                #Direction becomes subtracted and goes on the opposite direction (left / right)
                medxdir[indexmeddir]=medxdir[indexmeddir]*-1
            if medy[indexmeddir]>=550-25 or medy[indexmeddir]<=20+25:
                #Direction becomes subtracted and goes on the opposite direction (up / down)
                medydir[indexmeddir]=medydir[indexmeddir]*-1
        #This code moves the medium balls depending on the direction variable
        for medindexmove in range(len(medballs)):
            medx[medindexmove]=medx[medindexmove]+medxdir[medindexmove]
            medy[medindexmove]=medy[medindexmove]+medydir[medindexmove]



        #This code changes the directions of the small balls if they hit a wall
        for indexsmalldir in range(len(smallballs)):
            if smallx[indexsmalldir]>=1032-12 or smallx[indexsmalldir]<=20+12:
                #Direction becomes subtracted and goes on the opposite direction (left / right)
                smallxdir[indexsmalldir]=smallxdir[indexsmalldir]*-1
            if smally[indexsmalldir]>=550-12 or smally[indexsmalldir]<=20+12:
                #Direction becomes subtracted and goes on the opposite direction (up / down)
                smallydir[indexsmalldir]=smallydir[indexsmalldir]*-1
        #This code moves the small balls depending on the direction variable
        for smallindexmove in range(len(smallballs)):
            smallx[smallindexmove]=smallx[smallindexmove]+smallxdir[smallindexmove]
            smally[smallindexmove]=smally[smallindexmove]+smallydir[smallindexmove]

            
        #Advance to the next level if the lists are empty (All the balloons are popped)
        if smallballs == [] and medballs == [] and largeballs == []:
            nextlevel()
        #Blit the sprite and the lives onto the screen
        sprite(x,y)
        showlives()
        
       #This code checks for death by touching a large balloon
        for largedeath in range(len(largeballs)):
           largeDeathCenter = pygame.Rect(largex[largedeath]-50, largey[largedeath]-25, 100,50)
            #sin60 * 2R
           largeDeathMiddle = pygame.Rect(largex[largedeath]-50+(100-86)/2,largey[largedeath]-37.5,86,75)
            #sin48.6 * 2R
           largeDeathEnd = pygame.Rect(largex[largedeath]-50+(100-75)/2,largey[largedeath]-49.5,75,100)

           #if playerbox.colliderect(largex[largedeath]-50,largey[largedeath]-50,100,100):
           if playerbox.colliderect(largeDeathCenter or largeDeathMiddle or largeDeathEnd):
               #If death occurs:
               #Reset every balloon list, direction list and coordinate list
               largex=[]
               largey=[]
               largexdir=[]
               largeydir=[]
               medx=[]
               medy=[]
               medxdir=[]
               medydir=[]
               smallx=[]
               smally=[]
               smallxdir=[]
               smallydir=[]
               #Reset bullet variables
               fire=False
               bulletprogress=0
               bulletcorner=550
               #Subtract a life
               lives-=1
               #Display OW! Message
               death()

               
       #This code checks for death by touching a medium balloon
        for meddeath in range(len(medballs)):
           medRectCenter = pygame.Rect(medx[meddeath]-25, medy[meddeath]-12, 50,25)
           medRectMiddle = pygame.Rect(medx[meddeath]-25+(50-43)/2,medy[meddeath]-(14),43,38)
           medRectEnd = pygame.Rect(medx[meddeath]-25+(50-38)/2,medy[meddeath]-25,38,49)
           if playerbox.colliderect(medRectCenter or medRectEnd or medRectMiddle):
               #If death occurs:
               #Reset every balloon list, direction list and coordinate list
               largex=[]
               largey=[]
               largexdir=[]
               largeydir=[]
               medx=[]
               medy=[]
               medxdir=[]
               medydir=[]
               smallx=[]
               smally=[]
               smallxdir=[]
               smallydir=[]
               #Reset bullet variables
               fire=False
               bulletprogress=0
               bulletcorner=550
               #Subtract a life
               lives-=1
               #Display OW! Message
               death()

               
       #This code checks for death by touching a medium balloon
        for smalldeath in range(len(smallballs)):
           smallRectCenter = pygame.Rect(smallx[smalldeath]-12, smally[smalldeath]-6, 24,12)
           smallRectMiddle = pygame.Rect(smallx[smalldeath]-12+(24-21)/2,smally[smalldeath]-(9),21,18)
           smallRectEnd = pygame.Rect(smallx[smalldeath]-12+(24-18)/2,smally[smalldeath]-12,18,24)
           if playerbox.colliderect(smallRectCenter or smallRectEnd or smallRectMiddle):
               #If death occurs:00                     
               #Reset every balloon list, direction list and coordinate list
               largex=[]
               largey=[]
               largexdir=[]
               largeydir=[]
               medx=[]
               medy=[]
               medxdir=[]
               medydir=[]
               smallx=[]
               smally=[]
               smallxdir=[]
               smallydir=[]
               #Reset bullet variables
               fire=False
               bulletprogress=0
               bulletcorner=550
               #Subtract a life
               lives-=1
               #Display OW! Message
               death()

                
        #Display Game Over message if out of lives
        if lives==0:
            gameover('Game Over')
        #Refresh displays   
        pygame.display.update()
        #Clock ticks at 60 FPS
        clock.tick(60)
        
#Create the main function, running everything
def main():
    game_intro()
    game_loop()
    
#Run main function (has everything)
main()

#Quit when finished
pygame.quit()
quit()
