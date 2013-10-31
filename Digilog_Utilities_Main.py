'''
Created on Oct 21, 2013

@author: elliottlocke
'''
import Speed_validator
import easygui as eg
import sys
import os
from PyQt4 import QtGui, QtCore




def main():

    choices = eg.choicebox(msg='Pick something.', title=' ', choices=("Speed_Validator","Joe's face app" , "poop app"))
    
    if str(choices) == "Speed_Validator":
        app = QtGui.QApplication(sys.argv)
        form = MainForm()
        form.show()
        app.exec_()
        Speed_validator.speedValidator()

class TestListView(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        
        self.setAcceptDrops(True)
#         self.setIconSize(QtCore.QSize(72, 72))
        self.initUI()

    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')     
        
        okButton = QtGui.QPushButton("OK", self)
        cancelButton = QtGui.QPushButton("Cancel", self)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        okButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        cancelButton.clicked.connect(TestListView.close)

        self.setLayout(vbox)    
        
        self.setGeometry(444, 444, 444, 444)
        self.setWindowTitle('Route Drag and Drop Window')    
        self.show()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setGeometry(0, 0, 500, 300)
        self.view = TestListView(self)
        self.connect(self.view, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Drag and drop your routes on this window")

    def pictureDropped(self, l):
        urlList = []
        for url in l:
            if os.path.exists(url):             
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)                
                icon = QtGui.QIcon(pixmap)
                item = QtGui.QListWidgetItem(url, self.view)
                item.setIcon(icon)        
                item.setStatusTip(url)  
                urlList.append(url)     
        filepath = "/usr/local/Library/Digilog_Utilites.txt"
        textfile = open(filepath, 'w')
        #with os.fdopen(os.open(filepath, os.O_WRONLY | os.O_CREAT, 0600), 'w') as textfile:
        for thisfile in urlList:
            textfile.write(thisfile)
            textfile.write('\n')

if __name__ == '__main__':
    main()
    sys.exit()