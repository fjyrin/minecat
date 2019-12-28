import sys, pygame
from pygame.locals import *
from collision import collision_delta
pygame.init()

clock = pygame.time.Clock()


tilesize = 32
mapsize = mapwidth, mapheight = 10, 10
size = width, height = mapwidth * tilesize, mapheight * tilesize

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

    dx, dy = collision_delta(ballrect,speed,map,tilesize)
    ballrect = ballrect.move(dx, dy)
    
    # update display
    screen.fill(black)
    for y in range(mapheight):
        for x in range(mapwidth):
            if map[y][x] == 1:
                rect = pygame.Rect(x*tilesize, y*tilesize, tilesize, tilesize)
                pygame.draw.rect(screen, wallcolor, rect)

    screen.blit(ball, ballrect)
    debugtext = font.render("{},{}".format(dx,dy),True,(255,255,255))
    screen.blit(debugtext,(0,0))

    clock.tick(144)
    pygame.display.flip()