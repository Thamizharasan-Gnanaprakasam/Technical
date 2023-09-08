import sys

from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6 import QtCore
from bs4 import BeautifulSoup as bs
import requests as req


class ForeignExchange:
    def __init__(self):
        self.frm_ccy: str = ""
        self.to_ccy: str = ""
        self.amt: str = ""
        self.ccy_url: str= "https://www.x-rates.com/"


        self.ccy_cd = self.select_tag(self.get_url_content(self.ccy_url),
                                 "div#fromInput select#from option",
                                multi_tag=True,
                                 only_value=False,
                                 attrs="value"
                                 )

        self.frm_ccy = "USD"
        self.to_ccy = "INR"

        inp = "123"
        self.amt = inp

        self.pattern1 = "span.ccOutputRslt"
        self.pattern2 = "span.ccOutputTrail, span.ccOutputCode"
        self.exchng_url: str = f"https://www.x-rates.com/calculator/?from={self.frm_ccy}&to={self.to_ccy}&amt={self.amt}"

        self.exchng_html = self.select_tag(self.get_url_content(self.exchng_url),
                                           self.pattern1,
                                           only_html=True,
                                           only_value=False)


        self.trail_value ="".join(self.select_tag(self.exchng_html,
                                          self.pattern2,
                                          multi_tag=True))

        print(self.trail_value)
        print(self.exchng_html.text.replace(self.trail_value,""))




    def get_url_content(self, url: str) -> bs:
        content = req.get(url).content
        return bs(content, "html.parser")

    def select_tag(self,soup: bs, pattern: str,multi_tag: bool = False, only_html: bool = False, only_value: bool = True, attrs: str=""):
        if multi_tag:
            if only_html:
                return [item for item in soup.select(pattern)]
            elif only_value:
                return [item.text for item in soup.select(pattern)]
            else:
                return {item.text: item.attrs[attrs] for item in soup.select(pattern)}
        else:
            if only_html:
                return soup.select_one(pattern)
            elif only_value:
                return soup.select_one(pattern).text
            else:
                return soup.select_one(pattern).attrs[attrs]



class MainWidget():
    def __init__(self):
        self.fx = ForeignExchange()

        self.window = QWidget()
        self.window.setWindowTitle("Foreign Exchange")

        self.vlayout = QVBoxLayout()

        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()

        self.from_label = QLabel("Enter Amount:")
        self.from_label.setMaximumHeight(40)
        self.from_label.setStyleSheet("font-size: 15px")
        self.from_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.num_valid = QDoubleValidator()
        self.from_text = QLineEdit("1")
        self.from_text.setPlaceholderText("Enter Amount")
        self.from_text.setMaximumHeight(35)
        self.from_text.setValidator(self.num_valid)
        self.from_text.setStyleSheet("font-size: 15px")
        self.from_text.textChanged.connect(self.calc_rate)


        self.frm_ccy_combo = QComboBox()
        self.frm_ccy_combo.addItems(self.fx.ccy_cd.keys())
        self.frm_ccy_combo.setCurrentText("USD - US Dollar")
        self.frm_ccy_combo.currentTextChanged.connect(self.calc_rate)

        self.to_label = QLabel("Exchange Amount:")
        self.to_label.setMaximumHeight(40)
        self.to_label.setStyleSheet("font-size: 15px")
        self.to_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.to_label_val = QLabel("")
        self.to_label_val.setMaximumHeight(40)
        self.to_label_val.setStyleSheet("font-size: 15px")
        self.to_label_val.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.to_ccy_combo = QComboBox()
        self.to_ccy_combo.addItems(self.fx.ccy_cd.keys())
        self.to_ccy_combo.setCurrentText("EUR - Euro")
        self.to_ccy_combo.currentTextChanged.connect(self.calc_rate)
        #self.to_ccy_combo.currentTextChanged(self.calc_rate())

        self.ex_rate_lbl = QLabel("Today's Exchange Rate: ")
        self.ex_rate_lbl.setStyleSheet("font-size: 15px")
        self.ex_rate_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.btn = QPushButton("Get Value")
        self.btn.clicked.connect(self.calc_rate)






        self.hlayout1.addWidget(self.from_label)
        self.hlayout1.addWidget(self.from_text)
        self.hlayout1.addWidget(self.frm_ccy_combo)

        self.hlayout2.addWidget(self.to_label)
        self.hlayout2.addWidget(self.to_label_val)
        self.hlayout2.addWidget(self.to_ccy_combo)

        self.hlayout3.addWidget(self.ex_rate_lbl)
        #self.hlayout3.addWidget(self.btn)



        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.window.setLayout(self.vlayout)
        self.calc_rate()
        self.window.show()

    def calc_rate(self):
        try:
            exchng_url: str = f"https://www.x-rates.com/calculator/?from={self.fx.ccy_cd[self.frm_ccy_combo.currentText()]}&to={self.fx.ccy_cd[self.to_ccy_combo.currentText()]}&amt={self.from_text.text()}"
            print(exchng_url)
            pattern1 = "span.ccOutputRslt"
            pattern2 = "span.ccOutputTrail, span.ccOutputCode"

            exchng_html = self.fx.select_tag(self.fx.get_url_content(exchng_url),
                                               pattern1,
                                               only_html=True,
                                               only_value=False)
            print(exchng_html)

            trail_value = "".join(self.fx.select_tag(exchng_html,
                                                       pattern2,
                                                       multi_tag=True))

            self.ex_rate_lbl.setText("Today's Exchange Rate: 1 " + self.frm_ccy_combo.currentText() +" is " + exchng_html.text.replace(trail_value, "") + " " + self.to_ccy_combo.currentText())
            self.to_label_val.setText(str(float(self.from_text.text()) * float(exchng_html.text.replace(trail_value, ""))))
        except Exception as e:
            print(e)



app = QApplication(sys.argv)

window = MainWidget()

sys.exit(app.exec())
