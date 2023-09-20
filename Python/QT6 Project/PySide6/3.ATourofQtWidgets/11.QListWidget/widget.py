from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget, QListWidget, QAbstractItemView, QVBoxLayout, QPushButton
from functools import partial

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QListWidget")
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget.addItem("One")
        self.list_widget.addItems(["Two", "Three"])
        
        self.list_widget.currentItemChanged.connect(self.current_item_changed)
        self.list_widget.currentTextChanged.connect(self.current_text_changed)
        
        add_button = QPushButton("Add Item")
        #add_button.clicked.connect(lambda: self.add_new_item("A"))
        add_button.clicked.connect(partial(self.add_new_item,"A"))
        
        delete_button = QPushButton("Delete Item")
        delete_button.clicked.connect(self.delete_item)
        
        count_button = QPushButton("Selection Count")
        count_button.clicked.connect(self.count_list)
        
        selected_item_button = QPushButton("Selected Items")
        selected_item_button.clicked.connect(self.selected_item)
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(count_button)
        layout.addWidget(selected_item_button)
        
        self.setLayout(layout)
        
    def current_item_changed(self, new, old):
        print(f"Old Value: {old.text()}, New Value: {new.text()}")
        
    def current_text_changed(self, text):
        print(f"Value: {text}")
        
    def add_new_item(self, item):
        self.list_widget.addItem(item)
        
    def delete_item(self):
        self.list_widget.takeItem(self.list_widget.currentRow())
        
    def count_list(self):
        print(f"No. of Items: {self.list_widget.count()}")
        
    def selected_item(self):
        items = self.list_widget.selectedItems()
        
        for i in items:
            print(i.text())