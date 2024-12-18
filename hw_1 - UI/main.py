from PySide6 import QtWidgets

# from b_login import Ui_MainWindow
# from c_ship_parameters import Ui_MainWindow
# from d_engine_settings import Ui_MainWindow
from e_profile_card import Ui_MainWindow


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":

    app = QtWidgets.QApplication()

    window = Window()
    window.show()


    app.exec()

