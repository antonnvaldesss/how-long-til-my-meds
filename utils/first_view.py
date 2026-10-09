import os
import sys

import utils.colors as colors

from utils.my_calendar import Calendar
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


class FirstView(QWidget):
    
    open_meds_list = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {colors.dark_blue};")

        # Layouts
        layout = QHBoxLayout(self)
        right_side = QVBoxLayout()

        #---------------------------------------------------------
        # Calendar, text, button, etc.    
        calendar_widget = Calendar()
        
        streak_text = QLabel("Meds Streak")
        next_med = QLabel("Next Med")
        
        meds_button = QPushButton("See Meds")  
        
        # Visuals
        # - Apply custom font
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "..", "assets", "fonts", "ElmsSans-Regular.ttf")
        id = QFontDatabase.addApplicationFont(font_path)
        families = QFontDatabase.applicationFontFamilies(id)
        print(families[0])
        
        streak_text.setFont(QFont("Elms Sans", 20))
        next_med.setFont(QFont("Elms Sans", 20))
        meds_button.setFont(QFont("Elms Sans", 20))
        
        #---------------------------------------------------------
        # Layouts application
        right_side.addWidget(streak_text)
        right_side.addWidget(next_med)
        right_side.addWidget(meds_button)
        layout.addWidget(calendar_widget)
        layout.addLayout(right_side)
        
        #---------------------------------------------------------
        # Functions
        meds_button.clicked.connect(self.open_meds_list.emit)