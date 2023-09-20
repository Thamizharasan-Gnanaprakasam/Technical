from PySide6.QtWidgets import QMainWindow, QPushButton

class ButtonHolder(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("My First PySide Project")
        
        button = QPushButton()
        button.setText("Press Me")
        #button.setCheckable(True)
        
        self.setCentralWidget(button)