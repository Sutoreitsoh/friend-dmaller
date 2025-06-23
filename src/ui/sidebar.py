from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt
from logic.token_manager import TokenManager
from logic.message_manager import MessageManager
from logic.process_manager import ProcessManager
import os

class A(QWidget):
    def __init__(self, a=None):
        super().__init__(a)
        self.a1 = TokenManager()
        self.a2 = MessageManager()
        self.a3 = ProcessManager(self.a1, self.a2)
        self.a4()

    def a4(self):
        self.setFixedWidth(240)
        self.setStyleSheet("""
            QWidget { background-color: #181818; color: #ff4c4c; font-size: 15px; }
            QPushButton {
                background-color: #ff2222; color: white; border-radius: 8px;
                padding: 10px; font-size: 16px; margin-bottom: 10px;
            }
            QPushButton:hover { background-color: #ff4c4c; }
            QLabel { color: #ff4c4c; font-weight: bold; font-size: 17px; }
            QTextEdit, QSpinBox {
                background: #222; color: #fff; border: 1px solid #ff4c4c;
                border-radius: 5px; margin-bottom: 10px;
            }
            QListWidget {
                background: #222; color: #ff4c4c; border: none;
                font-size: 16px; margin-bottom: 20px;
            }
        """)

        b = QVBoxLayout(self)
        b.setAlignment(Qt.AlignTop)

        b.addWidget(QLabel("Straizo's Dmall", alignment=Qt.AlignCenter))
        b.addSpacing(15)

        self.b1 = QLabel(f'Tokens prêts : {self.a1.count_tokens()}')
        b.addWidget(self.b1)

        self.b2 = QPushButton('Vider tokens.txt')
        self.b2.clicked.connect(self.b3)
        b.addWidget(self.b2)

        self.b4 = QTextEdit()
        self.b4.setPlaceholderText('Ajoute tes tokens (1 par ligne ou séparés par virgule)')
        self.b4.setFixedHeight(80)
        b.addWidget(self.b4)

        self.b5 = QPushButton('Valider les tokens')
        self.b5.clicked.connect(self.b6)
        b.addWidget(self.b5)

        b.addSpacing(10)
        b.addWidget(QLabel('Message à envoyer :'))

        self.b7 = QTextEdit()
        self.b7.setPlaceholderText('Écris ton message ici...')
        self.b7.setFixedHeight(80)
        self.b7.setText(self.a2.read_messages())
        b.addWidget(self.b7)

        self.b8 = QPushButton('Valider le message')
        self.b8.clicked.connect(self.b9)
        b.addWidget(self.b8)

        b.addSpacing(10)
        b.addWidget(QLabel('Délai entre DM (secondes) :'))

        self.c1 = QSpinBox()
        self.c1.setRange(1, 60)
        self.c1.setValue(self.c2())
        self.c1.valueChanged.connect(self.c3)
        b.addWidget(self.c1)

        b.addSpacing(20)
        self.c4 = QPushButton('PANIC')
        self.c4.setStyleSheet("background:#ff2222; color:white; font-weight:bold; border-radius:8px;")
        self.c4.clicked.connect(self.c5)
        b.addWidget(self.c4)

        b.addStretch(1)

    def b6(self):
        d = self.b4.toPlainText()
        e = [f.strip() for f in d.replace(',', '\n').split('\n') if f.strip()]
        self.a1.save_tokens(e)
        self.b1.setText(f'Tokens prêts : {self.a1.count_tokens()}')
        QMessageBox.information(self, 'Succès', f'{len(e)} tokens enregistrés !')

    def b9(self):
        g = self.b7.toPlainText()
        self.a2.write_messages(g)
        QMessageBox.information(self, 'Succès', 'Message sauvegardé !')

    def b3(self):
        self.a1.clear_tokens()
        self.b1.setText(f'Tokens prêts : {self.a1.count_tokens()}')
        QMessageBox.information(self, 'Succès', 'Tokens vidés avec succès !')

    def c5(self):
        self.a3.halt_process()
        QMessageBox.warning(self, 'PANIC', 'Process stoppé !')

    def find_env_path(self):
        cwd = os.path.join(os.getcwd(), ".env")
        if os.path.exists(cwd):
            return cwd
        script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(script_dir):
            return script_dir
        parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
        if os.path.exists(parent_dir):
            return parent_dir
        return parent_dir

    def c3(self, h):
        i = self.find_env_path()
        j = []
        k = False
        if os.path.exists(i):
            with open(i, 'r', encoding='utf-8') as l:
                for m in l:
                    if m.startswith("Delay="):
                        j.append(f"Delay={h}\n")
                        k = True
                    else:
                        j.append(m)
        if not k:
            j.append(f"Delay={h}\n")
        with open(i, 'w', encoding='utf-8') as n:
            n.writelines(j)
        QMessageBox.information(self, 'Succès', f'Délai modifié à {h} seconde(s) !')

    def c2(self):
        try:
            i = self.find_env_path()
            with open(i, 'r', encoding='utf-8') as o:
                for p in o:
                    if p.startswith("Delay="):
                        return int(p.strip().split('=')[1])
        except:
            pass
        return 2