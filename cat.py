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
screen = pygame.display.set_mode(size, flags=pygame.DOUBLEBUF, depth=32)

tile_graphics = {
    0 : pygame.image.load('sky.png').convert_alpha(),
    1 : pygame.image.load('grass.png').convert_alpha(),
    2 : pygame.image.load('stone.png').convert_alpha(),
    3 : pygame.image.load('log.png').convert_alpha(),
    4 : pygame.image.load('leaves.png').convert_alpha()
}
highlight = pygame.image.load('frame.png').convert_alpha()

wallcolor = pygame.Color(50,50,50)
highlightcolor = pygame.Color(255,255,0,32)

speed = [0.0, 0.0]
position = [42.0, 42.0]
black = 0, 0, 0

inventory = {1:5, 2:5, 3:5, 4:5}


ball = pygame.image.load("nyan01.png").convert_alpha()

font = pygame.font.SysFont("Comic Sans",20)

def point_is_placeable(x, y, tilesize, max_dist, player_rect):
    rect = tilerect_from_point(x, y, tilesize)
    distance_squared = (player_rect.centerx - rect.centerx)**2 + (player_rect.centery - rect.centery)**2
    return distance_squared < max_dist**2 and not player_rect.colliderect(rect)

def tilerect_from_point(x, y, tilesize):
    tile_x = x // tilesize
    tile_y = y // tilesize
    return pygame.Rect(tile_x*tilesize, tile_y*tilesize, tilesize, tilesize)

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
                edit_type = min(4, edit_type+1)

        if event.type == pygame.KEYUP:
            if event.key == K_a:
                speed[0] += 1
            elif event.key == K_d:
                speed[0] -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1 and point_is_placeable(x, y, tilesize, 96, ballrect):
                xtile = x//tilesize
                ytile = y//tilesize
                tile_type = tiles[ytile][xtile]
                if edit_type == 0:
                    if tile_type > 0:
                        tiles[ytile][xtile] = edit_type
                        inventory[tile_type] += 1
                elif tile_type == 0:
                    if inventory[edit_type] > 0:
                        tiles[ytile][xtile] = edit_type
                        inventory[edit_type] -= 1
                

            

    speed[1] = min(speed[1] + 0.05, 3)

    position[0] += speed[0]
    position[1] += speed[1]

    collectangle = FloatRect(position[0], position[1], ball.get_width(), ball.get_height())
    dx, dy = collision_delta(collectangle,speed,tiles,tilesize)
    position[0] += dx
    position[1] += dy
    ballrect = ball.get_rect().move(position[0], position[1])

    # update display
    for y in range(mapheight):
        for x in range(mapwidth):
            rect = pygame.Rect(x*tilesize, y*tilesize, tilesize, tilesize)
            screen.blit(tile_graphics[tiles[y][x]], rect)

    # check cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if point_is_placeable(mouse_x, mouse_y, tilesize, 96, ballrect):
        screen.blit(highlight, tilerect_from_point(mouse_x, mouse_y, tilesize))
    
    
    screen.blit(ball, ballrect)

    # render inventory
    inv_rect = pygame.Rect(tilesize/2, tilesize/2, (tilesize+2)*4 + 2, tilesize+4)
    pygame.draw.rect(screen, (0,0,0), inv_rect)
    for id, count in inventory.items():
        item_rect = pygame.Rect(inv_rect.left+2 + (id-1)*(tilesize+2), inv_rect.top+2, tilesize, tilesize)
        screen.blit(tile_graphics[id], item_rect)
        count_text = font.render(str(count),True,(255,255,255))
        screen.blit(count_text, item_rect.center)
        if id == edit_type:
            screen.blit(highlight, item_rect)

    debugtext = font.render("1:{}, 2:{}, Sel:{}".format(inventory[1],inventory[2],edit_type),True,(255,255,255))
    screen.blit(debugtext,(0,0))

    clock.tick(144)
    pygame.display.flip()
