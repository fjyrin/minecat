import sys, pygame
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()


tilesize = tilewidth, tileheight = 32, 32
mapsize = mapwidth, mapheight = 10, 10
size = width, height = mapwidth * tilewidth, mapheight * tileheight

wallcolor = pygame.Color(50,50,50)

map =  [[1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,1,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]]

speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size, flags=pygame.DOUBLEBUF)

ball = pygame.image.load("nyan01.png")
ballrect = ball.get_rect().move(42,42)

def x_delta(rect, xvel, map):
    if xvel == 0:
        return 0

    top = rect.top//tileheight
    bottom = rect.bottom//tileheight
    
    if xvel > 0: #moving right
        x_limit = rect.right//tilewidth

        for y in range(top,bottom+1):
            if map[y][x_limit] == 1:
                return x_limit*tilewidth - rect.right - 1
        return 0

    else:
        x_limit = rect.left//tilewidth

        for y in range(top,bottom+1):
            if map[y][x_limit] == 1:
                return (x_limit+1)*tilewidth - rect.left
        return 0

def y_delta(rect, yvel, map):
    if yvel == 0:
        return 0

    left = rect.left//tilewidth
    right = rect.right//tilewidth
    
    if yvel > 0: #moving down
        y_limit = rect.bottom//tileheight

        for x in range(left,right+1):
            if map[y_limit][x] == 1:
                return y_limit*tileheight - rect.bottom - 1
        return 0

    else:
        y_limit = rect.top//tileheight

        for x in range(left,right+1):
            if map[y_limit][x] == 1:
                return (y_limit+1)*tileheight - rect.top
        return 0    

def x_first(rect, velocity, map):
    spectangle = rect.copy()
    spectangle.left += x_delta(spectangle, velocity[0], map)
    spectangle.top += y_delta(spectangle, velocity[1], map)

    delta = (spectangle.left - rect.left, spectangle.top - rect.top)
    return delta

def y_first(rect, velocity, map):
    spectangle = rect.copy()
    spectangle.top += y_delta(spectangle, velocity[1], map)
    spectangle.left += x_delta(spectangle, velocity[0], map)

    delta = (spectangle.left - rect.left, spectangle.top - rect.top)
    return delta

def collision_delta(rect, velocity, map):
    xf = x_first(rect, velocity, map)
    yf = y_first(rect, velocity, map)

    if xf[0]**2 + xf[1]**2 > yf[0]**2 + yf[1]**2:
        return yf
    else: 
        return xf

font = pygame.font.SysFont("Comic Sans",20)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                speed[1] -= 1
            elif event.key == K_a:
                speed[0] -= 1
            elif event.key == K_s:
                speed[1] += 1
            elif event.key == K_d:
                speed[0] += 1

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                speed[1] += 1
            elif event.key == K_a:
                speed[0] += 1
            elif event.key == K_s:
                speed[1] -= 1
            elif event.key == K_d:
                speed[0] -= 1


    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = 0
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = 0

    dx, dy = collision_delta(ballrect,speed,map)
    ballrect = ballrect.move(dx, dy)
    
    # update display
    screen.fill(black)
    for y in range(mapheight):
        for x in range(mapwidth):
            if map[y][x] == 1:
                rect = pygame.Rect(x*tilewidth, y*tileheight, tilewidth, tileheight)
                pygame.draw.rect(screen, wallcolor, rect)

    screen.blit(ball, ballrect)
    debugtext = font.render("{},{}".format(dx,dy),True,(255,255,255))
    screen.blit(debugtext,(0,0))

    clock.tick(144)
    pygame.display.flip()