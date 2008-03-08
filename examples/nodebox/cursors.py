tuio = ximport("tuio")

size(320,240)
speed(30)

def setup():
    fontsize(20)
    global t
    t = tuio.tracking()

def draw():
    for cursor in t.cursors:
        x = cursor.xpos * WIDTH
        y = cursor.ypos * HEIGHT
        oval(x, y, 10, 10)
        text(cursor.label, x, y)
