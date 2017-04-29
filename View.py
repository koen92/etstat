'''
Created on 12 Sep 2013

@author: koen
'''
from PyQt4 import QtGui, QtCore
import socket


class ServerDialog(QtGui.QDialog):

    def __init__(self, controller, parent):
        # To hide the ? button, we used QtCore.Qt.WindowSystemMenuHint
        super(ServerDialog, self).__init__(parent,
                                           QtCore.Qt.WindowSystemMenuHint |
                                           QtCore.Qt.WindowTitleHint)
        self.setParent(parent)
        self.c = controller
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                           QtGui.QDialogButtonBox.Cancel)
        self.setWindowTitle('Server toevoegen')
        vbox = QtGui.QVBoxLayout()

        lbl = QtGui.QLabel('Voer een nieuw IP-adres en poort in:')
        self.qle = QtGui.QLineEdit()

        buttonBox.accepted.connect(self.ok)
        buttonBox.rejected.connect(self.cancel)

        vbox.setSpacing(10)
        vbox.addWidget(lbl)
        vbox.addWidget(self.qle)
        vbox.addWidget(buttonBox)

        self.setLayout(vbox)

    def ok(self):
        text = self.qle.text()
        try:
            ip = str(text).split(':')[0]
            port = int(str(text).split(':')[1])
            socket.inet_aton(ip)
            self.c.addServer(ip + ':' + str(port))
            self.close()
        except (socket.error, IndexError, ValueError):
            QtGui.QMessageBox.warning(self, 'Ongeldig IP-adres',
                                      'Dit is geen geldig IP-adres, \
                                      probeer opnieuw.')

    def cancel(self):
        self.close()


class Toolbar(QtGui.QWidget):
    def __init__(self, controller, servers):
        super(Toolbar, self).__init__()
        self.c = controller
        self.servers = servers

        hbox = QtGui.QHBoxLayout()

        refresh = QtGui.QPushButton('Vernieuwen', self)
        refresh.setIcon(QtGui.QIcon.fromTheme('view-refresh'))
        refresh.clicked.connect(self.c.loadServers)

        add = QtGui.QPushButton('Nieuwe server', self)
        add.setIcon(QtGui.QIcon.fromTheme('list-add'))
        add.clicked.connect(self.addServer)

        delbtn = QtGui.QPushButton('Server verwijderen', self)
        delbtn.setIcon(QtGui.QIcon.fromTheme('list-remove'))
        delbtn.clicked.connect(self.delServer)

        hbox.addWidget(refresh)
        hbox.addWidget(add)
        hbox.addWidget(delbtn)

        self.setLayout(hbox)

    def addServer(self):
        dialog = ServerDialog(self.c, self)
        dialog.exec_()

    def delServer(self):
        if (self.servers.currentRow() > -1 and
            QtGui.QMessageBox.question(
                self, 'Vraag',
                'Weet je zeker dat je deze server wilt verwijderen? \
                        Dit kan niet ongedaan gemaakt worden.',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes):
            self.c.delServer(
                self.servers.cellWidget(self.servers.currentRow(), 1).text())


class View(QtGui.QWidget):
    ''' The main window '''

    def __init__(self):
        super(View, self).__init__()
        self.setGeometry(0, 0, 900, 500)
        self.center()
        self.setWindowTitle('ETstat')
        self.setWindowIcon(
            QtGui.QIcon('/usr/local/games/enemy-territory/ET.xpm'))

    def initUI(self, controller):
        self.c = controller

        vbox = QtGui.QVBoxLayout()

        self.servers = QtGui.QTableWidget(0, 4)
        self.servers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.servers.doubleClicked.connect(self.serverClicked)
        (
            self
            .servers
            .horizontalHeader()
            .setResizeMode(QtGui.QHeaderView.Stretch)
        )
        self.servers.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem('Naam'))
        self.servers.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem('IP'))
        self.servers.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem('Ping'))
        self.servers.setHorizontalHeaderItem(3,
                                             QtGui.QTableWidgetItem('Players'))

        self.toolbar = Toolbar(controller, self.servers)
        vbox.addWidget(self.toolbar)

        vbox.addWidget(self.servers)
        self.setLayout(vbox)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadServers(self, servers):
        self.servers.setRowCount(0)
        for i in servers:
            self.servers.setRowCount(self.servers.rowCount() + 1)
            for j in range(0, 4):
                lbl = QtGui.QLabel(i[j])
                lbl.setAlignment(QtCore.Qt.AlignCenter)
                self.servers.setCellWidget(self.servers.rowCount() - 1, j, lbl)

    def serverClicked(self):
        self.c.openServer(self.servers.cellWidget(self.servers.currentRow(),
                                                  1).text())
