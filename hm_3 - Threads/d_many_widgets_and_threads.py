"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets, QtCore, QtGui
from b_systeminfo_widget import Window1
from c_weatherapi_widget import Window2


class BothApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()

        self.sys_info = Window1()
        self.weather_info = Window2()

        self.tabs.addTab(self.sys_info, "Система")
        self.tabs.addTab(self.weather_info, "Погода")

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.sys_info.systemInfo.stop()
        self.sys_info.systemInfo.wait()
        self.weather_info.weather_handler.stop()
        self.weather_info.weather_handler.wait()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    monitor = BothApp()
    monitor.show()

    app.exec()
