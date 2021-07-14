add_library('minim')
import random, os
path = os.getcwd()
audio = Minim(this)

WIDTH = 600
HEIGHT = 900

#loading all the images we require in our game
MONSTER_LIST=[[loadImage(path + "/images/" + "monster00.png"),loadImage(path + "/images/" + "monster01.png")],[loadImage(path + "/images/" + "monster10.png"),loadImage(path + "/images/" + "monster11.png")]]
boss_monster=[loadImage(path + "/images/" + "0001.png"),loadImage(path + "/images/" + "0002.png"),loadImage(path + "/images/" + "0003.png"),loadImage(path + "/images/" + "0004.png"),loadImage(path + "/images/" + "0005.png"),loadImage(path + "/images/" + "0006.png")]

mainplayer=[loadImage(path + "/images/" + "player1.png"),loadImage(path + "/images/" + "player2.png"),loadImage(path + "/images/" + "player3.png"),loadImage(path + "/images/" + "player4.png")]
end1=[loadImage(path + "/images/" + "g1.png"),loadImage(path + "/images/" + "g2.png"),loadImage(path + "/images/" + "g3.png"),loadImage(path + "/images/" + "g4.png"),loadImage(path + "/images/" + "g5.png"),loadImage(path + "/images/" + "g6.png")]
start1=[loadImage(path + "/images/" + "0061.png"),loadImage(path + "/images/" + "0065.png"),loadImage(path + "/images/" + "0069.png"),loadImage(path + "/images/" + "0073.png"),loadImage(path + "/images/" + "0077.png"),loadImage(path + "/images/" + "0078.png")]
over=loadImage(path +"/images/"+"PROCRASTINATION.png")
start2=loadImage(path +"/images/"+"3.png")
start3=loadImage(path +"/images/"+"4.png")
start4=loadImage(path +"/images/"+"5.png")
start5=loadImage(path +"/images/"+"6.png")
start6=loadImage(path +"/images/"+"7.png")
start7=loadImage(path +"/images/"+"8.png")
pausex=loadImage(path +"/images/"+"11.png")
backgroundx=loadImage(path +"/images/"+"9.png")

#this controls the game flow of our game(0 and 1 are the different types of monsters while -1 asks the game to stop adding new monsters till all the old ones exist)
LEVEL=[0,0,0,0,-1,0,0,1,1,-1,1,1,1,1]

#the setup function and the draw function
def setup():
    size(WIDTH,HEIGHT)
    frameRate(10)
    
#we use all our game variables in a way that lets us show the images in a particular order
def draw():
    background(0)
    if game.start==0 and game.pause==0 and game.game_over==0 and game.win==0:
        fill(255,0,0)
        textSize(30)
        text('SCORE: '+str(game.score),100,50)
        text('LIVES: '+str(game.player.lives),400,50)
        game.display()
    elif game.win==1:
        
        image(over,0,0)
        fill(255,0,0)
        textSize(30)
        text('SCORE: '+str(game.score),250,450)
    elif game.start==1:
        image(start1[frameCount%6],0,0)
    elif game.start==2:
        image(start2,0,0)
    elif game.start==3:
        image(start3,0,0)
    elif game.start==4:
        image(start4,0,0)
    elif game.start==5:
        image(start5,0,0)
    elif game.start==6:
        image(start6,0,0)
    elif game.start==7:
        image(start7,0,0)
    elif game.pause==1:
        image(pausex,0,0)
        
    elif game.game_over==1:
        image(end1[frameCount%6],0,0)
        fill(255,0,0)
        textSize(30)
        text('*BACKSPACE',250,450)
        text('SCORE: '+str(game.score),100,50)
    elif game.win==1:
        image(over,0,0)
#the following functions help us track the button we click on our keyboard, pressing left will move our block one column to the left and pressing right will move it to the right
#pressing enter pauses our game and pressign BACKSPACE resets it
def keyPressed():
    if key == ENTER or key==RETURN:
        if game.pause==0 and game.start==0 and game.game_over==0:
            game.pause=1
        elif game.pause==1 and game.start==0 and game.game_over==0:
            game.pause=0
        if game.game_over==1:
            game.player.lives=10
            game.game_over=0
    if key==BACKSPACE and (game.win==1 or game.game_over==1 or game.pause==1):
        game.count=0
        game.win=0
        game.score=0
        game.game_over=0
        game.monster_list=[]
        game.boss=BossMonster(250,20)
        game.player=Player(WIDTH/2,HEIGHT-100)
           
    if keyCode == LEFT:
        game.player.movement_key[LEFT] = True
    elif keyCode == RIGHT:
        game.player.movement_key[RIGHT] = True

