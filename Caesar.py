import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
)

# Частота символов в английском языке
letterFrequency = {
    'E': 0.13,
    'M': 0.25,
    'U': 0.105,
    'T': 0.24,
    'A': 0.81,
    'G': 2.00,
    'O': 0.79,
    'P': 0.018,
    'Y': 0.012,
    'N': 0.71,
    'W': 0.012,
    'R': 0.68,
    'I': 0.055,
    'B': 0.011,
    'S': 0.61,
    'V': 0.008,
    'H': 0.52,
    'K': 0.047,
    'D': 0.38,
    'X': 0.001,
    'L': 0.34,
    'J': 0.001,
    'F': 0.29,
    'Q': 0.001,
    'C': 0.27,
    'Z': 0.001
}

# Функция подсчета числа разных букв и нахождения их частот
def findFrequency(text, referenceFrequency):
    letterDict = dict()
    for letter in text:
        if letter.isalpha():
            letterDict[letter.upper()] = letterDict.get(letter.upper(), 0) + 1
    difference = 0
    for letter in referenceFrequency:
        difference += abs(letterDict.get(letter, 0) - referenceFrequency.get(letter, 0))
    return difference

# Функция шифрования текста
def encryptText(text, shift):
    encryptedText = ""
    for letter in text:
        if letter.isalpha():
            base = ord('A') if letter.isupper() else ord('a')
            encryptedLetter = chr((ord(letter) - base + shift) % 26 + base)
            encryptedText += encryptedLetter
        else:
            encryptedText += letter
    return encryptedText

# Функция дешифровки
def decryptText(text, shift):
    return encryptText(text, -shift)

# Взлом шифра
def crackCipher(encryptedText, referenceFrequency):
    minDifference = float('inf')
    bestShift = 0
    bestDecryption = ''
    for shift in range(26):
        decryptedText = decryptText(encryptedText, shift)
        difference = findFrequency(decryptedText, referenceFrequency)
        if difference < minDifference:
            minDifference = difference
            bestShift = shift
            bestDecryption = decryptedText
    return bestShift, bestDecryption

# Основной класс приложения
class Caesar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.inputTextField = QTextEdit(self)
        self.inputTextField.setPlaceholderText("Введите текст")
        mainLayout.addWidget(QLabel("Введите текст:"))
        mainLayout.addWidget(self.inputTextField)

        self.shiftInputField = QTextEdit(self)
        self.shiftInputField.setPlaceholderText("Введите сдвиг")
        self.shiftInputField.setFixedHeight(30)
        mainLayout.addWidget(QLabel("Введите сдвиг:"))
        mainLayout.addWidget(self.shiftInputField)

        buttonLayout = QHBoxLayout()
        self.encryptButton = QPushButton("Шифровать", self)
        self.encryptButton.clicked.connect(self.handleEncryption)
        buttonLayout.addWidget(self.encryptButton)

        self.decryptButton = QPushButton("Расшифровать", self)
        self.decryptButton.clicked.connect(self.handleDecryption)
        buttonLayout.addWidget(self.decryptButton)

        self.crackButton = QPushButton("Взломать", self)
        self.crackButton.clicked.connect(self.handleCracking)
        buttonLayout.addWidget(self.crackButton)

        mainLayout.addLayout(buttonLayout)

        self.resultTextField = QTextEdit(self)
        self.resultTextField.setReadOnly(True)
        mainLayout.addWidget(QLabel("Результат:"))
        mainLayout.addWidget(self.resultTextField)

        self.shiftLabel = QLabel("Лучший сдвиг: ")
        mainLayout.addWidget(self.shiftLabel)

        # Установка макета
        self.setLayout(mainLayout)
        self.setWindowTitle("Шифр Цезаря")
        self.setGeometry(100, 100, 600, 600)

    def handleEncryption(self):
        text = self.inputTextField.toPlainText()
        shift = self.shiftInputField.toPlainText()

        if not shift.isdigit():
            QMessageBox.warning(self, "Введите в поле сдвиг целое число!")
            return

        shift = int(shift)
        encryptedText = encryptText(text, shift)
        self.resultTextField.setPlainText(encryptedText)

    def handleDecryption(self):
        text = self.inputTextField.toPlainText()
        shift = self.shiftInputField.toPlainText()

        if not shift.isdigit():
            QMessageBox.warning(self, "Введите в поле сдвиг целое число!")
            return

        shift = int(shift)
        decryptedText = decryptText(text, shift)
        self.resultTextField.setPlainText(decryptedText)

    def handleCracking(self):
        text = self.inputTextField.toPlainText()
        bestShift, bestDecryption = crackCipher(text, letterFrequency)
        self.resultTextField.setPlainText(bestDecryption)
        self.shiftLabel.setText(f"Вероятный сдвиг: {bestShift}")

# Точка входа
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Caesar()
    window.show()
    sys.exit(app.exec_())