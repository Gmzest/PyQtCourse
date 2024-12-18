"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

from PySide6 import QtWidgets, QtCore, QtGui
from a_threads import WeatherHandler


class Window2(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.state = True

        self.initUi()

        self.initSignals()

    def initUi(self):
        self.setWindowTitle("Погода")

        self.latitude_input = QtWidgets.QLineEdit()
        self.latitude_input.setText("50")
        self.longitude_input = QtWidgets.QLineEdit()
        self.longitude_input.setText("50")
        self.delay_input = QtWidgets.QSpinBox()
        self.delay_input.setRange(1, 60)  # Задержка от 1 до 60 секунд
        self.delay_input.setValue(10)
        self.weather_output = QtWidgets.QLabel("")

        self.start_button = QtWidgets.QPushButton("Запустить")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Широта:"))
        layout.addWidget(self.latitude_input)
        layout.addWidget(QtWidgets.QLabel("Долгота:"))
        layout.addWidget(self.longitude_input)
        layout.addWidget(QtWidgets.QLabel("Задержка (сек):"))
        layout.addWidget(self.delay_input)
        layout.addWidget(self.weather_output)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def initSignals(self):

        self.start_button.clicked.connect(self.start_weather_handler)

    def start_weather_handler(self):
        if self.state:
            latitude = float(self.latitude_input.text())
            longitude = float(self.longitude_input.text())
            self.weather_handler = WeatherHandler(latitude, longitude)

            self.weather_handler.start()
            self.latitude_input.setEnabled(False)
            self.longitude_input.setEnabled(False)
            self.delay_input.setEnabled(False)
            self.state = False
            self.start_button.setText("Остановить")
            self.weather_handler.weatherInfo.connect(self.update_weather_output)
        else:
            self.weather_handler.stop()
            #self.weather_handler.wait()  # Ожидаем завершения потока
            self.state = True
            self.latitude_input.setEnabled(True)
            self.longitude_input.setEnabled(True)
            self.delay_input.setEnabled(True)
            self.start_button.setText("Запустить")
            self.weather_output.setText("")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.weather_handler.stop()
        self.weather_handler.wait()
        super().closeEvent(event)

    def update_weather_output(self, data):
        self.weather_output.setText(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window2()

    window.show()

    app.exec()
