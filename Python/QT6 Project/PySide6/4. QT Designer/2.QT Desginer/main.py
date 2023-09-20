from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader
import sys



loader = QUiLoader()

app = QApplication(sys.argv)

window = loader.load("widget.ui", None) # load ui - happens at run time

def on_button_click():
    print(f"{window.full_name_line_edit.text()} is a {window.occupation_line_edit.text()}")

window.setWindowTitle("User Data")

window.submit_button.clicked.connect(on_button_click)

window.show()

app.exec()