#Version 1: Action on PushButton
"""
from PySide6.QtWidgets import QPushButton, QApplication
import sys

def on_button_press():
    print("Button Pressed")

app = QApplication(sys.argv)

button = QPushButton()
button.setText("Press Me")
button.clicked.connect(on_button_press)

button.show()
app.exec()
"""

#Version 2: Making PushButton as Chekcable and return the state
"""
from PySide6.QtWidgets import QApplication, QPushButton
import sys

def on_button_press(data):
    print(f"Button is Clicked and Current State is {data}")
    
app = QApplication(sys.argv)

button = QPushButton()
button.setText("Press Me")
button.setCheckable(True)
button.clicked.connect(on_button_press)

button.show()
app.exec()
"""

#Version 3: QSlider
from PySide6.QtWidgets import QSlider, QApplication
from PySide6 import QtCore
import sys

def on_slider_changed(data):
    print(f"Current slider Value: {data}")

app = QApplication(sys.argv)
slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(50)
slider.valueChanged.connect(on_slider_changed)


slider.show()
app.exec()