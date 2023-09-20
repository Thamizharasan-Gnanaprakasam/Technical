from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QSystemTrayIcon, QToolBar, QPushButton, QStatusBar
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.setWindowTitle("Custom MainWindow")
        
        menu_bar= self.menuBar()
        #menu_bar.setNativeMenuBar(False)
        
        file_menu = menu_bar.addMenu("&File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        
        menu_bar.addMenu("&Window")
        menu_bar.addMenu("&Setting")
        menu_bar.addMenu("&Help")
        app_menu = menu_bar.addMenu("&App")
        
        app_menu.addAction("Copy")
        app_menu.addAction("Cut")
        app_menu.addAction("Paste")
        app_menu.addAction("Undo")
        app_menu.addAction("Redo")
        
        #toolbars
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        toolbar.addAction(quit_action)
        
        action1 = QAction("Some Action", self)
        action1.setStatusTip("Status Message for some action")
        action1.triggered.connect(self.tool_bar_button_clicked)
        toolbar.addAction(action1)
        
        action2 = QAction(QIcon("start.png"),"Some Action",self)
        action2.setStatusTip("Status Message for some action")
        action2.triggered.connect(self.tool_bar_button_clicked)
        #action2.setCheckable(True)
        toolbar.addAction(action2)
        
        toolbar.addSeparator()
        toolbar.addWidget(QPushButton("Press me"))
        
        #Status Bar
        self.setStatusBar(QStatusBar())
        
        button1 = QPushButton("Button1")
        button1.clicked.connect(self.button_clicked)
        
        self.setCentralWidget(button1)
        
        
    def quit_app(self):
        self.app.quit()
        
    def tool_bar_button_clicked(self):
        self.statusBar().showMessage("Clicked",3000)
        
    def button_clicked(self):
        print("Button Clicked")
