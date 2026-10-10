import os
import sys

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
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView
)

import utils.colors as colors
from utils.add_meds.add_meds import AddMeds
from utils.my_calendar import Calendar

from db import sqlite
from styles import global_style


class MedsList(QWidget):
    
    close_meds_list = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        
        self.database = sqlite.Database()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(global_style.global_style)

        self.add_meds = AddMeds(self)
        self.add_meds.hide()

        #---------------------------------------------------------
        # Layouts
        layout = QVBoxLayout(self)
        edit_buttons_layout = QHBoxLayout()

        #---------------------------------------------------------
        # - Buttons
        self.back_button = QPushButton("<")
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        
        # - Meds
        all_meds = self.database.get_all_medicine()
        meds_count = len(all_meds)
        print(all_meds)

        self.meds_table = QTableWidget(meds_count + 1, 3)
        self.meds_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.meds_table.setItem(0, 0, QTableWidgetItem("Name"))
        self.meds_table.setItem(0, 1, QTableWidgetItem("Dose"))
        self.meds_table.setItem(0, 2, QTableWidgetItem("Every..."))
        
        for x in range(meds_count):
            self.meds_table.setItem(x + 1, 0, QTableWidgetItem(all_meds[x][1]))
            self.meds_table.setItem(x + 1, 1, QTableWidgetItem(f"{all_meds[x][2]} {all_meds[x][3]}"))
            
            if all_meds[x][8] == "Hours":
                hour_list = all_meds[x][7].split(":")
                print(hour_list)
                if len(hour_list[1]) == 1:
                    actual_minutes = f"0{hour_list[1]}"
                else:
                    actual_minutes = hour_list[1]
                actual_hour = f"{hour_list[0]}:{actual_minutes}"
                self.meds_table.setItem(x + 1, 2, QTableWidgetItem(f"{actual_hour} {all_meds[x][8]}"))
            else:
                self.meds_table.setItem(x + 1, 2, QTableWidgetItem(f"{all_meds[x][7]} {all_meds[x][8]}"))
        
        self.meds_table.verticalHeader().setVisible(False)
        self.meds_table.horizontalHeader().setVisible(False)
        
        #---------------------------------------------------------
        # Layouts application
        layout.addWidget(self.back_button)
        layout.addWidget(self.meds_table)
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