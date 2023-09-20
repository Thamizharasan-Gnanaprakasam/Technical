from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Size Policies and Stretches")
        
        label = QLabel("Some Text: ")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        line_edit = QLineEdit()
        line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(label)
        h_layout_1.addWidget(line_edit)
        
        
        
        button_1 = QPushButton("Button 1")
        button_2 = QPushButton("Button 2")
        button_3 = QPushButton("Button 3")
        
        #Streches tells us how many spaces should a Widget should occupy. This can be done when adding the widget to layout
        
        h_layout_2 = QHBoxLayout()
        h_layout_2.addWidget(button_1,3)
        h_layout_2.addWidget(button_2,1)
        h_layout_2.addWidget(button_3,1)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        
        self.setLayout(v_layout)