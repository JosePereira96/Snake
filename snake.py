import random
import math
import pygame

#window size
width = 1300
height = 700

minX = 2*width/10
maxX = 8*width/10

def updateVelocity():
    global score
    global velocity
    global step
    
    #update velocity when score is a multiple of 5
    if score!=0 and (score%step==0 or score%step==5):    
        velocity += 1
    
    
def summonFood():
    global food
    global step
    global maxX
    global minX
    global height
    
    #choosing x and y location for food. need to be a multiple of step and between the minX and maxX values
    x = step*random.randint(minX/step +2,maxX/step - 2)
    y = step*random.randint(2,height/step - 2)
    
    food = pygame.Rect(x,y,step,step)
    
def eatFood():
    global snake
    global step
    global score
    global snake_head
    
    last = snake[len(snake)-1]
    
    if len(snake)>1:
        
        penultimate = snake[len(snake)-2]
        
        if penultimate[0] == last[0]:
            #snake is moving up/down
            
            x = last[0]
            
            if penultimate[1] > last[1]:
                #snake is moving down
                #create food up (smaller y value) from last element
                newLast = pygame.Rect(last[0],last[1]-step,step,step)
            else:
                #snake is moving up
                #create food down from last element
                newLast = pygame.Rect(last[0],last[1]+step,step,step)
                
        elif penultimate[1] == last[1]:
            #snake is moving sideways
            y = last[1]
            if penultimate[0] > last[0]:
                #snake is moving right
                #create food left of last element
                newLast = pygame.Rect(last[0]-step,last[1],step,step)
            else:
                #snake is moving left
                #create food right of last element
                newLast = pygame.Rect(last[0]+step,last[1],step,step)
    else:
        if snake_direction == [0,1]:
            newLast = pygame.Rect(last[0],last[1]-step,step,step)
        elif snake_direction == [0,-1]:
            newLast = pygame.Rect(last[0],last[1]+step,step,step)
        elif snake_direction == [1,0]:
            newLast = pygame.Rect(last[0]-step,last[1],step,step)
        elif snake_direction == [-1,0]:
            newLast = pygame.Rect(last[0]+step,last[1],step,step)
        
    snake.append(newLast)
    score += 1
    
    updateVelocity()
    
def beginGame():
    global snake
    global snake_head
    global snake_direction
    global velocity
    global score
    global highscore
    
    highscore = max(score, highscore)
    
    score = 0
    
    snake = []

    snake_head = pygame.Rect(int(screen.get_width()/2), int(screen.get_height()/2),step,step)

    snake.append(snake_head)

    snake_direction = pygame.Vector2(0,0)
    
    velocity = 5

    summonFood()

def youLost():
    global velocity
    global screen
    global maxX
    global minX
    global step
    global height
    global snake 
    global running
    
    print(snake)
    
    velocity = 0
    screen.blit(pygame.font.Font.render(font, "You Lost! Retry(Y/N)?" ,True,(255,255,255)),((maxX-minX)/2 + 5*step,height/3))
    pygame.display.flip()
        
    #pygame.event.set_allowed(pygame.KEYDOWN)
        
    pygame.event.wait()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:
        beginGame()
            
    elif keys[pygame.K_n]:
        running = False



# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

score = 0
font = pygame.font.Font(pygame.font.get_default_font(), 36)
#pygame.font.render(score)
#welcome_text = pygame.font.Font.render(pygame.font.SysFont("bahnschrift", 30), str(score), True, (0, 0, 0))


running = True
dt = 0

step = 10

velocity = 5

highscore = 0

ateFood = False

beginGame()


topBorder = pygame.Rect(minX,0,maxX-minX,step)
bottomBorder = pygame.Rect(minX,height-step,maxX-minX,step)
rightBorder = pygame.Rect(minX,0,step,height)
leftBorder = pygame.Rect(maxX,0,step,height)



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    #drawing borders
    pygame.draw.rect(screen, "green", topBorder)
    pygame.draw.rect(screen, "green", bottomBorder)
    pygame.draw.rect(screen, "green", rightBorder)
    pygame.draw.rect(screen, "green", leftBorder)
    
    screen.blit(pygame.font.Font.render(font, "Score: " + str(score) ,True,(255,255,255)),(width-20*step,25))
    
    
    
    #screen.blit(pygame.font.Font.render(font, "Press W,A,S,D to start" ,True,(255,255,255)),(width,25))
        
    #drawing snake
    for i in range(len(snake)):
        pygame.draw.rect(screen, "red", snake[i])
    
    #drawing food
    pygame.draw.rect(screen, "white", food)
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    
    
    #check if snake ate the food
    if snake_head.colliderect(food):
        ateFood = True
        summonFood()
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != [0,1]:
        snake_direction = pygame.Vector2(0,-1)
    if keys[pygame.K_s] and snake_direction != [0,-1]:
        snake_direction = pygame.Vector2(0,1)
    if keys[pygame.K_a] and snake_direction != [1,0]:
        snake_direction = pygame.Vector2(-1,0)
    if keys[pygame.K_d] and snake_direction != [-1,0]:
        snake_direction = pygame.Vector2(1,0)
    
    #for i in range(1,len(snake)):
        #if snake_head.colliderect(snake[i]):
            #youLost()

            
    #update snake position WITH RECT
    #'''
    if not(snake_head.colliderect(topBorder) or snake_head.colliderect(bottomBorder) or snake_head.colliderect(rightBorder) or snake_head.colliderect(leftBorder)):
        
        previousX = snake_head[0]
        previousY = snake_head[1]
        snake_head[0] += velocity*snake_direction[0]
        snake_head[1] += velocity*snake_direction[1] 
        
        for i in range(1,len(snake)):
            auxX = snake[i][0]
            auxY = snake[i][1]
            
            snake[i][0] = previousX
            snake[i][1] = previousY
            
            previousX = auxX
            previousY = auxY
        if ateFood:
            eatFood()
            ateFood = False
    else:
        pygame.event.set_allowed(pygame.KEYDOWN)
        youLost()
       
    '''
    
    #update snake position
    if (snake_head[0] >= minX + 2*step and snake_head[0] <= maxX-2*step) and (snake_head[1] >= 2*step and snake_head[1] <= screen.get_height()-2*step):
        
        previousX = snake_head[0]
        previousY = snake_head[1]
        snake_head[0] += velocity*snake_direction[0]
        snake_head[1] += velocity*snake_direction[1] 
        
        for i in range(1,len(snake)):
            auxX = snake[i][0]
            auxY = snake[i][1]
            
            snake[i][0] = previousX
            snake[i][1] = previousY
            
            previousX = auxX
            previousY = auxY
            
        if ateFood:
            eatFood()
            ateFood = False
            
    else:
        youLost()
     '''       
    
pygame.quit()