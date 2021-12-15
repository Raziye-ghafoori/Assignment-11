import random
import arcade
import time
import math

SCREEN_WIDTH=500
SCREEN_HEIGHT=500
        
class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width=15
        self.color1=arcade.color.PAKISTAN_GREEN
        self.color2=arcade.color.NAPIER_GREEN
        self.color3=arcade.color.BLACK
        self.center_x=SCREEN_WIDTH//2
        self.center_y=SCREEN_HEIGHT//2
        self.score=0
        self.change_x=0
        self.change_y=0
        self.speed=7
        self.R=10
        self.body=[]
        self.body_size=1

    def move(self):
        self.body.append([self.center_x,self.center_y])
        
        if len(self.body)>self.score:
            self.body.pop(0)
        
        if self.change_x>0:
            self.center_x+=self.speed
        
        elif self.change_x<0:
            self.center_x-=self.speed
            
        elif self.change_y>0:
            self.center_y+=self.speed
            
        elif self.change_y<0:
            self.center_y-=self.speed
            

        
        if self.center_y < 0   or  self.center_y > 500 : 
            arcade.start_render()
            text = "GAME OVER"
            arcade.draw_text(text, 250, 250, arcade.color.RED, 50, anchor_x='center')
            arcade.finish_render()
            time.sleep(3)
            exit()
            
        
        if self.center_x < 0   or  self.center_x > 500 : 
            arcade.start_render()
            text = "GAME OVER"
            arcade.draw_text(text, 250, 250, arcade.color.RED, 50, anchor_x='center')
            arcade.finish_render()
            time.sleep(3)
            exit()


    def eat(self,food):
        if food=="apple":
            self.score+=1
            self.body_size+=1
        elif food=="pear":
            self.score+=2
            self.body_size+=2
        elif food=="poop":
            self.score-=1
            self.body_size-=1
            if self.body_size==0:
                arcade.start_render()
                text = "GAME OVER"
                arcade.draw_text(text, 250, 250, arcade.color.RED, 50, anchor_x='center')
                arcade.finish_render()
                time.sleep(3)
                exit()
        
    def draw(self):
        
        for i in range(len(self.body)):
            arcade.draw_circle_filled(self.body[i][0],self.body[i][1],self.R,self.color2)
        
        arcade.draw_circle_filled(self.center_x,self.center_y,self.R,self.color1)
        arcade.draw_circle_filled(self.center_x-2,self.center_y,3,self.color3)
        arcade.draw_circle_filled(self.center_x+5,self.center_y,3,self.color3)

class Apple(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width=20
        self.height=20
        self.center_x=random.randint(5,SCREEN_WIDTH-5)
        self.center_y=random.randint(5,SCREEN_HEIGHT-5)
        self.pecture_apple=arcade.load_texture("apple.png")
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center_x,self.center_y,self.width,self.height,self.pecture_apple)

class Pear(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width=20
        self.height=20
        self.center_x=random.randint(5,SCREEN_WIDTH-5)
        self.center_y=random.randint(5,SCREEN_HEIGHT-5)
        self.pecture_pear=arcade.load_texture("pear.png")
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center_x,self.center_y,self.width,self.height,self.pecture_pear)

class Poop(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width=20
        self.height=20
        self.center_x=random.randint(5,SCREEN_WIDTH-5)
        self.center_y=random.randint(5,SCREEN_HEIGHT-5)
        self.pecture_poop=arcade.load_texture("poop.png")
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center_x,self.center_y,self.width,self.height,self.pecture_poop)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH,height=SCREEN_HEIGHT,title="🐍Snake Game🐍")
        arcade.set_background_color(arcade.color.PALE_AQUA)
        self.snake=Snake()
        self.apple=Apple()
        self.poop=Poop()
        self.pear=Pear()

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.pear.draw()
        self.poop.draw()
        arcade.draw_text("SCORE::"+str(self.snake.score),20,460,arcade.color.PERSIAN_PLUM,20)
    
    def on_update(self, delta_time: float):
       
        food_center_x=0
        food_center_y=0
        if   math.sqrt((self.snake.center_x-self.apple.center_x)**2+(self.snake.center_y-self.apple.center_y)**2)<math.sqrt((self.snake.center_x-self.pear.center_x)**2+(self.snake.center_y-self.pear.center_y)**2):
            food_center_x=self.apple.center_x
            food_center_y=self.apple.center_y
            
        else :
            food_center_x=self.pear.center_x   
            food_center_y=self.pear.center_y
        
        open_way_top=True
        open_way_down=True
        open_way_right=True
        open_way_left=True

        if self.snake.center_x<self.poop.center_x and self.poop.center_y==self.snake.center_y:
            open_way_right=False
        elif self.snake.center_x>self.poop.center_x and self.poop.center_y==self.snake.center_y:
            open_way_left=False
        elif self.snake.center_x==self.poop.center_x and self.poop.center_y>self.snake.center_y:
            open_way_top=False
        elif self.snake.center_x==self.poop.center_x and self.poop.center_y<self.snake.center_y:
            open_way_down=False
        
        if open_way_top and self.snake.center_y <  food_center_y:
            self.snake.change_y = 1
            self.snake.change_x = 0
            self.snake.move()
            
        if open_way_left and self.snake.center_x> food_center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            self.snake.move()
               
        if open_way_down and self.snake.center_y> food_center_y:
            self.snake.change_y = -1
            self.snake.change_x = 0
            self.snake.move()
            
        if  open_way_right and self.snake.center_x < food_center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            self.snake.move()
            
        #self.snake.move()

        if arcade.check_for_collision(self.snake,self.apple):
            self.snake.eat("apple")
            self.apple=Apple()
            if arcade.check_for_collision(self.pear,self.apple):
                self.apple=Apple()
            if arcade.check_for_collision(self.poop,self.apple):
                self.apple=Apple()
        elif arcade.check_for_collision(self.snake,self.pear):
            self.snake.eat("pear")
            self.pear=Pear()
            if arcade.check_for_collision(self.pear,self.apple):
                self.apple=Pear()
            if arcade.check_for_collision(self.poop,self.pear):
                self.apple=Pear()
        elif arcade.check_for_collision(self.snake,self.poop):
            self.snake.eat("poop")
            self.poop=Poop()
            if arcade.check_for_collision(self.poop,self.apple):
                self.apple=Poop()
            if arcade.check_for_collision(self.poop,self.pear):
                self.apple=Poop()

    #def on_key_release(self, key: int, modifiers: int):
    #    if key==arcade.key.LEFT:
    #        self.snake.change_x =-1
    #        self.snake.change_y =0
    #    if key==arcade.key.RIGHT:
    #        self.snake.change_x =1
    #        self.snake.change_y =0
    #    if key==arcade.key.UP:
    #        self.snake.change_y =1
    #        self.snake.change_x=0
    #    if key==arcade.key.DOWN:
    #        self.snake.change_y =-1
    #        self.snake.change_x =0
            
        
my_game=Game()
arcade.run()
