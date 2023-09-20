from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QLabel and QLineEdit")
        
        label = QLabel("Full Name:")
        self.line_edit = QLineEdit()
        self.line_edit.textEdited.connect(self.text_edited)
        #self.line_edit.textChanged.connect(self.text_changed) # Takes presidence over textEdited Signal
        self.line_edit.cursorPositionChanged.connect(self.cursor_position_changed)
        self.line_edit.returnPressed.connect(self.return_pressed)
        self.line_edit.editingFinished.connect(self.editing_finished) # Takes presidence over returnPressed Signal
        self.line_edit.selectionChanged.connect(self.selection_changed)
        
        button = QPushButton("Grab Data")
        self.text_holder_label = QLabel("I am Here")
        button.clicked.connect(self.button_clicked)
        
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        h_layout.addWidget(label)
        h_layout.addWidget(self.line_edit)
        
        v_layout.addLayout(h_layout)
        v_layout.addWidget(button)
        v_layout.addWidget(self.text_holder_label)
        
        
        self.setLayout(v_layout)
        
    #SLOTS
    def button_clicked(self):
        #print(f"Full Name: {self.line_edit.text()}")
        self.text_holder_label.setText(self.line_edit.text())
        
    def text_changed(self):
        #print(f"Full Name: {self.line_edit.text()}")
        self.text_holder_label.setText(f"Texted Changed: {self.line_edit.text()}")
        
    def cursor_position_changed(self, old, new): # takes 2 Argumenrs
        print(f"Old Position: {old} and New Position: {new}")
        
    def text_edited(self, new_text): #Takes one argument
        #print(f"Full Name: {self.line_edit.text()}")
        self.text_holder_label.setText(f"Texted Edited: {new_text}")
        
    def editing_finished(self):
        #print(f"Full Name: {self.line_edit.text()}")
        self.text_holder_label.setText(f"Editing Finished: {self.line_edit.text()}")
        
    def return_pressed(self):
        #print(f"Full Name: {self.line_edit.text()}")
        self.text_holder_label.setText(f"Return Pressed: {self.line_edit.text()}")
        
    def selection_changed(self):
        print(f"Selected Text: {self.line_edit.selectedText()}")