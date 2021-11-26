from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QPushButton

import sys

# GLOBAL
PI = "3.415926535897932384626433832795"

from calculatrice.Calculatrice import Ui_Calculatrice


class Calculatrice(QMainWindow):
    def __init__(self):

        self.token = []
        self.touche = ""
        self.precision = 2
        self.number = ""
        self.screen = "0"
        self.sub_screen = ""
        self.result = ""

        QMainWindow.__init__(self)
        self.ui = Ui_Calculatrice()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(2)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 190))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.ui.label_text.setText("0")
        self.ui.lcdNumber.setText("")
        self.buttons = self.findChildren(QPushButton)

        for button in self.buttons:
            button.clicked.connect(self.guiPressEvent)

        self.operator = False
        self.validator = False
        self.ui.pushClose.disconnect()
        self.ui.pushClose.clicked.connect(self.closewindows)
        self.ui.dial.valueChanged.connect(self.value_precision)
        self.ui.dial.setValue(self.precision)

    def key_touches(self, touche):
        if touche in "0123456789,.":
            return touche

        return self.touche

    def key_operator(self, touche):
        if touche in "*/-+=,.":
            return touche

        return self.touche

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        print(event.text())
        self.touche = ""
        key = str(event.text())

        self.touche = self.key_touches(key)

        self.touche = self.key_operator(key)

        if event.key() == Qt.Key_BackForward:
            self.touche = "BACK"

        if event.key() == Qt.Key_Delete:
            self.touche = "BACK"

        if event.key() == Qt.Key_Return:
            self.touche = "="

        if event.text() == "C":
            self.touche = "C"

        if event.text == "%":
            self.touche = "PERCENT"

        if event.key() == Qt.Key_Up:
            self.precision += 1;
            if self.precision > 15:
                self.precision = 15
            self.ui.dial.setValue(self.precision)

        if event.key() == Qt.Key_Down:
            self.precision -= 1;
            if self.precision > 3:
                self.precision = 3
            self.ui.dial.setValue(self.precision)

        if event.key() == Qt.Key_Alt and event.key() == Qt.Key_F4:
            self.close()

        self.display_ui()

    def guiPressEvent(self):
        btn: QPushButton = self.sender()
        self.touche = str(btn.text())

        if self.ui.pushButton_back == btn:
            self.touche = "BACK"
        if self.touche == ",":
            self.touche = "."

        if self.touche == "%":
            self.touche = "PERCENT"

        if self.touche == "1/x":
            self.touche = "INVERSE"

        self.display_ui()

    def lcd(self, value):
        self.screen = self.floating_decimals(value, self.precision)
        self.ui.lcdNumber.setText(self.screen)

    def value_precision(self):
        style = "<b>précision:</b> {PREC} chiffres"
        self.precision = self.ui.dial.value()
        style = style.replace("{PREC}", str(self.precision))
        self.ui.label.setText(style)
        self.lcd(self.screen)

    def closewindows(self):
        self.close()

    def is_operator(self, token):
        if token in "+-/*":
            return True

        return False

    def floating_decimals(self, str_val, dec):
        if str_val == "":
            str_val = "0.0"

        if str_val[-1] == ".":  # si le nombre est en constitution on ne convertit rien on sort
            return str_val

        if "." in str_val:
            prc = "{:." + str(dec) + "f}"  # first cast decimal as str
            print(prc)  # str format output is {:.3f}
            return prc.format(float(str_val))
        else:
            return str_val

    def convert_point(self, number):
        if ',' in number:
            number = number.replace(",", ".")
        return number

    def verify(self, number):
        if number == "":
            return ""

        number = self.convert_point(number)
        l = len(number)
        if number[l - 1] == ".":
            return number

        if "." in number:  # on verfier que le nombre est décimal
            f_number = float(number)
            number = self.floating_decimals(str(f_number), self.precision)
        else:  # sinon c'est un entier
            i_number = int(number)
            number = str(i_number)

        return number

    def insert(self, number):
        self.token.append(self.verify(number))

    def push_back(self):
        l = len(self.number)
        self.touche = ""

        if l <= 1:
            self.screen = "0"
            self.number = ""
            self.sub_screen = ""
            self.lcd(self.screen)
            self.ui.label_text.setText(self.sub_screen)
            return

        self.number = self.number[0:l - 1]

        if self.number[-1] == ".":  # pour eviter 3.
            l = len(self.number)
            self.number = self.number[0:l - 1]

        str_number = self.verify(str(self.number))
        self.screen = str_number
        self.lcd(self.screen)

        l = len(self.sub_screen)
        self.sub_screen = self.sub_screen[0:l - 1]

        if self.sub_screen[-1] == ".":  # pour eviter 3.
            l = len(self.sub_screen)
            self.sub_screen = self.sub_screen[0:l - 1]

        self.operator = False

    def clear_screen(self):
        self.screen = "0"
        self.number = ""
        self.sub_screen = ""
        self.lcd(self.screen)
        self.ui.label_text.setText(self.sub_screen)

    def plus_minus(self):
        if "-" in self.screen:
            self.screen = self.screen.replace("-", "")
        else:
            self.screen = "-" + self.screen

    def display_ui(self):

        if self.touche == "BACK":
            self.touche = ""
            if self.validator:
                self.result = ""
                self.clear_screen()
            else:
                self.push_back()

        if self.operator:
            self.operator = False
            self.screen = ""
            self.number = ""

        if self.touche == ".":
            if "." in self.number:
                self.touche = ""
                pass
            else:
                self.number += self.touche

        if self.touche in "0123456789,":

            if self.validator:
                self.validator = False
                self.sub_screen = ""
                self.ui.label_text.setText("0")
                self.number = ""
            # self.screen += touche
            if len(self.touche) > 0:
                self.number += self.touche
            if len(self.number) > 0:
                str_number = self.verify(str(self.number))
                self.screen = str_number

        if self.touche in "+-/*" and len(self.touche) == 1:

            if len(self.sub_screen) == 0:
                return

            if "=" in self.sub_screen:
                return
            self.operator = True

        if self.touche == "C":
            self.touche=""
            self.screen = "0"
            self.sub_screen = ""
            self.ui.label_text.setText(self.sub_screen)
            self.ui.lcdNumber.setText(self.screen)

        if self.touche == "=":
            if self.sub_screen.count(self.touche) > 1:
                return
            if len(self.sub_screen) > 2:
                self.calculate()
            else:
                self.sub_screen = ""
                self.screen = ""
        if self.touche == "+/-":
            self.plus_minus()

        if self.touche == "x²":
            self.sub_screen = self.sub_screen.replace(self.touche, "")
            self.sub_screen += "*" + self.screen
            self.calculate()
            self.touche = ""

        if self.touche == "PERCENT":
            self.sub_screen = self.sub_screen.replace("%", "")
            self.sub_screen = self.sub_screen[:-1]
            self.sub_screen += self.screen + "/100"
            self.calculate()
            self.touche = ""

        if self.touche == "INVERSE":
            self.sub_screen = self.sub_screen.replace("1/X", "")
            self.sub_screen = self.sub_screen[:-1]
            self.sub_screen += "1/" + self.screen
            self.calculate()
            self.touche = ""

        if len(self.touche) > 0:
            self.sub_screen += self.touche
            self.sub_screen = self.convert_point(self.sub_screen)

            self.screen = self.floating_decimals(self.screen, self.precision)
            self.ui.lcdNumber.setText(self.screen)

        self.ui.label_text.setText(self.sub_screen)
        self.touche = ""

    def calculate(self):
        try:
            if "=" in self.sub_screen:
                val = str(eval(self.sub_screen[:-1]))
                self.validator = True
            else:
                val = str(eval(self.sub_screen))
                self.validator = False

            self.result = self.floating_decimals(val, self.precision)
            # self.sub_screen += touche
            self.screen = self.result
            self.ui.lcdNumber.setText(self.screen)
            self.ui.label_text.setText(self.sub_screen)

        except:
            self.ui.label_text.setText("Erreur")
            self.ui.lcdNumber.setText("Err")


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Calculatrice()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
