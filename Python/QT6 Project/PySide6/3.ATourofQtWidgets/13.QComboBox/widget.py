from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QComboBox")
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Earth", "Venus", "Mars", "Pluton", "Saturn"])
        
        button_current_value = QPushButton("Current Value")
        button_current_value.clicked.connect(self.current_value)
        
        button_set_current = QPushButton("Set Current")
        button_set_current.clicked.connect(self.set_current)
        
        button_get_values = QPushButton("Get all Values")
        button_get_values.clicked.connect(self.list_items)
        
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(button_current_value)
        layout.addWidget(button_set_current)
        layout.addWidget(button_get_values)
        
        self.setLayout(layout)
        
    def current_value(self):
        print(f"Current value: {self.combo_box.currentText()} - Current Index {self.combo_box.currentIndex()}")
        
    def set_current(self):
        self.combo_box.setCurrentIndex(2)
        
    def list_items(self):
        for i in range(self.combo_box.count()):
            print(self.combo_box.itemText(i))
        