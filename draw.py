from display import *
from matrix import *

def mag(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def norm(v):
    return [v[0]/mag(v), v[1]/mag(v), v[2]/mag(v)]

def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, color ):
    if len(polygons) < 3:
        return

    point = 0
    while point < len(polygons) - 1:
        a = [polygons[point+1][0] - polygons[point][0], polygons[point+1][1] - polygons[point][1], polygons[point+1][2] - polygons[point][2]]
        b = [polygons[point+2][0] - polygons[point][0], polygons[point+2][1] - polygons[point][1], polygons[point+2][2] - polygons[point][2]]
        c = [polygons[point+2][0] - polygons[point+1][0], polygons[point+2][1] - polygons[point+1][1], polygons[point+2][2] - polygons[point+1][2]]

        maga = mag(a)
        magb = mag(b)
        magc = mag(c)

        eps = .005
        draw = False
        if maga < eps or magb < eps or magb < eps:
            draw = True
        else:
            crossAB = cross(a,b)
            n = norm(crossAB)
            dot =  n[2]
            if dot > 0 and dot < 1:
                draw = True
        if draw == True:
            draw_line( int(polygons[point][0]),
                       int(polygons[point][1]),
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       screen, color)
            draw_line( int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       screen, color)
            draw_line( int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       int(polygons[point][0]),
                       int(polygons[point][1]),
                       screen, color)


        point+= 3

def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( polygons, x, y, z, x, y1, z, x1, y, z)
    add_polygon( polygons, x1, y1, z, x1, y, z, x, y1, z)

    #back
    add_polygon( polygons, x1, y1, z1, x, y1, z1, x1, y, z1)
    add_polygon( polygons, x, y, z1, x1, y, z1, x, y1, z1)

    #top
    add_polygon( polygons, x, y, z, x1, y, z, x, y, z1)
    add_polygon( polygons, x1, y, z1, x, y, z1, x1, y, z)

    #bottom
    add_polygon( polygons, x1, y, z1, x1, y1, z, x, y1, z1)
    add_polygon( polygons, x, y1, z, x, y1, z1, x1, y1, z)

    #left
    add_polygon( polygons, x, y, z, x, y, z1, x, y1, z)
    add_polygon( polygons, x, y1, z1, x, y1, z, x, y, z1)

    #right
    add_polygon( polygons, x1, y1, z1, x1, y, z1, x1, y1, z)
    add_polygon( polygons, x1, y, z, x1, y1, z, x1, y, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1

    for longt in range(longt_start, longt_stop+1):
        index = longt
        add_point(points, points[index][0],
                 points[index][1],
                 points[index][2])

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            index = lat * step + longt
            if longt == 0:
                add_polygon(polygons,
                            points[index][0],
                            points[index][1],
                            points[index][2],
                            points[index + 1][0],
                            points[index + 1][1],
                            points[index + 1][2],
                            points[index + step + 1][0],
                            points[index + step + 1][1],
                            points[index + step + 1][2])
            else:
                add_polygon(polygons,
                            points[index][0],
                            points[index][1],
                            points[index][2],
                            points[index + 1][0],
                            points[index + 1][1],
                            points[index + 1][2],
                            points[index + step][0],
                            points[index + step][1],
                            points[index + step][2])
                add_polygon(polygons,
                            points[index + 1][0],
                            points[index + 1][1],
                            points[index + 1][2],
                            points[index + step + 1][0],
                            points[index + step + 1][1],
                            points[index + step + 1][2],
                            points[index + step][0],
                            points[index + step][1],
                            points[index + step][2])

def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step
    for longt in range(longt_start, longt_stop):
        index = longt
        add_point(points, points[index][0],
                 points[index][1],
                 points[index][2])

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            index = lat * step + longt

            add_polygon(polygons,
                        points[index][0],
                        points[index][1],
                        points[index][2],
                        points[index + 1][0],
                        points[index + 1][1],
                        points[index + 1][2],
                        points[index + step][0],
                        points[index + step][1],
                        points[index + step][2])

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
