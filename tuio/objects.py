# -*- coding: utf-8 -*-
import math

class UpdateError(Exception):
    pass

class BaseObject(object):
    def __init__(self, *args):
        pass
        
    def __repr__(self):
        return "<%s %s> " % (self.__class__.__name__, self.label)

    def update(self):
        """
        The method which gets executed when a new state of the object was
        received.
        """
        raise NotImplementedError

    def _label(self):
        """
        The text that should be shown in the object reprentation.
        """
        raise NotImplementedError

    label = property(_label)

class Tuio2DCursor(BaseObject):
    """
    An abstract object representing a cursor, e.g. a finger.
    """
    def __init__(self, sessionid):
        super(Tuio2DCursor, self).__init__(sessionid)
        self.sessionid = sessionid
        self.xpos = self.ypos = self.xmot = self.ymot = self.amot = 0.0
    
    def update(self, sessionid, args):
        if len(args) == 5:
            self.sessionid = sessionid
            self.xpos, self.ypos, self.xmot, self.ymot, self.amot = args[0:5]
        else:
            raise UpdateError

    def _label(self):
        return str(self.id)

    label = property(_label)

class Tuio2DObject(BaseObject):
    """
    An abstract object representing a fiducial.
    """
    def __init__(self, objectid, sessionid):
        super(Tuio2DObject, self).__init__(objectid, sessionid)
        self.id = objectid
        self.sessionid = sessionid
        self.xpos = self.ypos = self.angle = self.mot_speed = 0.0
        self.mot_accel = self.rot_speed = self.rot_accel = 0.0
        self.speed = 0

    def update(self, sessionid, args):
        if len(args) == 8:
            #xpos, ypos, angle, xmot, ymot, rot_vector, mot_accel, rot_accel = args
            self.sessionid = sessionid
            self.xpos, self.ypos = args[0:2]
            self.angle = (180//math.pi)*args[2]
            xmot, ymot = args[3:5]
            self.mot_speed = math.sqrt(xmot*xmot+ymot*ymot)
        else:
            raise UpdateError
    
    def _label(self):
        return u"%s, %s°" % (str(self.id), str(int(self.angle)))

    label = property(_label)
