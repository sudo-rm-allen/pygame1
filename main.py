import pygame
import random
pygame.init()
screenH = 904
screenW = 1280
win = pygame.display.set_mode((screenW,screenH)) #width then hieght
pygame.display.set_caption("First Game")
randomNum = random.random() * screenW//2

#sounds
sounds = [pygame.mixer.Sound('Music\gun.wav'), pygame.mixer.Sound('Music\hit.wav')]
bgMusic = pygame.mixer.music.load('Music\cicada.mp3')
sounds[0].set_volume(1)
sounds[1].set_volume(1)
pygame.mixer.music.set_volume(1)

pygame.mixer.music.play(-1)



walkRight = [pygame.image.load('Game\R1.png'), pygame.image.load('Game\R2.png'), pygame.image.load('Game\R3.png'), pygame.image.load('Game\R4.png'), pygame.image.load('Game\R5.png'), pygame.image.load('Game\R6.png'), pygame.image.load('Game\R7.png'), pygame.image.load('Game\R8.png'), pygame.image.load('Game\R9.png')]
walkLeft = [pygame.image.load('Game\L1.png'), pygame.image.load('Game\L2.png'), pygame.image.load('Game\L3.png'), pygame.image.load('Game\L4.png'), pygame.image.load('Game\L5.png'), pygame.image.load('Game\L6.png'), pygame.image.load('Game\L7.png'), pygame.image.load('Game\L8.png'), pygame.image.load('Game\L9.png')]
bg = pygame.image.load('Game\hbg.jpg')
char = pygame.image.load('Game\standing.png')

clock = pygame.time.Clock()
score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
        

    def draw(self,win):
        if self.walkCount  + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            #win.blit(char,(self.x,self.y))
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
        else: 
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            elif self.left:
                win.blit(walkLeft[0],(self.x,self.y))  
            else:
                win.blit(char,(self.x,self.y))
        
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  
        if debug:
            pygame.draw.rect(win, (255,0,0), self.hitbox,2)
            pygame.draw.line(win,(255,0,0),(round (self.x + self.width //2),round (self.y + self.height //2)),(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),2)
        
    def hit(self): 
        self.isJump = False
        self.jumpCount = 10
        self.x = 0
        self.y = 690
        self.walkCount = 0
        font1 = pygame.font.SysFont('arial',100)
        text = font1.render('-5',1,(255,0,0))
        win.blit(text, (screenW/2 - (text.get_width() /2),screenH/2 - (text.get_height() /2)  ))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i +=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

        #print("PHIT")

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
   
    
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

        
class enemy(object):
    walkRight = [pygame.image.load('Game\R1.png'), pygame.image.load('Game\R2.png'), pygame.image.load('Game\R3.png'), pygame.image.load('Game\R4.png'), pygame.image.load('Game\R5.png'), pygame.image.load('Game\R6.png'), pygame.image.load('Game\R7.png'), pygame.image.load('Game\R8.png'), pygame.image.load('Game\R9.png')]
    walkLeft = [pygame.image.load('Game\L1.png'), pygame.image.load('Game\L2.png'), pygame.image.load('Game\L3.png'), pygame.image.load('Game\L4.png'), pygame.image.load('Game\L5.png'), pygame.image.load('Game\L6.png'), pygame.image.load('Game\L7.png'), pygame.image.load('Game\L8.png'), pygame.image.load('Game\L9.png')]

    #walkRight = [pygame.image.load('Game\R1E.png'), pygame.image.load('Game\R2E.png'), pygame.image.load('Game\R3E.png'), pygame.image.load('Game\R4E.png'), pygame.image.load('Game\R5E.png'), pygame.image.load('Game\R6E.png'), pygame.image.load('Game\R7E.png'), pygame.image.load('Game\R8E.png'), pygame.image.load('Game\R9E.png'),pygame.image.load('Game\R10E.png'),pygame.image.load('Game\R11E.png')]
    #walkLeft = [pygame.image.load('Game\L1E.png'), pygame.image.load('Game\L2E.png'), pygame.image.load('Game\L3E.png'), pygame.image.load('Game\L4E.png'), pygame.image.load('Game\L5E.png'), pygame.image.load('Game\L6E.png'), pygame.image.load('Game\L7E.png'), pygame.image.load('Game\L8E.png'), pygame.image.load('Game\L9E.png'),pygame.image.load('Game\L10E.png'),pygame.image.load('Game\L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 3
        self.path = [self.x,self.end]
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True  

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x,self.y))
            self.walkCount +=1
        
        
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1] - 20 , 50,10))
        pygame.draw.rect(win, (0,255,0), (self.hitbox[0],self.hitbox[1] - 20 , 5 * self.health,10))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  
        if debug:
            pygame.draw.rect(win, (255,0,0), self.hitbox,2)



    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -=1
        else:
            self.visible = False
        #print("HIT")




def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    
    for gob in goblin:  
        gob.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    text = font.render('Score: ' + str(score), 1,(0,0,0))
    win.blit(text, (10,10))
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('arial', 30,True)
run = True
man = player(0,690,64,64)
#goblins = []
#enemies = 5
goblin = []
bullets = []
bulletNumber = 5
debug = False
shootLoop = 0


while run:
    clock.tick(27)

    if len(goblin) < 1:
        goblin.append(enemy(random.random()*(screenW - 64) + 1,690,64,64,screenW - 64))


    for gob in goblin:
        if gob.health == 0:
            goblin.pop(goblin.index(gob))
        if man.hitbox[1] < gob.hitbox[1] + gob.hitbox[3] and man.hitbox[1] + man.hitbox[3] > gob.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > gob.hitbox[0] and man.hitbox[0] < gob.hitbox[0] + gob.hitbox[2]:
                man.hit()
                score -= 20
        
        
        
 

    if shootLoop > 0:
        shootLoop +=1
    if shootLoop > 3:
        shootLoop = 0

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if keys[pygame.K_F12]:
            debug = not(debug)

  
    (mousex,mousey) = pygame.mouse.get_pos()
    for bullet in bullets:

        for gob in goblin:
            if bullet.y - bullet.radius < gob.hitbox[1] + gob.hitbox[3] and bullet.y + bullet.radius > gob.hitbox[1]:
                if bullet.x + bullet.radius > gob.hitbox[0] and bullet.x - bullet.radius < gob.hitbox[0] + gob.hitbox[2]:
                    sounds[1].play()
                    gob.hit()
                    score += 10
                    bullets.pop(bullets.index(bullet))     
                

 
        if bullet.x < screenW and bullet.x > 0:
        
            bullet.x += bullet.vel 

        else:
            bullets.pop(bullets.index(bullet))

    
    mouseL = pygame.mouse.get_pressed()[0]
    

    if mouseL or keys[pygame.K_SPACE] and shootLoop == 0:
        
        if man.left:
            facing = -1 
        else:
            facing = 1

        if len(bullets) < bulletNumber:
            
            bullets.append(projectile( round (man.x + man.width //2) ,  round (man.y + man.height //2) , 6, (0,0,0), facing))
            sounds[0].play()
        shootLoop = 1

    

    if keys[pygame.K_LEFT] or keys[pygame.K_a] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and man.x < screenW - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0


    if not(man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.right = False
            man.left = False

    else:
        if man.jumpCount >= -10 :
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit