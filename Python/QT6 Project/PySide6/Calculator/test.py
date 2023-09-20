from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout
import sys

buttons = []
app = QApplication(sys.argv)
window = QWidget()

v_layout = QVBoxLayout()

for i in range(10):
    button = QPushButton(str(i))
    buttons.append(button)
    v_layout.addWidget(buttons[i])
    
window.setLayout(v_layout)
    

window.show()
app.exec()