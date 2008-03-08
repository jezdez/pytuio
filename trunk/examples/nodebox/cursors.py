tuio = ximport("tuio")

size(640, 480)
speed(30)

def setup():
    global tracking
    tracking = tuio.Tracking()

def draw():
    global tracking
    tracking.update()
    fontsize(10)
    for cursor in tracking.cursors:
        x = cursor.xpos * WIDTH
        y = cursor.ypos * HEIGHT
        oval(x, y, 10, 10)
        text(cursor, x, y)

def stop():
    global tracking
    tracking.stop()
