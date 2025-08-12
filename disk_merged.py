from PyQt5 import QtWidgets
from Logic.disk_manager_gui import Ui_Form
import subprocess
import sys

class DiskManagerLogic:
    def __init__(self):
        self.script_file = "diskpart_script.txt"

    def run_diskpart(self, commands):
        with open(self.script_file, "w") as file:
            for cmd in commands:
                file.write(cmd + "\n")

        result = subprocess.run(f"diskpart /s {self.script_file}", shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        return output

    def prepare_list_disk_script(self):
        with open("list_disk_script.txt", "w") as file:
            file.write("list disk\nexit\n")

    def list_disks(self):
        self.prepare_list_disk_script()
        result = subprocess.run("diskpart /s list_disk_script.txt", shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        return output

    def repair_pendrive(self, disk_number):
        format_command = "format fs=ntfs quick"
        diskpart_commands = [
            f"select disk {disk_number}",
            "clean",
            "create partition primary",
            "select partition 1",
            "active",
            format_command,
            "assign",
            "exit"
        ]
        return self.run_diskpart(diskpart_commands)


class DiskManagerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.logic = DiskManagerLogic()

        # Change labels
        self.ui.label_2.setText("Disk Manager")
        self.ui.pushButton.setText("List Disks")
        self.ui.pushButton_2.setText("Repair Pendrive")
        self.ui.pushButton_3.setText("Clear All")

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.list_disks)
        self.ui.pushButton_2.clicked.connect(self.repair_pendrive)
        self.ui.pushButton_3.clicked.connect(self.clear_output)

    def append_output(self, text):
        self.ui.outputScreen.append(text)

    def clear_output(self):
        self.ui.outputScreen.clear()

    def list_disks(self):
        self.append_output("🔍 Listing available disks...\n")
        result = self.logic.list_disks()
        self.append_output(result)

    def repair_pendrive(self):
        from PyQt5.QtWidgets import QInputDialog
        disk_number, ok = QInputDialog.getInt(self, "Disk Number", "Enter the disk number of your pendrive (⚠️ double-check):")
        if ok:
            confirm, confirm_ok = QInputDialog.getText(self, "Confirm", f"Are you sure you want to clean and format Disk {disk_number}? Type 'yes' to confirm:")
            if confirm_ok and confirm.strip().lower() == 'yes':
                self.append_output(f"⚠️ Repairing disk {disk_number}...\n")
                result = self.logic.repair_pendrive(disk_number)
                self.append_output(result)
                self.append_output("✅ Pendrive repair process completed with NTFS file system.\n")
            else:
                self.append_output("❌ Operation cancelled by user.\n")
        else:
            self.append_output("❌ No disk number provided.\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DiskManagerApp()
    window.show()
    sys.exit(app.exec_())
