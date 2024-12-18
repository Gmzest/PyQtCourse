"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
from PySide6 import QtGui, QtWidgets
from a_threads import SystemInfo


class Window1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CPU/RAM Monitor")

        self.delay_spinbox = QtWidgets.QSpinBox()
        self.delay_spinbox.setMinimum(100)
        self.delay_spinbox.setMaximum(10000)
        self.delay_spinbox.setRange(100, 10000)  # Диапазон задержки 0.1 - 10 сек
        self.delay_spinbox.setValue(1000)  # Задержка по умолчанию 1 секунда
        self.delay_spinbox.setSuffix(" мс")
        self.delay_spinbox.valueChanged.connect(self.update_delay)

        self.cpu_label = QtWidgets.QLabel("CPU: 0%")
        self.ram_label = QtWidgets.QLabel("RAM: 0%")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Задержка обновления:"))
        layout.addWidget(self.delay_spinbox)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        self.setLayout(layout)

        self.systemInfo = SystemInfo()
        self.systemInfo.systemInfoReceived.connect(self.update_labels)
        self.systemInfo.start()

    def update_delay(self, delay):
        if self.isValid():
            self.systemInfo.delay = delay

    def update_labels(self, sysInfo: list):
        self.cpu_label.setText(f"CPU: {sysInfo[0]:.1f}%")
        self.ram_label.setText(f"RAM: {sysInfo[1]:.1f}%")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.systemInfo.stop()
        self.systemInfo.wait()
        super().closeEvent(event)

    def isValid(self) -> bool:
        if self.delay_spinbox.value() < 100 or self.delay_spinbox.value() > 10000:
            return False
        else:
            return True


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window1()

    window.show()

    app.exec()
