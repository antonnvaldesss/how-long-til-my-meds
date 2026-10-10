import os

from .. import colors
from db import sqlite

from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QDialog,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from styles import global_style, add_meds_style

class AddMeds(QWidget):
    
    close_add_meds_signal = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(global_style.global_style)
        self.setStyleSheet(add_meds_style.add_style)
        
        my_layout = QVBoxLayout(self)
        my_layout.setContentsMargins(20, 2, 20, 2)
        
        dose_layout = QHBoxLayout()
        hour_minutes_layout = QHBoxLayout()
        date_layout = QHBoxLayout()
        time_layout = QHBoxLayout()
        
        save_cancel_layout = QHBoxLayout()
        
        self.database = sqlite.Database()
        
        #---------------------------------------------------------
        # Labels, buttons...
        # - Medicine name
        self.med_name = QLabel("Name:")
        self.med_name_insert = QLineEdit()
        self.med_name_insert.setPlaceholderText("Eg: Paracetamol, Ibuprofen")
    
        # - Medicine dose
        self.med_dose = QLabel("Dose:")
        self.med_dose_insert = QLineEdit()
        self.med_dose_insert.setValidator(QIntValidator())
        self.med_dose_insert.setPlaceholderText("Eg: 100mg, 1g")
        
        self.med_dose_unit = QComboBox()
        self.med_dose_unit.addItems(["mg", "g", "mcg", "ml", "l"])
    
        # - Medicine's first hour taken
        self.med_first_hour = QLabel("Hour of first dose:")
        self.med_first_hour_insert = QLineEdit()
        self.med_first_hour_insert.setPlaceholderText("Hour")
        
        self.med_first_minutes_insert = QLineEdit()
        self.med_first_minutes_insert.setPlaceholderText("Minutes")
        
        self.med_first_hour_insert.setValidator(QIntValidator())
        self.med_first_minutes_insert.setValidator(QIntValidator())
        
        self.med_hour_format = QComboBox()
        self.med_hour_format.addItems(["AM", "PM", "Military"])
        
        # - Medicine's first day taken
        self.med_first_day_dose = QLabel("Date of first dose:")
        self.med_first_day_insert = QLineEdit()
        self.med_month_insert = QLineEdit()
        self.med_year_insert = QLineEdit()
        
        self.med_first_day_insert.setPlaceholderText("Day")
        self.med_month_insert.setPlaceholderText("Month")
        self.med_year_insert.setPlaceholderText("Year")

        self.med_first_day_insert.setValidator(QIntValidator())
        self.med_month_insert.setValidator(QIntValidator())
        self.med_year_insert.setValidator(QIntValidator())
        
        # - Medicine's time
        self.med_schedule = QLabel("Take every...:")
        self.med_number_time_insert = QLineEdit()
        self.med_number_minutes_insert= QLineEdit()
        self.med_number_minutes_insert.hide()
        self.med_number_time_insert.setValidator(QIntValidator())

        self.med_time_format = QComboBox()
        self.med_time_format.addItems(["Hours", "Days", "Months", "Years"])
        self.med_time_format.currentTextChanged.connect(self.change_time_format_schedule)
        self.change_time_format_schedule(self.med_time_format.currentText())
        
        # - Cancel and save buttons + warning message
        self.warning_message = QLabel()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.setProperty("class", "save_button")
        self.cancel_button.setProperty("class", "cancel_button")
        
        #---------------------------------------------------------
        # Layout application
        # - Medicine's time layout
        time_layout.addWidget(self.med_number_time_insert)
        time_layout.addWidget(self.med_number_minutes_insert)
        time_layout.addWidget(self.med_time_format)
        
        # - Dose layout
        dose_layout.addWidget(self.med_dose_insert)
        dose_layout.addWidget(self.med_dose_unit)
        
        # - Medicine's first hour taken
        hour_minutes_layout.addWidget(self.med_first_hour_insert)
        hour_minutes_layout.addWidget(self.med_first_minutes_insert)
        hour_minutes_layout.addWidget(self.med_hour_format)
        
        # - Medicine's first day taken
        date_layout.addWidget(self.med_first_day_insert)
        date_layout.addWidget(self.med_month_insert)
        date_layout.addWidget(self.med_year_insert)
        
        save_cancel_layout.addWidget(self.warning_message)
        save_cancel_layout.addWidget(self.cancel_button)
        save_cancel_layout.addWidget(self.save_button)
        
        my_layout.addWidget(self.med_name)
        my_layout.addWidget(self.med_name_insert)
        
        # - Add doses to main layout
        my_layout.addWidget(self.med_dose)
        my_layout.addLayout(dose_layout)
        
        # - Add first hour to main layout
        my_layout.addWidget(self.med_first_hour)
        my_layout.addLayout(hour_minutes_layout)
        
        # - Add first day to main layout
        my_layout.addWidget(self.med_first_day_dose)
        my_layout.addLayout(date_layout)
    
        my_layout.addWidget(self.med_schedule)
        my_layout.addLayout(time_layout)

        my_layout.addLayout(save_cancel_layout)
        
        #---------------------------------------------------------
        # Signals
        
        self.cancel_button.clicked.connect(self.close_add_meds_signal.emit)
        self.save_button.clicked.connect(self.save_medicine)
        
    def change_time_format_schedule(self, text):
            if text == "Hours":
                self.med_number_minutes_insert.show()
                self.med_number_minutes_insert.setPlaceholderText("Minutes")
                self.med_number_time_insert.setPlaceholderText("Hours")
            else:
                self.med_number_time_insert.setPlaceholderText("")
                self.med_number_minutes_insert.hide()

    def save_medicine(self):
        name = self.med_name_insert.text()
        dose = self.med_dose_insert.text()
        dose_unit = self.med_dose_unit.currentText()

        hour_first_dose = self.med_first_hour_insert.text()
        minutes_first_dose = self.med_first_minutes_insert.text()
        hour_format = self.med_hour_format.currentText()
        
        day_first_dose = self.med_first_day_insert.text()
        month_first_dose = self.med_month_insert.text()
        year_first_dose = self.med_year_insert.text()
        
        schedule_time = self.med_number_time_insert.text()
        schedule_minutes = self.med_number_minutes_insert.text()
        schedule_format = self.med_time_format.currentText()
        
        if dose and int(dose) < 0:
            self.warning_message.setText("¡La dosis no puede ser negativa!")
            return
            
        if hour_first_dose:
            if (
                hour_format == "Military" and ((int(hour_first_dose) < 0)
                                               or (int(hour_first_dose) > 23))
            ):
                self.warning_message.setText("¡Hora inválida!")
                return
            if (
                hour_format == "PM" or hour_format == "AM") and ((int(hour_first_dose) > 12)
                                                                 or (int(hour_first_dose) < 1)
            ):
                self.warning_message.setText("¡Hora inválida!")
                return

        if (
            minutes_first_dose and ((int(minutes_first_dose) < 0)
                                    or (int(minutes_first_dose) > 59))
        ):
            self.warning_message.setText("¡Hora inválida!")
            return
        
        if (
            day_first_dose and ((int(day_first_dose) < 0)
                                or (int(day_first_dose) > 31))
        ):
            self.warning_message.setText("¡Fecha inválida!")
            return
            
        if month_first_dose and ((int(month_first_dose) < 0)
                                 or (int(month_first_dose) > 12)
        ):
            self.warning_message.setText("¡Fecha inválida!")
            return
            
        if year_first_dose and (int(year_first_dose) < 0):
            self.warning_message.setText("¡Fecha inválida!")
            return

        if schedule_time:
            if int(schedule_time) < 0:
                self.warning_message.setText("¡Cifra inválida!")
                return
            if (
                schedule_format == "Hours" and schedule_minutes and ((int(schedule_minutes) < 0)
                                                                      or (int(schedule_minutes) > 59))
            ):
                self.warning_message.setText("¡Hora inválida!")
                return
        
        if (not name
            or not dose
            or not hour_first_dose
            or not day_first_dose
            or not month_first_dose
            or not year_first_dose
            or not schedule_time
            ):
            self.warning_message.setText("¡Faltan datos!")
            return
        
        self.warning_message.setText("")
        print("yipee")
        
        print(name, dose, dose_unit)
        print(hour_first_dose, minutes_first_dose, hour_format)
        print(day_first_dose, month_first_dose, year_first_dose)
        print(schedule_time, schedule_minutes, schedule_format)
        
        if not minutes_first_dose:
            minutes_first_dose = 0
        if not schedule_minutes:
            schedule_minutes = 0
        
        db_hours_first_dose = f"{hour_first_dose}:{minutes_first_dose}"
        db_day_first_dose = f"{day_first_dose}-{month_first_dose}-{year_first_dose}"
        if schedule_format == "Hours":
            db_after_every = f"{schedule_time}:{schedule_minutes}"
        else:
            db_after_every = schedule_time

        self.database.create_medicine(name, dose, dose_unit,
                                      db_hours_first_dose,
                                      hour_format,
                                      db_day_first_dose,
                                      db_after_every,
                                      schedule_format)

        self.med_name_insert.setText("")
        self.med_dose_insert.setText("")

        self.med_first_hour_insert.setText("")
        self.med_first_minutes_insert.setText("")
        
        self.med_first_day_insert.setText("")
        self.med_month_insert.setText("")
        self.med_year_insert.setText("")
        
        self.med_number_time_insert.setText("")
        self.med_number_minutes_insert.setText("")
        
        self.close_add_meds_signal.emit()
        