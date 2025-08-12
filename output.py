from PyQt5 import QtCore, QtGui, QtWidgets

from network_merge_pyqt5_logic import NetworkQtWindow
from systeminfo_merged import SystemInfoApp
from filemang_merge_pyqt5_logic import FileManQtWindow
from battery_merged import BatteryHealthApp
from disk_merged import DiskManagerApp

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller and during development) """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class Ui_MainWindow(object):
    def show_loading(self):
        self.loading_dialog = QtWidgets.QDialog()
        self.loading_dialog.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup
        )
        self.loading_dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.loading_dialog.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.loading_dialog.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)
        self.loading_dialog.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.loading_dialog.setFixedSize(80, 80)

        spinner = QtWidgets.QLabel(self.loading_dialog)
        spinner.setStyleSheet("background-color: rgba(0,0,0,0);")
        movie = QtGui.QMovie(resource_path("media/spinner.gif"))

        movie.setScaledSize(QtCore.QSize(150, 150))
        spinner.setMovie(movie)
        spinner.setAlignment(QtCore.Qt.AlignCenter)
        movie.start()

        layout = QtWidgets.QVBoxLayout(self.loading_dialog)
        layout.addWidget(spinner)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        center = self.centralwidget.geometry().center()
        dlg_size = self.loading_dialog.size()
        self.loading_dialog.move(
            self.centralwidget.mapToGlobal(
                QtCore.QPoint(
                    center.x() - dlg_size.width() // 2,
                    center.y() - dlg_size.height() // 2,
                )
            )
        )
        self.loading_dialog.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1100, 849)
        MainWindow.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 0, 1061, 791))
        self.label.setMovie(QtGui.QMovie(resource_path("media/animated2.gif")))

        self.label.movie().start()
        self.label.setScaledContents(True)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 120, 301, 51))
        self.label_2.setStyleSheet('font: 75 26pt "MS Shell Dlg 2"; color: white;')

        def make_button(y, color, hover_color, text, icon_path, icon_size):
            btn = QtWidgets.QPushButton(self.centralwidget)
            btn.setGeometry(QtCore.QRect(428, y, 280, 60))
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font: bold 20px;
                    border-radius: 10px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
            """
            )
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(resource_path(icon_path)), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            btn.setIcon(icon)
            btn.setIconSize(QtCore.QSize(*icon_size))
            btn.setText(f"    {text}")
            return btn

        self.pushButton = make_button(
            200, "#670D2F", "#A53860", "File Management", "./media/FILE.jpeg", (40, 40)
        )
        self.pushButton_2 = make_button(
            290, "#344C64", "#57A6A1", "Network", "./media/network.png", (60, 60)
        )
        self.pushButton_3 = make_button(
            380, "#1D267D", "#5C469C", "System Info", "./media/SINFO.jpeg", (40, 40)
        )
        self.pushButton_4 = make_button(
            470, "#008080", "#4FBDBA", "Battery Info", "./media/BATTERY.jpeg", (40, 40)
        )
        self.pushButton_5 = make_button(
            560, "#78023B", "#A44770", "Disk Cleanup", "./media/disk.jpeg", (40, 40)
        )

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(QtWidgets.QMenuBar(MainWindow))
        MainWindow.setStatusBar(QtWidgets.QStatusBar(MainWindow))

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.open_file_management)
        self.pushButton_2.clicked.connect(self.open_network)
        self.pushButton_3.clicked.connect(self.open_system_info)
        self.pushButton_4.clicked.connect(self.open_battery_info)
        self.pushButton_5.clicked.connect(self.open_disk_info)

    def retranslateUi(self, MainWindow):
        _t = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_t("MainWindow", "MainWindow"))
        self.label_2.setText(_t("MainWindow", "Custom Shell"))

    def open_file_management(self):
        self.show_loading()
        QtCore.QTimer.singleShot(1000, self._launch_file_management)

    def _launch_file_management(self):
        self.file_window = FileManQtWindow()
        self.file_window.show()
        self.loading_dialog.close()

    def open_network(self):
        self.show_loading()
        QtCore.QTimer.singleShot(1000, self._launch_network)

    def _launch_network(self):
        self.file_window = NetworkQtWindow()
        self.file_window.show()
        self.loading_dialog.close()

    def open_system_info(self):
        self.show_loading()
        QtCore.QTimer.singleShot(1000, self._launch_system_info)

    def _launch_system_info(self):
        self.file_window = SystemInfoApp()
        self.file_window.show()
        self.loading_dialog.close()
        
    def open_battery_info(self):
        self.show_loading()
        QtCore.QTimer.singleShot(1000, self._launch_battery_info)

    def _launch_battery_info(self):
        self.file_window = BatteryHealthApp()
        self.file_window.show()
        self.loading_dialog.close()
        
    def open_disk_info(self):
        self.show_loading()
        QtCore.QTimer.singleShot(1000, self._launch_disk_info)

    def _launch_disk_info(self):
        self.file_window = DiskManagerApp()
        self.file_window.show()
        self.loading_dialog.close()



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())