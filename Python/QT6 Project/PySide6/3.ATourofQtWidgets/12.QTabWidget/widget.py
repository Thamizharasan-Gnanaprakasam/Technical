from PySide6.QtWidgets import QWidget, QTabWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QTabWidget")
        
        tab_widget = QTabWidget()
        
        form_layout = QHBoxLayout()
        
        label = QLabel("Full Name:")
        line_edit = QLineEdit()
        
        form_layout.addWidget(label)
        form_layout.addWidget(line_edit)
        
        widget_form = QWidget()
        widget_form.setLayout(form_layout)
        
        button_1 = QPushButton("One")
        button_1.clicked.connect(self.button_1_clicked)
        button_2 = QPushButton("Two")
        button_3 = QPushButton("Three")
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(button_1)
        button_layout.addWidget(button_2)
        button_layout.addWidget(button_3)
        
        widget_button = QWidget()
        widget_button.setLayout(button_layout)
        
        tab_widget.addTab(widget_form, "Information")
        tab_widget.addTab(widget_button, "Buttons")
        #tab_widget.setLayout(button_layout)
        
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        
        self.setLayout(layout)
        
    def button_1_clicked(self):
        print("Button 1 Clicked")