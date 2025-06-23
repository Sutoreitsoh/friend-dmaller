from PyQt5 import QtWidgets
import sys
from ui.main_window import Z

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Z()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()