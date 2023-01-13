import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QToolBar, QStatusBar


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        ###self.showMaximized()

        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.setWindowTitle("Graph Application")

        toolbar = QToolBar("toolbar")
        self.addToolBar(toolbar)
        
        button_add = QAction("Add Button", self)
        button_add.setStatusTip("Add Button")
        button_add.triggered.connect(self.onMyToolBarAddButtonClick)
        toolbar.addAction(button_add)

        button_delete = QAction("Delete Button", self)
        button_delete.setStatusTip("Delete Button")
        button_delete.triggered.connect(self.onMyToolBarDeleteButtonClick)
        toolbar.addAction(button_delete)

        self.setStatusBar(QStatusBar(self))

    def onMyToolBarAddButtonClick(self, s):
        print("Add Button", s)

    def onMyToolBarDeleteButtonClick(self, s):
        print("Add Button", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()