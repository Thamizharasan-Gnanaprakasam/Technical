from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore

loader = QUiLoader()

class UserInterface(QtCore.QObject):
    def __init__(self):
        super().__init__()
        
        self.ui = loader.load("widget.ui")
        self.ui.setWindowTitle("Qt App V2")
        
        self.ui.submit_button.clicked.connect(self.on_button_click)
        
    def on_button_click(self):
        print(f"{self.ui.full_name_line_edit.text()} is a {self.ui.occupation_line_edit.text()}")
        
    def show(self):
        self.ui.show()