from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QIcon

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Custom MainWindow")
        button = QPushButton("Clicked")
        button.pressed.connect(self.on_button_pressed)
        button.clicked.connect(self.on_button_clicked)
        button.released.connect(self.on_button_released)
        button.toggled.connect(self.on_button_toggled)
        button.setCheckable(True)
        button.setIcon(QIcon("bg1.jpg"))
        
        box = QVBoxLayout()
        box.addWidget(button)
        
        self.setLayout(box)
        
    def on_button_pressed(self):
        print("Button Pressed")
    
    def on_button_clicked(self):
        print("Button Clicked")
    
    def on_button_released(self):
        print("Button Released")
        
    def on_button_toggled(self,data):
        print(f"Button Toggled {data}")