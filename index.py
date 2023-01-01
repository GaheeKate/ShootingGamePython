import pygame
import random
from time import sleep

# variables for game
bg_col = (0, 0, 0)
pad_width = 480
pad_height = 640
spaceship_width = 64
spaceship_height = 64
enemy_width = 64
enemy_height = 64

# score count


def drawScore(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Kills: ' + str(count), True, (255, 255, 255))
    gamepad.blit(text, (0, 0))


# missed enemy count
def drawPassed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Missed: ' + str(count), True, (255, 0, 0))
    gamepad.blit(text, (360, 0))


# display msg
def dispMsg(text):
    global gamepad
    textfont = pygame.font.Font('freesansbold.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

# crashed msg


def crash():
    global gamepad
    dispMsg('Crashed!')

# game over msg


def gameover():
    global gamepad
    dispMsg('Game Over!')


# draw object on screen(x,y)
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


# main functions for starting
def runGame():
    global gamepad, clock, spaceship, enemy, bullet

    # bullet
    bulletList = []

    # Check hit
    isShot = False
    shotcount = 0
    enemypassed = 0

    # set default position of spaceship
    x = pad_width*0.43
    y = pad_height*0.9
    x_change = 0

    # set default position of enemy
    enemy_x = random.randrange(0, pad_width-enemy_width)
    enemy_y = 0
    enemy_speed = 3

    ongame = False
    while not ongame:
        for event in pygame.event.get():  # return event
            if event.type == pygame.QUIT:  # close screen with a mouse
                ongame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5
                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                # 2 bullets max
                elif event.key == pygame.K_SPACE:
                    if len(bulletList) < 2:
                        bullet_x = x + spaceship_width/2
                        bullet_y = y - spaceship_height
                        bulletList.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0  # reset change value to 0

        gamepad.fill(bg_col)

        # show bullet
        if len(bulletList) != 0:
            for i, bxy in enumerate(bulletList):
                bxy[1] -= 10
                bulletList[i][1] = bxy[1]  # y value minus 10

                # add score count
                if bxy[1] < enemy_y:  # when bullet y < enemy y and bullet x is in between enemy x and enemy x + width, remove the bullet from list and add one shot count
                    if bxy[0] > enemy_x and bxy[0] < enemy_x+enemy_width:
                        bulletList.remove(bxy)
                        isShot = True
                        shotcount += 1
                if bxy[1] <= 0:  # if y value is 0 or less remove from list
                    try:
                        bulletList.remove(bxy)
                    except:
                        pass

        if len(bulletList) != 0:
            for bx, by in bulletList:
                drawObject(bullet, bx, by)

        drawScore(shotcount)

        # set spaceship position by the x_change value
        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - spaceship_width:
            x = pad_width - spaceship_width

        drawObject(spaceship, x, y)

        # set spaceship position by the x_change value

        enemy_y += enemy_speed
        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width-enemy_width)
            enemypassed += 1

        if enemypassed == 3:  # 3 life
            gameover()

        drawPassed(enemypassed)

        # speed up to 10
        if isShot:
            enemy_speed += 1
            if enemy_speed >= 10:
                enemy_speed = 10
            enemy_x = random.randrange(0, pad_width-enemy_width)
            enemy_y = 0
            isShot = False

        drawObject(enemy, enemy_x, enemy_y)

        pygame.display.update()  # update
        # set FPS 60. It seems like requestAnimationFrame on JS that is also 60 frames per sec.
        clock.tick(60)

    pygame.quit()


# game init function
def initGame():
    global gamepad, clock, spaceship, enemy, bullet

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('SpaceshipGame')
    spaceship = pygame.image.load('img/spaceship.png')
    clock = pygame.time.Clock()
    enemy = pygame.image.load('img/enemy.png')
    bullet = pygame.image.load('img/bullet.png')


initGame()
runGame()
