tuio = ximport("tuio")

size(320,240)
speed(30)

def setup():
    fontsize(20)
    global t
    t = tuio.tracking()

def draw():
    for obj in t.objects:
        x = obj.xpos * WIDTH
        y = obj.ypos * HEIGHT
        rotate(obj.angle)
        rect(x, y, 20, 20)
        reset()
        text(obj.label, x, y)
