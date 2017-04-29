#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from View import View
from Controller import Controller
from Model import Model
from PyQt4 import QtGui


def main():
    
    app = QtGui.QApplication(sys.argv)

    w = View()
    m = Model();
    c = Controller(w, m);
    w.initUI(c);
    w.show()
    c.loadServers();
    #c.loadServers();
            
    #server = [ "kernwaffe", "127.0.0.1", "20", "9/10" ]
    #w.addServer(server);
    
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
