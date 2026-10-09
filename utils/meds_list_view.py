import os
import sys

import utils.colors as colors

from utils.my_calendar import Calendar
from utils.add_meds.add_meds import AddMeds
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MedsList(QWidget):
    
    close_meds_list = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {colors.dark_blue};")

        self.add_meds = AddMeds(self)
        self.add_meds.hide()

        # Layouts
        layout = QVBoxLayout(self)
        edit_buttons_layout = QHBoxLayout()

        # Buttons
        self.back_button = QPushButton("<")
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        
        #---------------------------------------------------------
        # Layouts application
        layout.addWidget(self.back_button)
        edit_buttons_layout.addWidget(self.edit_button)
        edit_buttons_layout.addWidget(self.add_button)
        layout.addLayout(edit_buttons_layout)
        
        self.back_button.clicked.connect(self.close_meds_list.emit)
        self.add_button.clicked.connect(self.open_add_meds)
        
        #---------------------------------------------------------
        # Signals
        self.add_meds.close_add_meds_signal.connect(self.close_add_meds)
        
    def open_add_meds(self):
        self.add_meds.setGeometry(self.rect())
        self.add_meds.show()
        self.add_meds.raise_()
    
    def close_add_meds(self):
        self.add_meds.hide()