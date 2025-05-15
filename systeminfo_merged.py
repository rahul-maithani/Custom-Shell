from PyQt5 import QtWidgets
from Logic.system_info_ui import Ui_Form
import platform
import psutil
from cpuinfo import get_cpu_info

try:
    import GPUtil
except ImportError:
    GPUtil = None


class SystemInfoLogic:
    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor

    def get_cpu_name(self):
        try:
            info = get_cpu_info()
            return info.get("brand_raw", "Unknown CPU")
        except Exception as e:
            return f"Error retrieving CPU info: {e}"

    def get_system_info(self):
        uname = platform.uname()
        cpu_name = self.get_cpu_name()
        return (
            f"System: {uname.system}\n"
            f"Node Name: {uname.node}\n"
            f"Release: {uname.release}\n"
            f"Version: {uname.version}\n"
            f"Machine: {uname.machine}\n"
            f"Processor: {cpu_name}\n"
            f"{'-'*40}"
        )

    def get_disk_info(self):
        info = "Disk Information:\n"
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info += (
                    f"Device: {partition.device}\n"
                    f"  Mountpoint: {partition.mountpoint}\n"
                    f"  File System: {partition.fstype}\n"
                    f"  Total: {self.get_size(usage.total)}\n"
                    f"  Used: {self.get_size(usage.used)}\n"
                    f"  Free: {self.get_size(usage.free)}\n"
                    f"  Usage: {usage.percent}%\n\n"
                )
            except PermissionError:
                continue
        info += f"\n{'-'*40}"
        return info

    def get_ram_info(self):
        svmem = psutil.virtual_memory()
        return (
            f"RAM Information:\n"
            f"Total: {self.get_size(svmem.total)}\n"
            f"Available: {self.get_size(svmem.available)}\n"
            f"Used: {self.get_size(svmem.used)}\n"
            f"Percentage: {svmem.percent}%\n"
            f"{'-'*40}"
        )

    def get_gpu_info(self):
        if GPUtil is None:
            return (
                "GPU Info: GPUtil not installed or no compatible GPU found.\n"
                + "-" * 40
            )

        gpus = GPUtil.getGPUs()
        if not gpus:
            return "GPU Info: No GPU Found.\n" + "-" * 40

        info = "GPU Information:\n"
        for gpu in gpus:
            info += (
                f"Name: {gpu.name}\n"
                f"Total Memory: {self.get_size(gpu.memoryTotal * 1024 * 1024)}\n"
                f"Temperature: {gpu.temperature} °C\n"
                f"Driver: {gpu.driver}\n"
                f"Load: {gpu.load * 100:.1f}%\n\n"
            )
        info += f"{'-'*40}"
        return info


class SystemInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.logic = SystemInfoLogic()

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.display_system_info)
        self.ui.pushButton_2.clicked.connect(self.display_disk_info)
        self.ui.pushButton_3.clicked.connect(self.display_ram_info)
        self.ui.pushButton_4.clicked.connect(self.display_gpu_info)
        self.ui.pushButton_5.clicked.connect(self.clear_output)

    def display_system_info(self):
        self.append_output(self.logic.get_system_info())

    def display_disk_info(self):
        self.append_output(self.logic.get_disk_info())

    def display_ram_info(self):
        self.append_output(self.logic.get_ram_info())

    def display_gpu_info(self):
        self.append_output(self.logic.get_gpu_info())

    def clear_output(self):
        self.ui.outputScreen.clear()

    def append_output(self, text):
        self.ui.outputScreen.append(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SystemInfoApp()
    window.show()
    sys.exit(app.exec_())
