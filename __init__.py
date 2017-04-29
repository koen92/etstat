#!/usr/bin/python

'''
Created on 12 Sep 2013

@author: koen
'''

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
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
