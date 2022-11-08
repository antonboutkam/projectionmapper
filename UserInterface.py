from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import QSize, Qt
from UserInterfaceWindow import UserInterfaceWindow
import sys


class UserInterface:
    app = None
    window = None

    def start(self):
        self.app = QApplication(sys.argv)

        self.window = UserInterfaceWindow()
        self.window.show()

        self.app.exec()


if __name__ == "__main__":
    user_interface = UserInterface()
    print("start")
    user_interface.start()