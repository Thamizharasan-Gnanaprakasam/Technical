from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        
        self.setupUi(self)
        
        self.setWindowTitle("Text Editor")
        self.actionQuit.triggered.connect(self.on_quit)
        
        self.actionCopy.triggered.connect(self.text_edit.copy)
        self.actionPaste.triggered.connect(self.text_edit.paste)
        self.actionCut.triggered.connect(self.text_edit.cut)
        self.actionRedo.triggered.connect(self.text_edit.redo)
        self.actionUndo.triggered.connect(self.text_edit.undo)
        self.actionAbout.triggered.connect(self.about)
        self.actionAbout_QT.triggered.connect(QApplication.aboutQt)
        
    def on_quit(self):
        self.app.exit()
        
    def about(self):
        QMessageBox().information(self,"Going Pro!","QMainWindow, Qt Designer and Resource", QMessageBox.Ok, QMessageBox.Cancel)