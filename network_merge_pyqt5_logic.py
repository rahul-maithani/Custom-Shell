# network_pyqt.py
from PyQt5 import QtWidgets
from Logic.network_gui import Ui_MainWindow  # PyQt GUI
from Logic.backend import shellBackend  # Logic
import sys


class NetworkQtWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.backend = shellBackend()
        self.inputType = None

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.ask_ping)
        self.ui.pushButton_2.clicked.connect(self.tracert)
        self.ui.pushButton_3.clicked.connect(self.hostname)
        self.ui.pushButton_4.clicked.connect(self.ipconfig)
        self.ui.pushButton_5.clicked.connect(self.ask_curl)
        self.ui.pushButton_6.clicked.connect(self.ask_get_ip)
        self.ui.pushButton_7.clicked.connect(self.close)

    def ask_input(self, title, label, input_type):
        self.inputType = input_type
        text, ok = QtWidgets.QInputDialog.getText(self, title, label)
        if ok and text:
            self.process_input(text)

    def ask_ping(self):
        self.ask_input("Ping", "Enter the IP or URL to ping:", "ping")

    def ask_curl(self):
        self.ask_input("Curl", "Enter the URL to curl:", "curl")

    def ask_get_ip(self):
        self.ask_input("Get IP", "Enter the URL to get IP of:", "getIp")

    def process_input(self, inputRes):
        if self.inputType == "ping":
            result = self.backend.pingRun(inputRes)
        elif self.inputType == "getIp":
            result = self.backend.getIp(inputRes)
        elif self.inputType == "curl":
            result = self.backend.curl(inputRes).stdout
        else:
            result = "Unknown input type."
        QtWidgets.QMessageBox.information(self, "Result", result)

    def tracert(self):
        result = self.backend.tracertRun()
        QtWidgets.QMessageBox.information(self, "Tracert", result)

    def hostname(self):
        result = self.backend.hostRun()
        QtWidgets.QMessageBox.information(self, "Hostname", f"Hostname: {result}")

    def ipconfig(self):
        result = self.backend.ipconfig()
        QtWidgets.QMessageBox.information(self, "IP Config", result)


# To test standalone
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NetworkQtWindow()
    window.show()
    sys.exit(app.exec_())
