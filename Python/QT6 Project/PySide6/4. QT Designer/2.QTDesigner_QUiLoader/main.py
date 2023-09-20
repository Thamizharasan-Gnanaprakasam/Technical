from PySide6.QtWidgets import QApplication
from user_interface import UserInterface
import sys



app = QApplication(sys.argv)

window = UserInterface()

window.show()

app.exec()