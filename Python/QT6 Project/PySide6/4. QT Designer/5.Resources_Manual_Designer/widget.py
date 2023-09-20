from PySide6.QtWidgets import QWidget
from ui_widget import Ui_Widget
from PySide6.QtGui import QIcon

import resource_rc # Able to access 

class Widget(QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        self.setWindowTitle("Spin Box")
        
        self.spin_box.setValue(50)
        
        self.minus_button.clicked.connect(self.on_minus_clicked)
        self.plus_button.clicked.connect(self.on_plus_clicked)
        
        minus = QIcon(':/images/minus-button_4436695.png')
        plus = QIcon(':/images/plus_4315609.png')
        
        self.minus_button.setIcon(minus)
        self.plus_button.setIcon(plus)
        
    def on_minus_clicked(self):
        #value = int(self.spin_box.text()) # this works with type casting
        value = self.spin_box.value()
        self.spin_box.setValue(value - 1)
        
    def on_plus_clicked(self):
        value = int(self.spin_box.text())
        self.spin_box.setValue(value + 1)
        