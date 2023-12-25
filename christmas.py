import turtle

window = turtle.Screen()
window.bgcolor("sky blue")
tree = turtle.Turtle()
tree.color("forest green")




def make_tree_segment(size, top_position):
    tree.begin_fill()
    tree.setposition(0, top_position)
    tree.setposition(size, top_position - size)
    tree.setposition(-size, top_position - size)
    tree.setposition(0, top_position)
    tree.end_fill()


def wood():
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


def christmas():
    turtle.penup()
    turtle.setposition(-180, 100)
    turtle.pendown()
    turtle.color("red")
    turtle.write("Merry Christmas", move=False, align="left", font=("Arial", 50, "bold"))
    turtle.penup()

def haus():
    haus = turtle.Turtle()
    haus.penup()
    haus.setposition(150, -160)
    haus.pendown()
    haus.fd(100)    # das
    haus.lt(145)
    haus.fd(124)    # ist
    haus.rt(145)
    haus.fd(100)    # das
    haus.lt(133)
    haus.fd(80)     # Haus
    haus.lt(98)
    haus.fd(75)     # vom
    haus.lt(40)
    haus.fd(70)     # Ni-
    haus.lt(123)
    haus.fd(122)     # -ko-
    haus.rt(123)
    haus.fd(70)     # -laus
    haus.lt(90)
    haus.fd(50)     # mit
    haus.lt(142)
    haus.fd(63)     # ei-
    haus.rt(143)
    haus.fd(50)     # nem
    haus.lt(132)
    haus.fd(44)     # Scheiß-
    haus.lt(104)
    haus.fd(38)     # haus
    haus.lt(35)
    haus.fd(40)     # hin-
    haus.lt(127)
    haus.fd(63)     # -ten
    haus.rt(127)
    haus.fd(44)     # draus

tree_segments = ((50, 20), (80, 0), (120, -30), (150, -60))
for size, top_position in tree_segments:
    make_tree_segment(size, top_position)
wood()
haus()
christmas()



turtle.done()
