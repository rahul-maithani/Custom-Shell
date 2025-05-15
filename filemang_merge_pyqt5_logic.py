# fileman_pyqt.py
from PyQt5 import QtWidgets, QtGui
from Logic.filemang_gui import Ui_MainWindow  # Your PyQt5-designed GUI
from Logic.backend import shellBackend  # Logic from filemang.py
import sys


class FileManQtWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Backend logic
        self.backend = shellBackend()

        # Connect GUI buttons to methods
        self.ui.pushButton.clicked.connect(self.show_files)  # Show Files
        self.ui.pushButton_6.clicked.connect(self.show_directory)  # Show Directory
        self.ui.pushButton_2.clicked.connect(self.create_file)  # Create File
        self.ui.pushButton_3.clicked.connect(self.create_folder)  # Create Folder
        self.ui.pushButton_5.clicked.connect(self.delete_file)  # Delete File
        self.ui.pushButton_4.clicked.connect(self.delete_folder)  # Delete Folder
        self.ui.pushButton_7.clicked.connect(self.close)  # Exit

    def show_files(self):
        files = self.backend.getls()
        QtWidgets.QMessageBox.information(self, "Files", files)

    def show_directory(self):
        directory = self.backend.getCurrentPos().decode()
        QtWidgets.QMessageBox.information(self, "Current Directory", directory)

    def create_file(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Create File", "Enter file name:"
        )
        if ok and name:
            result = self.backend.createnewFile(name)
            msg = (
                "File created successfully."
                if result == 0
                else "Failed to create file."
            )
            QtWidgets.QMessageBox.information(self, "Create File", msg)

    def create_folder(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Create Folder", "Enter folder name:"
        )
        if ok and name:
            result = self.backend.createNewFolder(name)
            msg = (
                "Folder created successfully."
                if result == 0
                else "Failed to create folder."
            )
            QtWidgets.QMessageBox.information(self, "Create Folder", msg)

    def delete_file(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Delete File", "Enter file name:"
        )
        if ok and name:
            result = self.backend.deleteFile(name)
            msg = (
                "File deleted successfully."
                if result == 0
                else "Failed to delete file."
            )
            QtWidgets.QMessageBox.information(self, "Delete File", msg)

    def delete_folder(self):
        name, ok = QtWidgets.QInputDialog.getText(
            self, "Delete Folder", "Enter folder name:"
        )
        if ok and name:
            result = self.backend.deleteFolder(name)
            msg = (
                "Folder deleted successfully."
                if result == 0
                else "Failed to delete folder."
            )
            QtWidgets.QMessageBox.information(self, "Delete Folder", msg)


# To run standalone for testing
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FileManQtWindow()
    window.show()
    sys.exit(app.exec_())
