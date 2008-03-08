# -*- coding: utf-8 -*-

__author__    = "Jannis Leidel"
__version__   = "0.1"
__copyright__ = "Copyright (c) 2008 Jannis Leidel"
__license__   = "MIT"

import os
import sys
import math
import socket
import OSC
from profiles import Tuio2DobjProfile, Tuio2DcurProfile

class CallbackError(Exception):
    pass

class Tracking(object):
    def __init__(self, host="127.0.0.1", port=3333):
        self.host = host
        self.port = port
        self.current_frame = 0
        self.last_frame = 0

        # Defines the possible OSC profiles
        self.profiles = {
            "2Dobj": Tuio2DobjProfile(),
            "2Dcur": Tuio2DcurProfile(),
        }

        self.manager = OSC.CallbackManager()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.socket.setblocking(1)

        # Mapping callback method to every profile
        for profile in self.profiles.itervalues():
            self.manager.add(self.callback, profile.address)

    def respawn(self):
        self.socket.bind((self.host, self.port))

    def die(self):
        self.socket.close()

    def refreshed(self):
        """
        Returns True if there was a new frame
        """
        return self.current_frame >= self.last_frame
    
    def get_profile(self, profile):
        if profile in self.profiles:
            return self.profiles[profile]
        return None

    def pump(self):
        """
        Tells the connection manager to receive the next 1024 byte of messages
        to analyze.
        """
        try:
            self.manager.handle(self.socket.recv(1024))
        except socket.error:
            pass

    def callback(self, *incoming):
        message = incoming[0]
        if len(message) > 1:
            address, command = message[0][1:].split("/")[-1], message[2]
            if address in self.profiles:
                try:
                    getattr(self.profiles[address], command)(self, message)
                except AttributeError:
                    pass
    
    def _objects(self):
        self.pump()
        profile = self.get_profile('2Dobj')
        if profile is not None:
            for obj in profile.objects.itervalues():
                if obj.sessionid in profile.sessions:
                    yield obj
    
    objects = property(_objects)

    def _cursors(self):
        self.pump()
        profile = self.get_profile('2Dcur')
        if profile is not None:
            for obj in profile.objects.itervalues():
                if obj.sessionid in profile.sessions:
                    yield obj
    
    cursors = property(_cursors)

def tracking(host="127.0.0.1", port=3333):
    return Tracking(host, port)
