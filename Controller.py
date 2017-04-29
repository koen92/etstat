'''
Created on 12 Sep 2013

@author: koen
'''
import subprocess


class Controller():
    def __init__(self, w, m):
        self.w = w
        self.m = m

    def loadServers(self):
        self.w.loadServers(self.m.getServers())

    def addServer(self, IP):
        self.m.addServer(IP)
        self.loadServers()

    def openServer(self, IP):
        subprocess.Popen(
            ['/usr/local/games/enemy-territory/et', '+connect', IP])

    def delServer(self, IP):
        self.m.delServer(IP)
        self.loadServers()
