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
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from utils.first_view import FirstView
from utils.meds_list_view import MedsList

window_width: int = 1200
window_height: int = 700


class MedsApp(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.start()
        
    def start(self):
        self.setWindowTitle("How long til my meds")
        self.resize(window_width, window_height)

        #---------------------------------------------------------
        # Create stack
        self.first = FirstView()
        self.list_meds = MedsList()
        
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.first)
        self.stack.addWidget(self.list_meds)
        
        self.setCentralWidget(self.stack)
        
        #---------------------------------------------------------
        # Connect to signals
        self.first.open_meds_list.connect(self.open_meds_list)
        self.list_meds.close_meds_list.connect(self.close_meds_list)
        
    def open_meds_list(self) -> None:
        self.stack.setCurrentWidget(self.list_meds)
        
    def close_meds_list(self) -> None:
        self.stack.setCurrentWidget(self.first)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedsApp()
    window.show()
    sys.exit(app.exec())