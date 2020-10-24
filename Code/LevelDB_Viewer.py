# Author Mark McKinnon
# Email: Mark.McKinnon@gmail.compile
# License: Apache 2.0

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import ntpath
import leveldb

qtCreatorFile = "LevelDB_Viewer.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Setup File Menu
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(self.setupMenu())
        # self.setupTableContextMenu()

    def setupMenu(self):

        fileOpenAction = QtWidgets.QAction('Open Database', self)
        fileOpenAction.setShortcut("CTRL+O")
        fileOpenAction.setStatusTip("Open Database")
        fileOpenAction.triggered.connect(self.openImage)

        return fileOpenAction

        
    def openImage(self):
        #fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open LevelDb File',
        #                                             'D:\\LevelDB', "All Files (*.*)")
        fileDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', 'D:\\LevelDB')
        if len(fileDirectory) > 0:
            self.clearLevelDbTableWidget()
            #levelDb = leveldb.LevelDB(str(fileDirectory))
            self.addLevelDb(str(fileDirectory))
            print ("Directory selected is " + fileDirectory)
        else:
            print ("No Directory Selected!!!!")

    def addLevelDb(self, levelDbDir):
    
        try:
            levelDb = leveldb.LevelDB(levelDbDir)
            try:
                print (levelDb.GetStats())
            except:
                print ("No Stats")

            columnHeadings = ["Key", "Value"]
            self.levelDbTableWidget.setColumnCount(2)
            self.levelDbTableWidget.setHorizontalHeaderLabels(columnHeadings)
            tabHeader = self.levelDbTableWidget.horizontalHeader()
            #tabHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
            #tabHeader.setResizeMode(0, QtGui.QHeaderView.Stretch)
            #tabHeader.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            rowNum = 0
            for key, value in levelDb.RangeIter():
                self.levelDbTableWidget.insertRow(rowNum)
                self.levelDbTableWidget.setItem(rowNum, 0, self.createItem(str(key)))
                self.levelDbTableWidget.setItem(rowNum, 1, self.createItem(str(value)))
                rowNum = rowNum + 1

            print ("Number of records dumped are ==> " + str(rowNum))
        except:
            print ("Attempting to repair DB")
            levelDb = leveldb.RepairDB(levelDbDir)
            levelDb2 = leveldb.LevelDB(os.path.join(levelDbDir, "lost"))
            try:
                print (levelDb2.GetStats())
            except:
                print ("No Stats")
            columnHeadings = ["Key", "Value"]
            self.levelDbTableWidget.setColumnCount(2)
            self.levelDbTableWidget.setHorizontalHeaderLabels(columnHeadings)
            tabHeader = self.levelDbTableWidget.horizontalHeader()
            #tabHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
            #tabHeader.setResizeMode(0, QtGui.QHeaderView.Stretch)
            #tabHeader.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            rowNum = 0
            for key, value in levelDb2.RangeIter():
                self.levelDbTableWidget.insertRow(rowNum)
                self.levelDbTableWidget.setItem(rowNum, 0, self.createItem(str(key.decode('utf-8', "ignore"))))
                self.levelDbTableWidget.setItem(rowNum, 1, self.createItem(str(value.decode('utf-8', "ignore"))))
                rowNum = rowNum + 1

    def createItem(self, itemString):

        item = QtWidgets.QTableWidgetItem(str(itemString))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    def clearLevelDbTableWidget(self):

        self.levelDbTableWidget.clearContents()
        self.levelDbTableWidget.setRowCount(0)
        self.levelDbTableWidget.setColumnCount(0)

            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())