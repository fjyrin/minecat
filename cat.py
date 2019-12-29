import sys, pygame, json
from os import path
from pygame.locals import *
from floatrect import FloatRect
from collision import collision_delta
pygame.init()

clock = pygame.time.Clock()
edit_type = 0

if path.exists('world.json'):
    map = json.load(open('world.json'))
    tilesize = map["tilesize"]
    mapsize = mapwidth, mapheight = map["mapwidth"], map["mapheight"]
    tiles = map["tiles"]
else:
    mapwidth = 40
    mapheight = 20
    tiles = [
        [
            1 if x in (0,mapwidth-1) or y in (0,mapheight-1) else 0 
            for x in range(mapwidth)
        ] for y in range(mapheight) 
    ]
    tilesize = 32
    
    


size = width, height = mapwidth * tilesize, mapheight * tilesize
wallcolor = pygame.Color(50,50,50)

speed = [0.0, 0.0]
position = [42.0, 42.0]
black = 0, 0, 0

screen = pygame.display.set_mode(size, flags=pygame.DOUBLEBUF)

ball = pygame.image.load("nyan01.png")

font = pygame.font.SysFont("Comic Sans",20)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            map = {
                "tiles":tiles, 
                "mapheight":mapheight, 
                "mapwidth":mapwidth,
                "tilesize":tilesize
            }
            json.dump(map, open('world.json', 'w'))
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                speed[1] = -3
            elif event.key == K_a:
                speed[0] -= 1
            elif event.key == K_d:
                speed[0] += 1
            elif event.key == K_MINUS:
                edit_type = max(0, edit_type-1)
            elif event.key == K_EQUALS:
                edit_type = min(2, edit_type+1)

        if event.type == pygame.KEYUP:
            if event.key == K_a:
                speed[0] += 1
            elif event.key == K_d:
                speed[0] -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                xtile = event.pos[0]//tilesize
                ytile = event.pos[1]//tilesize
                tiles[ytile][xtile] = edit_type

            

    speed[1] = min(speed[1] + 0.05, 3)

    position[0] += speed[0]
    position[1] += speed[1]

    collectangle = FloatRect(position[0], position[1], ball.get_width(), ball.get_height())
    dx, dy = collision_delta(collectangle,speed,tiles,tilesize)
    position[0] += dx
    position[1] += dy
    ballrect = ball.get_rect().move(position[0], position[1])

    # update display
    screen.fill(black)
    for y in range(mapheight):
        for x in range(mapwidth):
            if tiles[y][x] == 1:
                rect = pygame.Rect(x*tilesize, y*tilesize, tilesize, tilesize)
                pygame.draw.rect(screen, wallcolor, rect)

    screen.blit(ball, ballrect)
    debugtext = font.render("{},{}".format(dx,dy),True,(255,255,255))
    screen.blit(debugtext,(0,0))

    clock.tick(144)
    pygame.display.flip()