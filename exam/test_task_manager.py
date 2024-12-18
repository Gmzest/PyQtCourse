from PySide6 import QtWidgets
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                               QGridLayout, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout)
from PySide6.QtCore import Qt, QTimer
import psutil
import platform

"""
На данный момент приложение реализовано под Mac OS/Linux
Из-за отсутствия общей библиотеки для вывода служб
в операционной системе.

Ниже представлено условие под импорт иной библиотеки,
и закомментированный код реализации под Windows.



"""
if platform.system() == "Windows":
    import win32service

import subprocess


class ServiceMonitor_MacOS(QWidget):

    def __init__(self):
        super().__init__()

        self.service_table = QTableWidget()
        self.service_table.setSortingEnabled(True)
        self.service_table.setColumnCount(3)
        headers = ["Name", "PID", "Status"]
        self.service_table.setHorizontalHeaderLabels(headers)

        # Устанавливаем размер таблицы под содержимое
        # self.service_table.resizeColumnsToContents()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.service_table)

        self.setLayout(self.layout)

    def update_service_table(self):
        result = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
        services = result.stdout.split("\n")[1:]

        for i, service in enumerate(services[:-1]):
            label, pid_status, name = service.split("\t")
            item_name = QTableWidgetItem(name)
            item_label = QTableWidgetItem(label)
            item_pid_status = QTableWidgetItem(pid_status)

            self.service_table.insertRow(i)
            self.service_table.setItem(i, 0, item_name)
            self.service_table.setItem(i, 1, item_label)
            self.service_table.setItem(i, 2, item_pid_status)


class DiskMonitor(QWidget):

    def __init__(self):
        super().__init__()

        self.labels = []
        self.layout = QVBoxLayout()

        for i, disk in enumerate(psutil.disk_partitions()):
            disk_usage = psutil.disk_usage(disk.mountpoint)
            disk_label = QLabel(f"Диск{i + 1}: {disk.device} // {disk_usage.percent}%")
            self.labels.append(disk_label)
            self.layout.addWidget(disk_label)

        self.setLayout(self.layout)

    def disk_update(self):
        for i, disk in enumerate(psutil.disk_partitions()):
            disk_usage = psutil.disk_usage(disk.mountpoint)
            self.labels[i].setText(f"Диск{i + 1}: {disk.device} // {disk_usage.percent}%")


class SystemMonitor(QWidget):

    def __init__(self):
        super().__init__()

        self.status_sort = False

        self.initUi()
        self.initSignals()

    def initUi(self):

        # Таблица процессов
        self.process_table = QTableWidget()
        self.process_table.setSortingEnabled(True)
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU%", "Mem%"])
        self.process_table.horizontalHeader().setStretchLastSection(True)

        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.process_table)

        self.setLayout(main_layout)

    def initSignals(self):
        ...
        # self.process_table.horizontalHeader().sectionClicked.connect(self.sort_column)

    def update_process_table(self):
        self.process_table.setRowCount(0)
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        self.process_table.setRowCount(len(processes))
        for i, p in enumerate(processes):
            self.process_table.setItem(i, 0, QTableWidgetItem(str(p['pid'])))
            self.process_table.setItem(i, 1, QTableWidgetItem(p['name']))
            if p['cpu_percent'] is not None:
                self.process_table.setItem(i, 2, QTableWidgetItem(f"{p['cpu_percent']:.2f}%"))
            if p['memory_percent'] is not None:
                self.process_table.setItem(i, 3, QTableWidgetItem(f"{p['memory_percent']:.1f}%"))

    def sort_column(self, column):
        if not self.status_sort:
            self.process_table.sortItems(column, Qt.SortOrder.AscendingOrder)
            self.status_sort = True
        else:
            self.process_table.sortItems(column, Qt.SortOrder.DescendingOrder)
            self.status_sort = False


class SystemInfo(QWidget):

    def __init__(self):
        super().__init__()

        self.initUi()
        self.initSignals()

    def initUi(self):
        # Общая информация о системе
        self.platform_label = QLabel()
        self.cpu_label = QLabel()
        self.mem_label = QLabel()

        self.system_info_layout = QVBoxLayout()

        self.system_info_layout.addWidget(self.platform_label)
        self.system_info_layout.addWidget(self.cpu_label)
        self.system_info_layout.addWidget(self.mem_label)

        self.update_interval_combo = QComboBox()
        self.update_interval_combo.addItems(["1 сек", "5 сек", "10 сек", "30 сек"])
        self.update_interval = 1000  # 1 секунда по умолчанию

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.system_info_layout)
        main_layout.addWidget(self.update_interval_combo)

        self.setLayout(main_layout)

        # Запуск таймера обновления

    def initSignals(self):
        ...

    def update_system_info(self):
        platform_info = f"Опреационная система: {platform.system()}"
        cpu_info = f"Процессор: {platform.processor()} ({psutil.cpu_count(logical=True)} ядер), Загрузка: {psutil.cpu_percent()}%"
        mem_info = f"ОЗУ: {psutil.virtual_memory().total >> 20} MB, Использовано: {psutil.virtual_memory().percent}%"

        self.platform_label.setText(platform_info)
        self.cpu_label.setText(cpu_info)
        self.mem_label.setText(mem_info)


class TaskManager(QWidget):

    def __init__(self):
        super().__init__()

        self.initUi()
        self.initSignals()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.timeout.connect(self.disk_info.disk_update)
        self.timer.timeout.connect(self.service_info.update_service_table)
        self.timer.start(self.sys_info.update_interval)

    def update_data(self):
        self.sys_info.update_system_info()
        self.proc_table.update_process_table()

    def change_update_interval(self, index):
        intervals = [1000, 5000, 10000, 30000]
        self.sys_info.update_interval = intervals[index]
        self.timer.setInterval(self.sys_info.update_interval)

    def initUi(self):
        self.setWindowTitle("Диспетчер задач")

        self.sys_info = SystemInfo()
        self.proc_table = SystemMonitor()
        self.disk_info = DiskMonitor()
        self.service_info = ServiceMonitor_MacOS()

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self.proc_table, "Процессы")
        self.tabs.addTab(self.disk_info, "Диски")
        self.tabs.addTab(self.service_info, "Службы")

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sys_info)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def initSignals(self):
        self.sys_info.update_interval_combo.currentIndexChanged.connect(self.change_update_interval)


if __name__ == "__main__":
    app = QApplication()

    monitor = TaskManager()
    monitor.show()

    app.exec()
