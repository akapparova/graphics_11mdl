import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident(tmp)
    xD = [[x[:] for x in tmp]]
    screen = new_screen()
    zbuffer = new_zbuffer()
    temp = []
    step_3d = 20
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
        for command in commands:
            line = command[0]
            if (len(command) > 1):
                args = command[1:]
            if line == 'sphere':
                #print 'SPHERE\t' + str(args)
                add_sphere(temp,
                           float(args[0]), float(args[1]), float(args[2]),
                           float(args[3]), step_3d)
                matrix_mult( xD[-1], temp )
                draw_polygons(temp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                temp = []

            elif line == 'torus':
                #print 'TORUS\t' + str(args)
                add_torus(temp,
                          float(args[0]), float(args[1]), float(args[2]),
                          float(args[3]), float(args[4]), step_3d)
                matrix_mult( xD[-1], temp )
                draw_polygons(temp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                temp = []

            elif line == 'box':
                #print 'BOX\t' + str(args)
                add_box(temp,
                        float(args[0]), float(args[1]), float(args[2]),
                        float(args[3]), float(args[4]), float(args[5]))
                matrix_mult( xD[-1], temp )
                draw_polygons(temp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                temp = []

            elif line == 'circle':
                #print 'CIRCLE\t' + str(args)
                add_circle(edges,
                           float(args[0]), float(args[1]), float(args[2]),
                           float(args[3]), step)
                matrix_mult( xD[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []

            elif line == 'hermite' or line == 'bezier':
                #print 'curve\t' + line + ": " + str(args)
                add_curve(edges,
                          float(args[0]), float(args[1]),
                          float(args[2]), float(args[3]),
                          float(args[4]), float(args[5]),
                          float(args[6]), float(args[7]),
                          step, line)
                matrix_mult( xD[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []

            elif line == 'line':
                #print 'LINE\t' + str(args)

                add_edge( edges,
                          float(args[0]), float(args[1]), float(args[2]),
                          float(args[3]), float(args[4]), float(args[5]) )
                matrix_mult( xD[-1], edges )
                draw_lines(eges, screen, zbuffer, color)
                edges = []

            elif line == 'scale':
                #print 'SCALE\t' + str(args)
                t = make_scale(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult( xD[-1], t )
                xD[-1] = [ x[:] for x in t]

            elif line == 'move':
                #print 'MOVE\t' + str(args)
                t = make_translate(float(args[0]), float(args[1]), float(args[2]))
                matrix_mult( xD[-1], t )
                xD[-1] = [ x[:] for x in t]

            elif line == 'rotate':
                #print 'ROTATE\t' + str(args)
                theta = float(args[1]) * (math.pi / 180)
                if args[0] == 'x':
                    t = make_rotX(theta)
                elif args[0] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( xD[-1], t )
                xD[-1] = [ x[:] for x in t]

            elif line == 'push':
                xD.append( [x[:] for x in xD[-1]] )

            elif line == 'pop':
                xD.pop()

            elif line == 'display' or line == 'save':
                if line == 'display':
                    display(screen)
                else:
                    save_extension(screen, args[0]+args[1])
    else:
        print "Parsing failed."
        return
