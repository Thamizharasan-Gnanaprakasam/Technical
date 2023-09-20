from widget import Widget
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = Widget()
window.show()
app.exec()