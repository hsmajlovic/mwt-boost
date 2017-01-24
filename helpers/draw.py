import turtle

# turtle.ht()
turtle.up()
turtle.speed(1)


def draw_polygon(dots):
    for dot in dots:
        turtle.setpos(dot.x, dot.y)
        turtle.down()
    turtle.setpos(dots[0].x, dots[0].y)
    turtle.up()


def draw_dots(dots):
    for dot in dots:
        turtle.setpos(dot.x, dot.y)
        turtle.down()
        turtle.dot()
        turtle.up()


def draw_line(dot_a, dot_b):
    turtle.up()
    turtle.setpos(dot_a.x, dot_a.y)
    turtle.down()
    turtle.setpos(dot_b.x, dot_b.y)
    turtle.up()


def draw_edges(edges):
    for edge in edges:
        edge.draw()


def erase_polygon(polygon):
    turtle.begin_fill()
    turtle.color('white')
    draw_polygon(polygon)
    turtle.end_fill()
    turtle.color('black')
