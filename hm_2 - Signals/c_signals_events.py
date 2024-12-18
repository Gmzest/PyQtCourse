"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

from PySide6 import QtWidgets
from PySide6 import QtGui, QtCore
from c_signals_events_form import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initSignals()

    def initSignals(self) -> None:

        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoords)
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetData)

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:

        print(f"X:{event.oldPos().x()}, Y:{event.oldPos().y()}")
        print(f"X:{event.pos().x()}, Y:{event.pos().y()}")

    def resizeEvent(self, event: QtCore.QEvent) -> None:

        print(f"{self.size().width()}x{self.size().height()}")

    def onPushButtonMoveCoords(self) -> None:

        self.move(int(self.ui.spinBoxX.text()), int(self.ui.spinBoxY.text()))

    def onPushButtonGetData(self) -> None:

        list_of_logs = [
            f"Количество экранов: {QtWidgets.QApplication.screens().__len__()}",
            f"Текущее основное окно: {QtWidgets.QApplication.activeWindow().objectName()}",
            f"Разрешение экрана: {QtWidgets.QApplication.primaryScreen().geometry().width()}x{QtWidgets.QApplication.primaryScreen().geometry().height()}",
            f"Окно находится на экране номер: {QtWidgets.QApplication.screens().index(self.screen()) + 1}",
            f"Размеры окна: {self.size().width()}x{self.size().height()}",
            f"Минимальные размеры окна: {self.minimumSize().width()}x{self.minimumSize().height()}",
            f"Координаты окна X:{self.pos().x()}, Y:{self.pos().y()}",
            f"Координаты центра окна X:{self.geometry().center().x()}, Y:{self.geometry().center().y()}"
        ]

        if self.windowState().name == "WindowNoState":
            list_of_logs.append("Состояние окна: Нормальное")
        elif self.windowState().name == "WindowMinimized":
            list_of_logs.append("Состояние окна: Свернуто")
        elif self.windowState().name == "WindowMaximized":
            list_of_logs.append("Состояние окна: Развернуто")
        elif self.windowState().name == "WindowFullScreen":
            list_of_logs.append("Состояние окна: На весь экран")

        self.ui.plainTextEdit.setPlainText("\n".join(list_of_logs))


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()

    window.show()

    app.exec()
