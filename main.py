from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
polygons = []
transform = new_matrix()
# add_polygon( polygons, 50, 50, 0, 100, 400, 0, 250, 400, 0 )
# clear_screen(screen)
# draw_polygons( polygons, screen, color )
# display(screen)
parse_file( 'script', edges, polygons, transform, screen, color )