def keyReleased():
    if keyCode == LEFT:
        game.player.movement_key[LEFT] = False
    elif keyCode == RIGHT:
        game.player.movement_key[RIGHT] = False
        
##Clicking the mouse button is used in shooting projectiles and to move the story forward initially    
def mousePressed():
    if game.player.g==0 and game.start==0:
        game.player.g=1
    if game.start!=0:
        game.start+=1
        if game.start>7:
            game.start=0
def mouseReleased():
    game.player.g=0
    
#defining a simple class from whcih our other classes will inherit    
class SimpleObject:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        
#the projectile class helps us create the three types of projectiles seen in the game        
class Projectile(SimpleObject):
    def __init__(self,p,x,y):
        SimpleObject.__init__(self,x,y)
        self.p=p
    def update(self):
        if self.p==1:
            self.vy=-12
        elif self.p==0:
            self.vy=13
        else:
            self.vy=15
        self.y+=self.vy
    def display(self):
        self.update()
        if self.p==1:
            fill(0,0,255)
            rect(self.x,self.y,5,25)

        elif self.p==0:
            fill(250,0,0)
            ellipse(self.x,self.y,10,10)
        else:
            fill(0,250,0)
            rect(self.x,self.y,30,50)
                
        
#this is the player class which creates the character we will control in the game, we use a dictionary to help us with the movement and append projectiles to a list when we click the mouse button 
       
class Player(SimpleObject):
    def __init__(self,x,y):
        SimpleObject.__init__(self,x,y)
        self.projectile_list=[]
        self.movement_key={LEFT:False,RIGHT:False}
        self.g=0
        self.last_proj=0
        self.lives=10
    def update(self):
        if self.movement_key[LEFT] and self.x>5:
            self.vx=-10
        elif self.movement_key[RIGHT] and self.x<WIDTH-60:
            self.vx=+10
        else:
            self.vx=0
        if self.g==1 and frameCount-self.last_proj>5:
            self.last_proj=frameCount
            self.projectile_list.append(Projectile(1,self.x+30,self.y))
        self.x+=self.vx
    def display(self):
        self.update()
        for i in self.projectile_list:
            if i.y<0:
                self.projectile_list.remove(i)
            i.display()
        image(mainplayer[frameCount%4],self.x,self.y,80,80)

#the monster class creates the two types of simple monsters we see in the game, we initialise one to shoot projectiles and the other to move faster       
 
class Monster(SimpleObject):
    def __init__(self,num,x,y):
        SimpleObject.__init__(self,x,y)
        self.num=num
        self.projectile_list=[]
        if self.num==0:
            self.vy=5
        else:
            self.vy=3
    def update(self):
        self.y+=self.vy
        if self.num==1:
            self.a=random.randint(0,50)
            if self.a==1:
                self.projectile_list.append(Projectile(0,self.x+20,self.y+20))
                    
    def display(self):
        self.update()
        for i in self.projectile_list:
            i.display()
        for j in self.projectile_list:
            if j.y>900:
                self.projectile_list.remove(j)
        if self.num==0:
            #fill(50,0,20)
            #ellipse(self.x,self.y,40,40)
            image(MONSTER_LIST[0][frameCount%2],self.x,self.y,40,40)
        else:
            #fill(0,200,20)
            #ellipse(self.x,self.y,40,40)
            image(MONSTER_LIST[1][frameCount%2],self.x,self.y,40,40)
            
#the boss monster is the final monster of the game, we use the class methods to create its two attacks and random movement patterns           
 
class BossMonster(SimpleObject):
    def __init__(self,x,y):
        SimpleObject.__init__(self,x,y)
        self.projectile_list=[]
        self.lives=50
#the first attack consists of throwing three projectiles similar to the ones our simple monster threw
    def attack1(self):
        self.projectile_list.append(Projectile(0,self.x+40,self.y+200))
        self.projectile_list.append(Projectile(0,self.x+160,self.y+200))
        self.projectile_list.append(Projectile(0,self.x+100,self.y+200))
#these projectiles are larger and move faster        
    def attack2(self):
        for f in range(6):
            self.projectile_list.append(Projectile('x',random.randint(0,570),random.randint(-100,0)))
#the following methods decide to move the boss monster randomly
    def tele_left(self):
        if self.x>=200:
            self.x-=100
    def tele_right(self):
        if self.x<=390:
            self.x+=100
