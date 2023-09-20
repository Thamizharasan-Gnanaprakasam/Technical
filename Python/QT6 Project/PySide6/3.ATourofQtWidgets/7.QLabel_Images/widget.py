from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QLabel Image Demo")
        
        image_label = QLabel()
        image_label.setPixmap(QPixmap("images/minions.png"))
        
        v_layout = QVBoxLayout()
        v_layout.addWidget(image_label)
        
        self.setLayout(v_layout)