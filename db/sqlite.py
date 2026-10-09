import os
import sqlite3


class Database:
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "medicine.db")
        self.create_table()
    
    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS medicine (id INTEGER PRIMARY KEY,
                                                            name TEXT NOT NULL,
                                                            dose INTEGER NOT NULL CHECK (dose > 0),
                                                            dose_unit TEXT NOT NULL,
                                                            hour_first_dose TEXT NOT NULL,
                                                            hour_format TEXT NOT NULL,
                                                            day_first_dose TEXT NOT NULL,
                                                            after_every INTEGER NOT NULL CHECK (after_every > 0),
                                                            after_every_format TEXT NOT NULL)
                       """)
        conn.commit()
        conn.close()
    
    def create_medicine(self, name, dose, dose_unit, hours_first_dose,
                        hour_format, day_first_dose, after_every,
                        after_every_format):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO medicine (name, dose, dose_unit,
                       hour_first_dose, hour_format, day_first_dose,
                       after_every, after_every_format) VALUES
                       (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (name, dose, dose_unit, hours_first_dose,
                             hour_format, day_first_dose, after_every,
                             after_every_format))
        conn.commit()
        conn.close()
        
    def get_all_medicine(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicine")
        conn.commit()
        conn.close()