"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtGui, QtCore
from d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.numbParameters = QtCore.QSettings("param")

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.dial.setMinimum(0)
        self.ui.dial.setMaximum(10)
        self.ui.dial.setNotchesVisible(True)
        self.ui.dial.installEventFilter(self)

        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(10)

        self.ui.comboBox.addItems(["Dec", "Hex", "Bin", "Oct"])

        self.initSignals()

        self.loadData()

    def eventFilter(self, watched: QtCore.QObject, event) -> bool:

        if watched == self.ui.dial and event.type() == QtCore.QEvent.Type.KeyPress:

            if event.key() == QtCore.Qt.Key.Key_Plus or event.key() == QtCore.Qt.Key.Key_Equal:

                self.ui.dial.setValue(min(self.ui.dial.maximum(), self.ui.dial.value() + 1))

                return True

            elif event.key() == QtCore.Qt.Key.Key_Minus or event.key() == QtCore.Qt.Key.Key_Underscore:

                self.ui.dial.setValue((max(self.ui.dial.minimum(), self.ui.dial.value() - 1)))

                return True

        return super(Window, self).eventFilter(watched, event)

    def initSignals(self) -> None:

        self.ui.dial.valueChanged.connect(self.dialValueChanged)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderValueChanged)

        self.ui.comboBox.currentTextChanged.connect(self.changeComboBox)

    def loadData(self):

        self.ui.comboBox.setCurrentText(self.numbParameters.value("mode"))
        self.ui.lcdNumber.display(self.numbParameters.value("value"))
        self.ui.dial.setValue(self.numbParameters.value("value"))
        self.ui.horizontalSlider.setValue(self.numbParameters.value("value"))

    def dialValueChanged(self):

        self.ui.horizontalSlider.setValue(self.ui.dial.value())
        self.ui.lcdNumber.display(self.ui.dial.value())

    def sliderValueChanged(self):

        self.ui.dial.setValue(self.ui.horizontalSlider.value())
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())

    def changeComboBox(self):

        if self.ui.comboBox.currentText() == "Hex":

            self.ui.lcdNumber.setHexMode()

        elif self.ui.comboBox.currentText() == "Oct":

            self.ui.lcdNumber.setOctMode()

        elif self.ui.comboBox.currentText() == "Bin":

            self.ui.lcdNumber.setBinMode()

        elif self.ui.comboBox.currentText() == "Dec":

            self.ui.lcdNumber.setDecMode()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:

        self.numbParameters.setValue(
            "value", self.ui.lcdNumber.value()
        )
        self.numbParameters.setValue(
            "mode", self.ui.comboBox.currentText()
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
