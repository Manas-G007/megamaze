import pygame as pyg
import game_object as go
import text as txt
import random
from time import sleep
import levels

pyg.init()

# screen config
screen_size=500,500
pyg.display.set_mode(screen_size)
img=pyg.image.load("assets/maze_logo.png")
pyg.display.set_icon(img)

screen=pyg.display.set_mode(screen_size)
disp=pyg.display

# global parameters
running=True
unit_size=50
# generate random levels
trees_pos=[
   [random.randint(0,screen_size[0]//unit_size) for _ in range(random.randint(0,screen_size[0]//unit_size))]
   for _ in range(screen_size[0]//unit_size)
]
# trees_pos=levels.level1
winState=False
gameSpeed=15
counter=10


# game object
player=go.GameObject("assets/player.png",0,0,0,unit_size)
bg=go.GameObject("assets/bg.png",0,0,0,0)
winObj=go.GameObject("assets/win.png",screen_size[0]-unit_size,screen_size[0]-unit_size,0,0)

trees=[]
for i in range(len(trees_pos)):
    for j in range(len(trees_pos[i])):
        trees.append(go.GameObject("assets/tree.png",
                                   trees_pos[i][j]*unit_size,
                                   i*unit_size,
                                   0,0))

def keyboardControl(key):
    if key==pyg.K_RIGHT:
        player.changeSpeedX(player.speed)
        player.changeSpeedY(0)
    elif key==pyg.K_LEFT:
        player.changeSpeedX(-player.speed)
        player.changeSpeedY(0)
    elif key==pyg.K_DOWN:
        player.changeSpeedY(player.speed)
        player.changeSpeedX(0)
    elif key==pyg.K_UP:
        player.changeSpeedY(-player.speed)
        player.changeSpeedX(0)

def boundaryCheck(gameObject):
    if gameObject.x < 0:
        gameObject.x = 0
        gameObject.changeSpeedX(0)
    if gameObject.x > screen_size[0] - unit_size:
        gameObject.x = screen_size[0] - unit_size
        gameObject.changeSpeedX(0)
    if gameObject.y < 0:
        gameObject.y = 0
        gameObject.changeSpeedY(0)
    if gameObject.y > screen_size[1] - unit_size:
        gameObject.y = screen_size[1] - unit_size
        gameObject.changeSpeedY(0)

        
# tuffest function
def boundaryBlock(gameObject):
    # Calculate future positions based on current speed
    future_x = gameObject.x + gameObject.speedX
    future_y = gameObject.y + gameObject.speedY
    
    for tree in trees:
        if gameObject.speedX > 0:  # Moving right
            if future_x == tree.x and gameObject.y == tree.y:
                gameObject.changeSpeedX(0)
        elif gameObject.speedX < 0:  # Moving left
            if future_x == tree.x and gameObject.y == tree.y:
                gameObject.changeSpeedX(0)
        
        if gameObject.speedY > 0:  # Moving down
            if gameObject.x == tree.x and future_y == tree.y:
                gameObject.changeSpeedY(0)
        elif gameObject.speedY < 0:  # Moving up
            if gameObject.x == tree.x and future_y == tree.y:
                gameObject.changeSpeedY(0)


def winCheck():
    global winState
    
    winState=True if (player.x==winObj.x) and (player.y==winObj.y) else False

def updatePos(gameObject):
    gameObject.changeX(gameObject.x+gameObject.speedX)
    gameObject.changeY(gameObject.y+gameObject.speedY) 

def render(gameObject,bgBool):
    if bgBool:
        gameObject.image = pyg.transform.scale(gameObject.image,screen_size)
    else:
        gameObject.image = pyg.transform.scale(gameObject.image,(unit_size,unit_size))
    screen.blit(gameObject.image,(gameObject.x,gameObject.y))

def renderText(text,x,y):
    screen.blit(
        txt.Text(text,(0,0,0)).text,(x,y))

def update():
    global running,counter,winState
    # events
    for event in pyg.event.get():
        if event.type==pyg.QUIT:
            running=False

        if event.type==pyg.KEYDOWN:
            keyboardControl(event.key)

        if event.type==pyg.KEYUP:
            player.changeSpeedX(0)
            player.changeSpeedY(0)


    boundaryBlock(player)

    # updating position
    updatePos(player)

    # boundary check
    boundaryCheck(player)

    # win check
    winCheck()

    # render game object
    for _ in range(gameSpeed):
        render(bg,True)
    if winState:
        if counter==0:
            player.changeX(0)
            player.changeY(0)
            counter=15
            winState=False
            return 
    
        renderText("You Won !",
                   screen_size[0]//2 - unit_size*1.8,
                   screen_size[0]//2 - unit_size*0.5)
        sleep(1)
        renderText(f"Game Restart in {counter}",
                   screen_size[0]//2 - unit_size*3.5,
                   screen_size[0]//2 + unit_size)
        counter-=1
    else:
        render(winObj,False)
        render(player,False)
        for tree in trees:
            render(tree,False)
        
    # updating per frame
    disp.update()

def main():
    while running:
        update()

if __name__=="__main__":
    main()