from PySide6.QtWidgets import QWidget, QCheckBox, QRadioButton, QGroupBox, QVBoxLayout, QButtonGroup, QHBoxLayout

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        
        self.setWindowTitle("QCheckBox and QRadioButton")
        
        #Checkboxes Operating System
        os = QGroupBox("Choose Operating System")
        windows = QCheckBox("Windows")
        windows.toggled.connect(self.windows_box_toggled)
        
        linux = QCheckBox("Linux")
        linux.toggled.connect(self.linux_box_toggled)
        
        mac = QCheckBox("Mac")
        mac.toggled.connect(self.mac_box_toggled)
        
        os_layout = QVBoxLayout()
        os_layout.addWidget(windows)
        os_layout.addWidget(linux)
        os_layout.addWidget(mac)
        
        os.setLayout(os_layout)
        
        #Exclusive Checkbox
        drinks = QGroupBox("Select the Drink")
        
        beer = QCheckBox("Beer")
        coffee = QCheckBox("Coffee")
        juice = QCheckBox("Juice")
        
        beer.setChecked(True)
        
        #Make the checkbox exclusive: QButtonGroup will allow only one item to select
        
        execlusive_button_group = QButtonGroup(self) #Self parent needed here
        execlusive_button_group.addButton(beer)
        execlusive_button_group.addButton(coffee)
        execlusive_button_group.addButton(juice)
        
        drinks_layout = QVBoxLayout()
        drinks_layout.addWidget(beer)
        drinks_layout.addWidget(coffee)
        drinks_layout.addWidget(juice)
        
        #drinks_layout.addWidget(execlusive_button_group)
        
        drinks.setLayout(drinks_layout)
        
        #RadioButton
        answers = QGroupBox("Choose you Answer")
        
        answer_a = QRadioButton("A")
        answer_b = QRadioButton("B")
        answer_c = QRadioButton("C")
        
        answer_layout = QVBoxLayout()
        answer_layout.addWidget(answer_a)
        answer_layout.addWidget(answer_b)
        answer_layout.addWidget(answer_c)
        
        answers.setLayout(answer_layout)
        
        
        
        layout = QHBoxLayout()
        layout.addWidget(os)
        layout.addWidget(drinks)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(layout)
        v_layout.addWidget(answers)
        
        self.setLayout(v_layout)
        
    def linux_box_toggled(self, checked):
        if checked:
            print("Linux is Selected")
        else:
            print("Linux is unselected")
            
    def windows_box_toggled(self, checked):
        if checked:
            print("Windows is Selected")
        else:
            print("Windows is unselected")
            
    def mac_box_toggled(self, checked):
        if checked:
            print("Mac is Selected")
        else:
            print("Mac is unselected")
        