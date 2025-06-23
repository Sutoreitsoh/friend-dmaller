from PyQt5 import QtWidgets, QtCore
import os

class Settings(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QtWidgets.QVBoxLayout()

        self.token_input = QtWidgets.QTextEdit()
        self.token_input.setPlaceholderText("Enter tokens here...")
        self.token_input.setFixedHeight(100)
        self.layout.addWidget(self.token_input)

        self.token_count_label = QtWidgets.QLabel("Token Count: 0")
        self.layout.addWidget(self.token_count_label)

        self.clear_tokens_button = QtWidgets.QPushButton("Clear Tokens")
        self.clear_tokens_button.clicked.connect(self.clear_tokens)
        self.layout.addWidget(self.clear_tokens_button)

        self.message_input = QtWidgets.QLineEdit()
        self.message_input.setPlaceholderText("Modify message...")
        self.layout.addWidget(self.message_input)

        self.delay_input = QtWidgets.QSpinBox()
        self.delay_input.setRange(1, 60)
        self.delay_input.setValue(2)
        self.layout.addWidget(QtWidgets.QLabel("Set Delay (seconds):"))
        self.layout.addWidget(self.delay_input)

        self.panic_button = QtWidgets.QPushButton("Panic Button")
        self.panic_button.clicked.connect(self.panic)
        self.layout.addWidget(self.panic_button)

        self.setLayout(self.layout)

        self.load_tokens()

    def load_tokens(self):
        if os.path.exists('src/tokens.txt'):
            with open('src/tokens.txt', 'r') as file:
                tokens = file.readlines()
                self.token_input.setPlainText(''.join(tokens))
                self.token_count_label.setText(f"Token Count: {len(tokens)}")

    def clear_tokens(self):
        self.token_input.clear()
        self.token_count_label.setText("Token Count: 0")
        with open('src/tokens.txt', 'w') as file:
            file.write('')

    def panic(self):
        print("Panic Button pressed! Halting process...")