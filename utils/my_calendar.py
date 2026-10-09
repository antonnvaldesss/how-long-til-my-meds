import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCalendarWidget
)


class Calendar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        self.calendar = QCalendarWidget(self)
        
        layout.addWidget(self.calendar)