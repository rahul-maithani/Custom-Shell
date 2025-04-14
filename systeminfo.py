import tkinter as tk
from tkinter import scrolledtext
import platform
import psutil
import os
from cpuinfo import get_cpu_info
from ssd_checker import is_ssd

try:
    import GPUtil
except ImportError:
    GPUtil = None

class SystemInfo:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("System Info Tool - CMD Style")
        self.app.geometry("750x500")

        self.output_field = scrolledtext.ScrolledText(self.app, wrap=tk.WORD, bg="black", fg="lime",
                                                      insertbackground='lime', font=("Consolas", 11))
        self.output_field.pack(expand=True, fill='both', padx=10, pady=10)

        button_frame = tk.Frame(self.app, bg="black")
        button_frame.pack(fill='x')

        tk.Button(button_frame, text="System Info", command=self.show_system_info, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Disk Info", command=self.show_disk_info, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="RAM Info", command=self.show_ram_info, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="GPU Info", command=self.show_gpu_info, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_screen, width=15).pack(side=tk.RIGHT, padx=5, pady=5)

    def run(self):
        self.app.mainloop()

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor

    def append_info(self, text):
        self.output_field.insert(tk.END, text + "\n")
        self.output_field.see(tk.END)  # Auto-scroll

    def clear_screen(self):
        self.output_field.delete(1.0, tk.END)

    def get_cpu_name(self):
        try:
            info = get_cpu_info()
            return info.get('brand_raw', 'Unknown CPU')
        except Exception as e:
            return f"Error retrieving CPU info: {e}"

    def detect_disks(self):
        disk_report = ""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            device = partition.device
            try:
                disk_type = "SSD" if is_ssd(device) else "HDD"
            except Exception:
                disk_type = "Unknown"
            disk_report += f"Device: {device} - Type: {disk_type}\n"
        return disk_report

    def show_system_info(self):
        uname = platform.uname()
        cpu_name = self.get_cpu_name()
        info = (
            f"System: {uname.system}\n"
            f"Node Name: {uname.node}\n"
            f"Release: {uname.release}\n"
            f"Version: {uname.version}\n"
            f"Machine: {uname.machine}\n"
            f"Processor: {cpu_name}\n"
            f"{'-'*40}"
        )
        self.append_info(info)

    def show_disk_info(self):
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

        info += "Detected Disk Types:\n"
        info += self.detect_disks()
        info += f"\n{'-'*40}"
        self.append_info(info)

    def show_ram_info(self):
        svmem = psutil.virtual_memory()
        info = (
            f"RAM Information:\n"
            f"Total: {self.get_size(svmem.total)}\n"
            f"Available: {self.get_size(svmem.available)}\n"
            f"Used: {self.get_size(svmem.used)}\n"
            f"Percentage: {svmem.percent}%\n"
            f"{'-'*40}"
        )
        self.append_info(info)

    def show_gpu_info(self):
        if GPUtil is None:
            self.append_info("GPU Info: GPUtil not installed or no compatible GPU found.\n" + '-'*40)
            return

        gpus = GPUtil.getGPUs()
        if not gpus:
            self.append_info("GPU Info: No GPU Found.\n" + '-'*40)
            return

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
        self.append_info(info)


