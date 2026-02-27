import sys
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMessageBox, QTextEdit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())