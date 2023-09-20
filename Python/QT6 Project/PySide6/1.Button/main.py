#from typing import Optional
#import PySide6.QtCore
from button_holder import ButtonHolder
from PySide6.QtWidgets import QApplication
import sys


#Version 1 - No Class
"""
#from typing import Optional
#import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("My First PySide Project")

button = QPushButton()
button.setText("Press Me")

window.setCentralWidget(button)


window.show()
app.exec()
"""

#Version 2 - with Class
"""
#from typing import Optional
#import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class ButtonHolder(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("My First PySide Project")
        
        button = QPushButton()
        button.setText("Press Me")
        
        self.setCentralWidget(button)
        
app = QApplication(sys.argv)
window = ButtonHolder()
window.show()
app.exec()
"""

#Version 3 - Seperate Python file for Button Holder

app = QApplication(sys.argv)
window = ButtonHolder()
window.show()
app.exec()