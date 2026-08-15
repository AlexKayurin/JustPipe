import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                               QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox)
from PySide6.QtGui import QFont, QIcon

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Third - Party Licenses')
        self.resize(600, 500)

        # Основной вертикальный слой
        layout = QVBoxLayout(self)

        # Поле для отображения текста лицензий
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Установка моноширинного шрифта для сохранения форматирования
        font = QFont('Courier New', 10)
        self.text_edit.setFont(font)

        # Загрузка текста из файла
        self.load_license_file()
        layout.addWidget(self.text_edit)

        # Кнопка закрытия окна (Стандартный набор Qt)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def load_license_file(self):
        # Находим путь к файлу лицензий рядом со скриптом
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'THIRD_PARTY_LICENSES.txt')

        try:
            with open(file_path, 'r', encoding ='utf - 8') as file:
                self.text_edit.setPlainText(file.read())
        except FileNotFoundError:
            self.text_edit.setPlainText('Error: THIRD_PARTY_LICENSES.txt file not found.')
        except Exception as e:
            self.text_edit.setPlainText(f'Error loading licenses: {str(e)}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        self.resize(400, 200)

        # Кнопка для вызова окна с лицензиями
        self.btn = QPushButton('Open About and Licenses', self)
        self.btn.clicked.connect(self.show_licenses)
        self.setCentralWidget(self.btn)

    def show_licenses(self):
        dialog = LicenseDialog(self)
        # exec() блокирует основное окно, пока диалог открыт
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