#within the update function we extensively use frameCount to move the monster down and use attacks    
    def update(self):
        if frameCount%50==0:
            self.y+=30
        else:
            if frameCount%20==0:
                self.z=random.randint(0,1)
                if self.z==0:
                    self.tele_right()   
                else:
                    self.tele_left()
            if frameCount%33==0: 
                self.u=random.randint(0,1)
                if self.u==0:
                    self.attack1()   
                else:
                    self.attack2()
    def display(self):
        for a in self.projectile_list:
            a.display()
        for d in self.projectile_list:
            if d.y>900:
                self.projectile_list.remove(d)
        image(boss_monster[frameCount%6],self.x,self.y,200,200)
        self.update()
                
                      
#the game class brings together all the components we have created previously and also hols attributes which will help us start/restart/pause the game

class Game:
    def __init__(self):
        self.player=Player(WIDTH/2,HEIGHT-100)
        self.monster_list=[]
        self.boss=BossMonster(250,20)
        self.k=0
        self.count=0    
        self.background_sound = audio.loadFile(path + "/sounds/background.mp3")
        self.background_sound.rewind()
        self.background_sound.loop()
        self.start=1
        self.game_over=0
        self.pause=0
        self.win=0
        self.continue_play=0
        self.restart=0
        self.score=0
        self.collision_sound = audio.loadFile(path + "/sounds/collision.mp3")
        
#this method adds a row of monster depending on our levels list        
    def add_monster_row(self):
        if len(self.monster_list)==0 or self.monster_list[-1].y>70:
            self.k=LEVEL[self.count]
            for i in range(6):
                self.monster_list.append(Monster(self.k,80*(i+1),0))
            self.count+=1
#this method checks for collisions between projectiles and monsters/players    
    def collision(self):
        for i in self.monster_list:
            for j in self.player.projectile_list:
                if (((i.x+20)-(j.x+2.5))**2 + ((i.y+20)-(j.y+12.5))**2)<=(32.5)**2 and j.x<=i.x+40 and j.x>=i.x:
                    self.collision_sound.rewind()
                    self.collision_sound.play()
                    self.monster_list.remove(i)
                    self.player.projectile_list.remove(j)
                    self.score+=1
        for i in self.monster_list:
            for j in i.projectile_list:
                if (j.x-(self.player.x+40))**2 + (j.y-(self.player.y+40))**2<=40**2:
                    self.collision_sound.rewind()
                    self.collision_sound.play()
                    self.player.lives-=1
                    i.projectile_list.remove(j)
        for i in self.boss.projectile_list:
            if i.p==0:
                if (i.x-(self.player.x+40))**2 + (i.y-(self.player.y+40))**2<=40**2:
                    self.collision_sound.rewind()
                    self.collision_sound.play()
                    self.player.lives-=1
                    self.boss.projectile_list.remove(i)
            else:
                if ((i.x+15)-(self.player.x+40))**2 + ((i.y+25)-(self.player.y+40))**2<=65**2 and i.x<self.player.x+50 and i.x>=self.player.x:
                    self.collision_sound.rewind()
                    self.collision_sound.play()
                    self.player.lives-=1
                    self.boss.projectile_list.remove(i)
                    
        for j in self.player.projectile_list:
                if (((self.boss.x+100)-(j.x+2.5))**2 + ((self.boss.y+100)-(j.y+12.5))**2)<=(112.5)**2 and j.x<=self.boss.x+200 and j.x>=self.boss.x:
                    self.collision_sound.rewind()
                    self.collision_sound.play()
                    self.boss.lives-=1
                    self.player.projectile_list.remove(j)
                    self.score+=1
        if self.boss.lives==0:
            self.win=1
        if self.player.lives<=0:
            self.game_over=1
#calls our collision method and ontrols our add_monster_row method
    def update(self):
        self.collision()
        if self.count<=13 and (len(self.monster_list)==0 or LEVEL[self.count]==1 or LEVEL[self.count]==0):
            if len(self.monster_list)==0:
                self.count+=1
            self.add_monster_row()
#used for displaying everyhting
    def display(self):
        self.player.display()
        for n in self.monster_list:
            n.display()
        for l in self.monster_list:
            if l.y>850:
                self.monster_list.remove(l)
                self.player.lives-=1
        if self.count>13 and len(self.monster_list)==0:
            self.boss.display()
        if self.player.lives<=0:
            self.game_over=1
        if self.boss.y>200:
            self.game_over=1
        self.update()
game=Game()
            
