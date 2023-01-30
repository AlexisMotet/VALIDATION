from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtTest import *
import sys

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class RuleWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        hbox = QHBoxLayout()
        self.label = QLabel(name)
        hbox.addWidget(self.label)
        self.button_delete = QPushButton("Delete")
        self.button_delete.clicked.connect(self.delete_element)
        hbox.addWidget(self.button_delete)
        self.setLayout(hbox)
        
    def delete_element(self):
        self.label.setParent(None)
        self.button.setParent(None)
        
class PopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.save_function = None
        hbox = QHBoxLayout()
        combo_box_target = QComboBox()
        combo_box_target.addItem("target")
        hbox.addWidget(combo_box_target)
        hbox.addWidget(QLabel("="))
        combo_box1 = QComboBox()
        combo_box1.addItem("var1")
        hbox.addWidget(combo_box1)
        combo_box_sign = QComboBox()
        combo_box_sign.addItem("+")
        hbox.addWidget(combo_box_sign)
        combo_box2 = QComboBox()
        combo_box2.addItem("var2")
        hbox.addWidget(combo_box2)
        button = QPushButton("Save")
        hbox.addWidget(button)
        button.clicked.connect(self.save)
        self.setLayout(hbox)
        
    def save(self):
        self.save_function(self.text_edit.toPlainText())
        
    def _show(self, save_function):
        self.save_function = save_function
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.pop_up = PopUp()
        
        hbox = QHBoxLayout()

        vbox = QVBoxLayout()
        
        hbox_ = QHBoxLayout()
        self.combo_box_guard1 = QComboBox()
        self.combo_box_guard1.addItem("comp1")
        hbox_.addWidget(self.combo_box_guard1)
        
        self.combo_box_comp = QComboBox()
        self.combo_box_comp.addItem("target")
        hbox_.addWidget(self.combo_box_comp)
        
        self.combo_box_target = QComboBox()
        self.combo_box_target.addItem("target")
        hbox_.addWidget(self.combo_box_target)
        
        self.combo_box_target = QComboBox()
        self.combo_box_target.addItem("target")
        hbox_.addWidget(self.combo_box_target)
        
        hbox_.addWidget(QLabel("="))
        
        self.combo_box1 = QComboBox()
        self.combo_box1.addItem("var1")
        hbox_.addWidget(self.combo_box1)
        
        self.combo_box_op = QComboBox()
        self.combo_box_op.addItem("+")
        hbox_.addWidget(self.combo_box_op)
        
        self.combo_box2 = QComboBox()
        self.combo_box2.addItem("var2")
        hbox_.addWidget(self.combo_box2)
        
        button_add = QPushButton("Add")
        button_add.clicked.connect(self.create_rule)
        hbox_.addWidget(button_add)

        vbox.addLayout(hbox_)
        self.list_rules = QVBoxLayout()
        vbox.addLayout(self.list_rules)
        
        hbox.addLayout(vbox)
        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        self.show()
        
    def create_rule(self):
        pass     
        
        
        
    def delete_element(self, hbox, label, button):
        # self.list.removeItem(hbox)
        label.setParent(None)
        button.setParent(None)
        
    def save_function(self, text):
        rule_widget = RuleWidget("test")
        self.list.addWidget(rule_widget)
        self.pop_up.close()
        self.pop_up.text_edit.document().setPlainText("")

    def add_item(self):
        self.pop_up._show(self.save_function)
        

if __name__ == "__main__" :
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    app.exec()
