'''
Created on 12 Sep 2013

@author: koen
'''

import os
import socket
import subprocess
from BeautifulSoup import BeautifulSoup

class Model():
    def __init__(self):
        pass
    
    def readIPs(self):
        try:
            f = open(os.path.expanduser('~/.ETstat'), 'r')
        except IOError:
            f = open(os.path.expanduser('~/.ETstat'), 'w')
            f.close();
            f = open(os.path.expanduser('~/.ETstat'), 'r')
        ips = [];
        for i in f:
            try:
                ip = str(i).split(':')[0]
                port = int(str(i).split(':')[1])
                socket.inet_aton(ip)
                ips.append(i)
            except (socket.error, IndexError, ValueError):
                pass
        f.close()
        return ips
    
    def parseServer(self, serverData):
        serverData = serverData.replace("<name>", "<servername>")
        serverData = serverData.replace("</name>", "</servername>")
        parsedServer = [];
        xml = BeautifulSoup(serverData)
        if xml.qstat.server['status'] == "DOWN":
            parsedServer.append("Server is down")
            parsedServer.append(xml.qstat.server.hostname.string.split('&')[0])
            parsedServer.append("999")
            parsedServer.append("0/0")
        else:
            parsedServer.append(xml.qstat.server.servername.string)
            parsedServer.append(xml.qstat.server.hostname.string.split('&')[0])
            parsedServer.append(xml.qstat.server.ping.string)
            parsedServer.append(xml.qstat.server.numplayers.string + "/" + xml.qstat.server.maxplayers.string)

        return parsedServer; 
    
    def getServers(self):
        servers = [];
        ips = self.readIPs()
        for i in ips:
            proc = subprocess.Popen(['quakestat', '-xml', '-woets', i], stdout=subprocess.PIPE)
            servers.append(self.parseServer(proc.stdout.read()));
        return servers

    def addServer(self, IP):
        f = open(os.path.expanduser('~/.ETstat'), 'a')
        f.write(IP + '\n');
        f.close();
    
    def delServer(self, IP):
        f = open(os.path.expanduser('~/.ETstat'), 'r')
        lines = f.readlines()   
        f.close()
        f = open(os.path.expanduser('~/.ETstat'), 'w')
        for i in lines:
            if i != IP + "\n":
                f.write(i)
        f.close()