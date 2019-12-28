def collision_delta(rect, velocity, map, tilesize):
    xf = x_first(rect, velocity, map, tilesize)
    yf = y_first(rect, velocity, map, tilesize)

    if xf[0]**2 + xf[1]**2 > yf[0]**2 + yf[1]**2:
        return yf
    else: 
        return xf

def x_first(rect, velocity, map, tilesize):
    spectangle = rect.copy()
    spectangle.left += x_delta(spectangle, velocity[0], map, tilesize)
    spectangle.top += y_delta(spectangle, velocity[1], map, tilesize)

    delta = (spectangle.left - rect.left, spectangle.top - rect.top)
    return delta

def y_first(rect, velocity, map, tilesize):
    spectangle = rect.copy()
    spectangle.top += y_delta(spectangle, velocity[1], map, tilesize)
    spectangle.left += x_delta(spectangle, velocity[0], map, tilesize)

    delta = (spectangle.left - rect.left, spectangle.top - rect.top)
    return delta

def x_delta(rect, xvel, map, tilesize):
    if xvel == 0:
        return 0

    top = rect.top//tilesize
    bottom = rect.bottom//tilesize
    
    if xvel > 0: #moving right
        x_limit = rect.right//tilesize

        for y in range(top,bottom+1):
            if map[y][x_limit] == 1:
                return x_limit*tilesize - rect.right - 1
        return 0

    else:
        x_limit = rect.left//tilesize

        for y in range(top,bottom+1):
            if map[y][x_limit] == 1:
                return (x_limit+1)*tilesize - rect.left
        return 0

def y_delta(rect, yvel, map, tilesize):
    if yvel == 0:
        return 0

    left = rect.left//tilesize
    right = rect.right//tilesize
    
    if yvel > 0: #moving down
        y_limit = rect.bottom//tilesize

        for x in range(left,right+1):
            if map[y_limit][x] == 1:
                return y_limit*tilesize - rect.bottom - 1
        return 0

    else:
        y_limit = rect.top//tilesize

        for x in range(left,right+1):
            if map[y_limit][x] == 1:
                return (y_limit+1)*tilesize - rect.top
        return 0    
