from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class RockWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        button1 = QPushButton()
        button1.setText("Button 1")
        button2 = QPushButton()
        button2.setText("Button 2")
        
        button1.clicked.connect(self.button1_clicked(button1.text()))
        button2.clicked.connect(self.button2_clicked)
        
        box_layout = QVBoxLayout()
        box_layout.addWidget(button1)
        box_layout.addWidget(button2)
        
        self.setLayout(box_layout)
        
    def button1_clicked(self,data):
        print(f"Button1 Clicked{data}")
        
    def button2_clicked(data):
        print(f"Button2 Clicked")