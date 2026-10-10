from utils import colors

add_style = f"""
    QPushButton[class="save_button"] {{
        background-color: {colors.dark_teal}
    }}

    QPushButton[class="cancel_button"] {{
            background-color: {colors.light_teal}
        }}
        
    QLabel, QLineEdit, QPushButton, QComboBox {{
        font-family: Elms Sans;
    }}
    
    QLabel, QPushButton {{
            font-size: 25px;
        }}
        
    QLineEdit {{
        font-size: 20px;
    }}
"""
