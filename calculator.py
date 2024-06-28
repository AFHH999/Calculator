from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, 
)
from PySide6.QtCore import Qt
import sympy as sp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(361,486)

        # Creating a central widget and setting the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Creating the input field
        self.input_field = QLineEdit()
        main_layout.addWidget(self.input_field)

        # Creating the buttons
        grid_layout = QGridLayout()
        buttons = [
        ["C","⌫","(",")","/"],
        ["7","8","9","%","*"],
        ["4","5","6","π","-"],
        ["1","2","3","√","+"],
        ["0","00",".","+/-","="]
        ]
        
        for row, button_row in enumerate(buttons):
            for col, button_label in enumerate(button_row):
                button = QPushButton(button_label)
                button.clicked.connect(self.button_clicked)
                button.setObjectName("calculatorButton")
                # Add a separate selector for mathematical symbols buttons
                if button_label in ["/","*","-","+","+/-","=","%","C","⌫","(",")","π","√"]:
                    button.setObjectName("mathButton")
                grid_layout.addWidget(button, row, col)
        
        main_layout.addLayout(grid_layout)

         # Set the colors and styles
        self.setStyleSheet('''
            QPushButton#calculatorButton {
                background-color: #ed872d;
                color: white;
                font-size: 20px;
                padding: 10px;
                border-radius: 22px;
            }
            QWidget {
                background-color: #090909;
            }
            QLineEdit {
                background-color: #222222;
                color: white;
                font-size: 24px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton#mathButton {
                background-color: #222222;
                color: white;
                font-size: 24px;
                padding: 10px;
                border-radius: 22px;
            }
            QPushButton#mathButton:hover {
                background-color: #b3b3b3;
            }
            QPushButton#mathButton:pressed {
                background-color: #777777;
            }
            QPushButton#calculatorButton:hover {
                background-color: #ffae1a;
            }
            QPushButton#calculatorButton:pressed {
                background-color: #ff9206;
            }
        ''')

    def button_clicked(self):
        button = self.sender()  # Get the button that was clicked
        current_text = self.input_field.text()
        button_text = button.text() # Get the text on the clicked button

        if button_text == "C":
            self.input_field.clear()
        elif button_text == "⌫":
            self.input_field.setText(current_text[:-1])
        elif button_text == "=":
            try:
                result = self.calculate() # Calculate result
                self.input_field.setText(str(result)) # Display result
            except Exception as e:
                self.input_field.setText("Error")
        elif button_text == "π":
            self.input_field.setText(current_text + str(sp.pi)) 
        elif button_text == "√":
            self.input_field.setText(current_text + "sqrt(")
        elif button_text == "+/-":  # Toggle between positive and negative
            if current_text and current_text[0] == '-':
                self.input_field.setText(current_text[1:]) # Remove minus sing 
            else:
                self.input_field.setText('-' + current_text) # Add minus sing
        else:
            self.input_field.setText(current_text + button_text)

    def keyPressEvent(self, event):
        key = event.key() # Get the key code of the pressed key
        current_text = self.input_field.text()  # Get the current text in the input field
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            try:
                result = self.calculate()  # Try to calculate the result
                self.input_field.setText(str(result))  # Set the result in the input field
            except Exception as e:
                self.input_field.setText("Error")
        elif key == Qt.Key_Backspace: # If Backspace key is pressed
            self.input_field.setText(current_text[:-1])   # Remove the last character from the input field
        elif key == Qt.Key_Escape: # If Escape key is pressed
            self.input_field.clear() # Clear the input field
        else: 
            text = event.text() # Get the text representation of the key
            if text in "0123456789.+-*/()":
                # If the key is a valid calculator input
                self.input_field.setText(current_text + text)  # Add the text to the input field
        
        super().keyPressEvent(event) # Call the parent class's keyPressEvent method

    def get_input(self): # Return the text in the input field
        return self.input_field.text()
         
    def calculate(self):
        input_str = self.get_input() # Get the input string
        try:
            input_str = input_str.replace('π', str(sp.pi))  # Replace 'pi' with the actual value of pi
            expr = sp.sympify(input_str) # Convert string into SymPy expressions
            result = expr.evalf() # Evaluated the expression 
            return result
        except sp.SympifyError:
            raise ValueError("Invalid expression") # Raise error for invalid expression
        except Exception as e:
            raise ValueError(f"Error: {str(e)}") # Raise error for other exceptions