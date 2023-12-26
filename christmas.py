import random
import turtle

window = turtle.Screen()
window.bgcolor("sky blue")
tree = turtle.Turtle()
tree.color("forest green")
snow_y = -320


def make_tree_segment(size, top_position):
    tree.begin_fill()
    tree.setposition(0, top_position)
    tree.setposition(size, top_position - size)
    tree.setposition(-size, top_position - size)
    tree.setposition(0, top_position)
    tree.end_fill()


def draw_tree(segments):
    for size, top_position in segments:
        make_tree_segment(size, top_position)


def draw_wood():
    wood = turtle.Turtle()
    wood.penup()
    wood.setposition(-10, -260)
    wood.pendown()
    wood.color("brown")
    wood.fillcolor("brown")
    wood.begin_fill()
    wood.fd(30)
    wood.left(90)
    wood.fd(50)
    wood.lt(90)
    wood.fd(30)
    wood.lt(90)
    wood.fd(50)
    wood.end_fill()
    wood.penup()
    wood.hideturtle()


def christmas():
    turtle.penup()
    turtle.setposition(-180, 100)
    turtle.pendown()
    turtle.color("red")
    turtle.write("Merry Christmas", move=False, align="left", font=("Arial", 50, "bold"))
    turtle.penup()
    turtle.hideturtle()


def draw_haus():
    haus = turtle.Turtle()
    haus.penup()
    haus.setposition(150, -160)
    haus.pendown()
    haus.fd(100)  # das
    haus.lt(145)
    haus.fd(124)  # ist
    haus.rt(145)
    haus.fd(100)  # das
    haus.lt(133)
    haus.fd(80)  # Haus
    haus.lt(98)
    haus.fd(75)  # vom
    haus.lt(40)
    haus.fd(70)  # Ni-
    haus.lt(123)
    haus.fd(122)  # -ko-
    haus.rt(123)
    haus.fd(70)  # -laus
    haus.lt(90)
    haus.fd(50)  # mit
    haus.lt(142)
    haus.fd(63)  # ei-
    haus.rt(143)
    haus.fd(50)  # nem
    haus.lt(132)
    haus.fd(44)  # Scheiß-
    haus.lt(104)
    haus.fd(38)  # haus
    haus.lt(35)
    haus.fd(40)  # hin-
    haus.lt(127)
    haus.fd(63)  # -ten
    haus.rt(127)
    haus.fd(38)  # draus
    haus.hideturtle()


def draw_schneeflocke(x):
    schneeflocke = turtle.Turtle()
    schneeflocke.pen(pencolor="white", speed=200)
    schneeflocke.penup()
    schneeflocke.setposition(x)
    schneeflocke.pendown()
    for i in range(8):
        schneeflocke.left(45)
        for a in range(3):
            for b in range(3):
                schneeflocke.fd(10)
                schneeflocke.bk(10)
                schneeflocke.rt(45)
            schneeflocke.lt(90)
            schneeflocke.bk(10)
            schneeflocke.lt(45)
        schneeflocke.rt(90)
        schneeflocke.fd(30)
    schneeflocke.hideturtle()


def draw_snow():
    global snow_y
    snow = turtle.Turtle()
    snow.pen(pencolor="white", pensize=8)
    snow.penup()
    snow.setposition(-400, snow_y)
    snow.pendown()
    snow.fd(800)
    snow.hideturtle()


def draw_schneeflocken():
    global snow_y
    for i in range(10):
        x = random.randrange(-200, 200)
        y = random.randrange(-200, 200)
        draw_schneeflocke((x, y))
        draw_snow()
        snow_y += 8


def deko_tree():
    deko = turtle.Turtle()
    x = 0
    y = -15
    colors = ['blue', 'yellow', 'purple', 'red', 'cyan']
    for d in range(5):
        deko.penup()
        deko.setposition(x, y)
        deko.pendown()
        deko.color(colors[d])
        deko.fillcolor(colors[d])
        deko.begin_fill()
        deko.circle(10)
        deko.end_fill()
        deko.penup()
        x += 10
        y -= 40
        colors += [1]  # Modify the copy of the list
    x = 90
    y = -200

    for e in range(5):
        deko.setposition(x, y)
        deko.pendown()
        deko.color(colors[e])
        deko.fillcolor(colors[e])
        deko.begin_fill()
        deko.circle(10)
        deko.end_fill()
        deko.penup()
        x -= 50
        y -= 0
        colors += [1]  # Modify the copy of the list
    deko.hideturtle()


tree_segments = ((50, 20), (80, 0), (120, -30), (150, -60))
schnee = (random.randrange(50, 200)), (random.randrange(50, 200))
draw_tree(tree_segments)
draw_wood()
deko_tree()
draw_haus()
christmas()
draw_schneeflocken()
turtle.done()
