from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox, QVBoxLayout

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QMessageBox")
        
        button_hard = QPushButton("Hard Message")
        button_hard.clicked.connect(self.button_clicked_hard)
        
        button_critical = QPushButton("Critical Message")
        button_critical.clicked.connect(self.button_clicked_critical)
        
        button_information = QPushButton("Information Message")
        button_information.clicked.connect(self.button_clicked_information)
        
        button_warning = QPushButton("Warning Message")
        button_warning.clicked.connect(self.button_clicked_warning)
        
        button_question = QPushButton("Question Message")
        button_question.clicked.connect(self.button_clicked_question)
        
        button_about = QPushButton("About Message")
        button_about.clicked.connect(self.button_clicked_about)
        
        box_layout = QVBoxLayout()
        
        box_layout.addWidget(button_hard)
        box_layout.addWidget(button_critical)
        box_layout.addWidget(button_question)
        box_layout.addWidget(button_information)
        box_layout.addWidget(button_warning)
        box_layout.addWidget(button_about)
        
        self.setLayout(box_layout)
        
    def button_clicked_hard(self):
        message = QMessageBox()
        message.setMinimumSize(700,200)
        message.setWindowTitle("Hard Message")
        message.setText("Some Text")
        message.setInformativeText("Do you want?")
        message.setIcon(QMessageBox.Critical)
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        message.setDefaultButton(QMessageBox.Ok)
        ret = message.exec()
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")
        
    def button_clicked_critical(self):
        ret = QMessageBox.critical(self,"Critical Message","Some Text",QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")
            
        
    def button_clicked_question(self):
        ret = QMessageBox.question(self,"Critical Message","Some Text",QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")
        
    def button_clicked_information(self):
        ret = QMessageBox.information(self,"Critical Message","Some Text",QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")
        
    def button_clicked_warning(self):
        ret = QMessageBox.warning(self,"Critical Message","Some Text",QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")
        
    def button_clicked_about(self):
        ret = QMessageBox.about(self,"Critical Message","Some Text")
        if ret == QMessageBox.Ok:
            print("User Chose Ok")
        else:
            print("User chose Cancel")