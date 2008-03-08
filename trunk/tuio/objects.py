# -*- coding: utf-8 -*-
import math

class UpdateError(Exception):
    pass

class Tuio2DCursor(object):
    """
    An abstract object representing a cursor, e.g. a finger.
    """
    def __init__(self, sessionid):
        self.sessionid = sessionid
        self.xpos = self.ypos = self.xmot = self.ymot = self.amot = 0.0
    
    def update(self, sessionid, args):
        if len(args) == 5:
            self.sessionid = sessionid
            self.xpos = args[0]
            self.ypos = args[1]
            self.xmot = args[2]
            self.ymot = args[3]
            self.amot = args[4]
        else:
            raise UpdateError

    def _label(self):
        return str(self.id)

    label = property(_label)

class Tuio2DObject(object):
    """
    An abstract object representing a fiducial.
    """
    def __init__(self, objectid, sessionid):
        self.id = objectid
        self.sessionid = sessionid
        self.xpos = self.ypos = self.angle = self.mot_speed = self.mot_accel = \
            self.rot_speed = self.rot_accel = 0.0
        self.speed = 0

    def update(self, sessionid, args):
        if len(args) == 8:
            #xpos, ypos, angle, xmot, ymot, rot_vector, mot_accel, rot_accel = args
            self.sessionid = sessionid
            self.xpos = args[0]
            self.ypos = args[1]
            self.angle = (180//math.pi)*args[2]
            # self.mot_speed, self.mot_accel = mot_speed, mot_accel
            # self.rot_speed, self.rot_accel = rot_speed, rot_accel
            xmot, ymot = args[3:5]
            self.mot_speed = math.sqrt(xmot*xmot+ymot*ymot)
        else:
            raise UpdateError
    
    def _label(self):
        return u"%s, %s°" % (str(self.id), str(int(self.angle)))

    label = property(_label)
