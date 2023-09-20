from typing import Optional
import PySide6.QtCore
from ui_widget import Ui_Widget
from PySide6.QtWidgets import QWidget

class Widget(QWidget, Ui_Widget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setupUi(self)
        self.setWindowTitle("User Data")
        
        self.submit_button.clicked.connect(self.on_button_click)
        
    def on_button_click(self):
        print(f"{self.full_name_line_edit.text()} is a {self.occupation_line_edit.text()}")