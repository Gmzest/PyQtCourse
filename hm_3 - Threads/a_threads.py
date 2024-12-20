"""
Модуль в котором содержаться потоки Qt
"""
import requests
import time

import psutil
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)

    # TODO Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # TODO создайте атрибут класса self.delay = None, для управлением задержкой получения данных
        self.running = True

    def run(self) -> None:  # TODO переопределить метод run
        if self.delay is None:  # TODO Если задержка не передана в поток перед его запуском
            self.delay = 3  # TODO то устанавливайте значение 1

        while True:  # TODO Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # TODO с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # TODO с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value,
                                          ram_value])  # TODO с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(
                self.delay / 1000)  # TODO с помощью функции .sleep() приостановите выполнение цикла на время self.delay
            if not self.running:
                break

    def stop(self):
        self.running = False


class WeatherHandler(QtCore.QThread):
    # TODO Пропишите сигналы, которые считаете нужными

    weatherInfo = QtCore.Signal(str)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.lat = lat
        self.lon = lon
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=true"
        self.__delay = 5
        self.__status = True


        self.running = True

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay

    def run(self) -> None:
        # TODO настройте метод для корректной работы

        while self.__status:
            # TODO Примерный код ниже

            response = requests.get(self.__api_url)
            data = response.json()
            self.weatherInfo.emit(str(data['current_weather']['temperature']))
            time.sleep(self.__delay)

            if not self.running:
                break

    def stop(self):
        self.running = False
