from PySide6.QtWidgets import QApplication
import sys
from widget import Widget

app = QApplication()
window = Widget()
window.show()
app.exec()