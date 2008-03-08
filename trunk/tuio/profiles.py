from objects import *

class BaseProfile(object):
    """An abstract profile as defined in the TUIO protocol"""
    def __init__(self):
        self.address = None
        self.objects = {}
        self.sessions = []

    def set(self, client, message):
        """
        The state of each alive (but unchanged) fiducial is periodically
        resent with 'set' messages.
        """
        raise NotImplementedError

    def alive(self, client, message):
        """
        The 'alive' message contains the session ids of all alive fiducials
        known to reacTIVision.
        """
        raise NotImplementedError

    def fseq(self, client, message):
        """
        fseq messages associates a unique frame id with a set of set
        and alive messages
        """
        client.last_frame = client.current_frame
        client.current_frame = message[3]

class Tuio2DcurProfile(BaseProfile):
    """A profile for a 2D cursor, e.g. a finger."""
    def __init__(self):
        super(Tuio2DcurProfile, self).__init__()
        self.address = "/tuio/2Dcur"

    def set(self, client, message):
        sessionid = message[3]
        if sessionid not in self.objects:
            self.objects[sessionid] = Tuio2DCursor(sessionid)
        self.objects[sessionid].update(sessionid, message[4:])

    def alive(self, client, message):
        if client.refreshed():
            self.sessions = message[3:]
            for obj in self.objects.keys():
                if obj not in self.sessions:
                    del self.objects[obj]

class Tuio2DobjProfile(BaseProfile):
    """A profile for a 2D tracking object, e.g. a fiducial."""
    def __init__(self):
        super(Tuio2DobjProfile, self).__init__()
        self.address = "/tuio/2Dobj"

    def set(self, client, message):
        sessionid, objectid = message[3:5]
        if objectid not in self.objects:
            self.objects[objectid] = Tuio2DObject(objectid, sessionid)
        self.objects[objectid].update(sessionid, message[5:])

    def alive(self, client, message):
        if client.refreshed():
            self.sessions = message[3:]

class Tuio25DobjProfile(BaseProfile):
    """A profile for a 2,5D tracking object, e.g. a fiducial."""
    def __init__(self):
        super(Tuio2DobjProfile, self).__init__()
        self.address = "/tuio/25Dobj"

    def set(self, client, message):
        sessionid, objectid = message[3:5]
        if objectid not in self.objects:
            self.objects[objectid] = TuioObject(objectid, sessionid)
        self.objects[objectid].update(sessionid, message[5:])

    def alive(self, client, message):
        if client.refreshed():
            self.sessions = message[3:]
