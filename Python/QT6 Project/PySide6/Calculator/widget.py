from typing import Optional
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout, QSizePolicy, QHBoxLayout, QVBoxLayout, QFontDialog, QMenuBar, QMenu
from PySide6.QtGui import QPixmap, QDoubleValidator, QFont, QFontDatabase, QAction
from functools import partial

class Widget(QWidget):
    keypad = [{"C": "icons/C.png",
                "+/-": "icons/plus_minus.png",
                "%": "icons/percent.png",
                "/": "icons/divide.png"},
              {"7": "icons/7.png",
                "8": "icons/8.png",
                "9": "icons/9.png",
                "*": "icons/multiply.png"},
              {"4": "icons/4.png",
                "5": "icons/5.png",
                "6": "icons/6.png",
                "-": "icons/subtract.png"},
              {"1": "icons/1.png",
                "2": "icons/2.png",
                "3": "icons/3.png",
                "+": "icons/add.png"},
              {"0": "icons/0.png",
                ".": "icons/point.png",
                "=": "icons/equal.png"}]
    
    #font = None
    first_num = ""
    sec_num = ""
    oper = ""
    calc_bool = False
    
    #buttons = []
    def __init__(self):
        super().__init__()
        
        id = QFontDatabase.addApplicationFont("fonts/Lcd.ttf")
        #print(id)
        
        self.ok = bool()
        
        #font = QFontDialog.getFont()
        #print(font[1])
        
        
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QPixmap("icons/calculator.png"))
        self.setMaximumHeight(600)
        self.setMaximumWidth(400)
        self.setMinimumHeight(600)
        self.setMinimumWidth(400)
        
        self.menu_bar = QMenuBar()
        self.font_menu = QMenu("Fonts")
        self.sel_font = QAction(self)
        self.sel_font.setText("Select Font")
        self.sel_font.triggered.connect(self.select_font)
        self.menu_bar.addMenu(self.font_menu)
        self.font_menu.addAction(self.sel_font)
        
        self.line_edit = QLineEdit("0")
        self.line_edit.setValidator(QDoubleValidator())
        self.line_edit.setFont(QFont("Annai MN", 32))
        #self.line_edit.pos(QtCore.QPoint(0, 0))
        self.line_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        #self.line_edit.setFixedSize(100,100)
        
        #v_layout = QVBoxLayout()
        #v_layout.addWidget(self.menu_bar)
        #v_layout.addWidget(self.line_edit)
        #v_layout.addWidget(font)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.menu_bar)
        self.grid_layout.addWidget(self.line_edit,0,0,1,4)
        
        i = 1
        k = 0
        for my_dict in self.keypad:
            j = 0
            for key, val in my_dict.items():
                button = QPushButton()
                #self.buttons.append(button)
                #self.buttons[k].setText(str(key))
                button.setText(str(key))
                button.setMinimumHeight(50)
                
                #button.setStyleSheet("border: 20px;  padding: 20px; text-align: center;  margin: 4px 2px; border-radius: 50%; ")
                
                if key not in ["0", ".","="]:
                    self.grid_layout.addWidget(button, i, j)
                elif key == "0":
                    
                    self.grid_layout.addWidget(button, i, j, 1, 2)
                else:
                    self.grid_layout.addWidget(button, i, j+1)
                #button.setIcon(QPixmap(val))
                #button.setIconSize(QtCore.QSize(10,10))
                if key in ["/", "*", "-","+", "="]:
                    button.setStyleSheet("background-color: #FFA500; border-radius: 45px; border: 1px; padding: 10px 20px;")
                                        
                elif key in ["C", "+/-", "%"]:
                    button.setStyleSheet("background-color: #D3D3D3; color: black; border-radius: 45px; border: 1px; padding: 10px 20px;")
                                         #"border-radius: 5px;" +
                                     #"border: 1px;" +
                #                    "padding: 10px 20px;")
                if key in ["0","1","2","3","4","5","6","7","8","9"]:    
                    button.clicked.connect(partial(self.on_num_click,key))
                elif key == ".":
                    button.clicked.connect(partial(self.on_point_click,'.'))
                    #self.buttons[k].clicked.connect(partial(self.on_point_click,self.buttons[k].text()))
                elif key == "C":
                    button.clicked.connect(self.on_clear_click)
                elif key == "+/-":
                    button.clicked.connect(self.on_switch_sign)
                elif key == "%":
                    button.clicked.connect(self.on_percent_button)
                elif key in ["+","-","*","/"]:
                    button.clicked.connect(partial(self.on_oper_button,key))
                elif key == "=":
                    button.clicked.connect(self.on_equal_button)
                
                j += 1
                k += 1
            i += 1
        #v_layout.addLayout(self.grid_layout)
                
        
        self.setLayout(self.grid_layout)
        
    def on_num_click(self, txt):
        if self.line_edit.text() in ["0", "-0"] or not self.calc_bool:
            self.line_edit.setText("")
        self.calc_bool= True
        self.line_edit.setText(self.line_edit.text() + txt)
    
    def on_point_click(self, txt):
        if not self.calc_bool:
            self.line_edit.setText("0")
        if self.line_edit.text().find(".") < 0:
            self.line_edit.setText(self.line_edit.text() + txt)
        self.calc_bool= True
            
    def on_clear_click(self):
        self.line_edit.setText("0")
        self.first_num = ""
        self.sec_num = ""
        self.oper = ""
        self.calc_bool= False
        
    def on_switch_sign(self):
        self.calc_bool= False
        if self.line_edit.text().find(".") > -1:
            self.line_edit.setText(str(-1 * float(self.line_edit.text())))
        else:
            self.line_edit.setText(str(-1 * int(self.line_edit.text())))
            
    def on_percent_button(self):
        self.calc_bool= False
        self.line_edit.setText(str(float(self.line_edit.text()) / 100))
        
    def on_oper_button(self, oper):
        if not self.calc_bool:
            self.first_num = ""
            self.sec_num = ""
            self.oper = ""
        if self.first_num == "":
            self.first_num = self.line_edit.text()
        elif self.sec_num == "":
            self.sec_num = self.line_edit.text()
        if self.first_num and self.sec_num:
            self.line_edit.setText(str(eval(f"{self.first_num} {self.oper} {self.sec_num}")))
        self.oper = oper
        self.calc_bool = False
        
    def on_equal_button(self):
        if self.first_num and not self.sec_num:
            self.sec_num = self.line_edit.text()
        if self.first_num and self.sec_num:
            self.line_edit.setText(str(eval(f"{self.first_num} {self.oper} {self.sec_num}")))
            self.first_num = self.line_edit.text()
        self.calc_bool = False
            
            
        
    def select_font(self):
        ok, font = QFontDialog.getFont()
        font.setPointSize(32)
        self.line_edit.setFont(font)