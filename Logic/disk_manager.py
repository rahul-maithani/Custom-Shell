import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
import subprocess

class DiskManager:
    def __init__(self):
        self.script_file = "diskpart_script.txt"
        self.app = tk.Tk()
        self.app.title("Disk Manager Tool")
        self.app.geometry("750x500")

        # Output area to show the commands and results
        self.output_field = scrolledtext.ScrolledText(self.app, wrap=tk.WORD, bg="black", fg="lime",
                                                      insertbackground='lime', font=("Consolas", 11))
        self.output_field.pack(expand=True, fill='both', padx=10, pady=10)

        button_frame = tk.Frame(self.app, bg="black")
        button_frame.pack(fill='x')

        tk.Button(button_frame, text="List Disks", command=self.list_disks, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Repair Pendrive", command=self.repair_pendrive_gui, width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_screen, width=15).pack(side=tk.RIGHT, padx=5, pady=5)

    def run(self):
        self.app.mainloop()

    def append_info(self, text):
        """Add output to the text field."""
        self.output_field.insert(tk.END, text + "\n")
        self.output_field.see(tk.END)  # Auto-scroll

    def clear_screen(self):
        """Clear the text field."""
        self.output_field.delete(1.0, tk.END)

    def run_diskpart(self, commands):
        """Run DiskPart commands from a list and capture output."""
        with open(self.script_file, "w") as file:
            for cmd in commands:
                file.write(cmd + "\n")
        
        self.append_info("Running diskpart commands...\n")
        
        # Run diskpart and capture the output
        result = subprocess.run(f"diskpart /s {self.script_file}", shell=True, capture_output=True, text=True)

        # Display the output in the text field
        self.append_info(result.stdout)
        if result.stderr:
            self.append_info(f"Error: {result.stderr}")

    def prepare_list_disk_script(self):
        """Prepare the script for listing disks."""
        with open("list_disk_script.txt", "w") as file:
            file.write("list disk\nexit\n")

    def list_disks(self):
        """List all available disks using DiskPart."""
        self.prepare_list_disk_script()
        self.append_info("Listing available disks...\n")
        result = subprocess.run("diskpart /s list_disk_script.txt", shell=True, capture_output=True, text=True)
        self.append_info(result.stdout)
        if result.stderr:
            self.append_info(f"Error: {result.stderr}")

    def repair_pendrive(self, disk_number):
        """Repair and format the selected pendrive with NTFS file system."""
        # Always format as NTFS
        format_command = "format fs=ntfs quick"

        # DiskPart commands for repair
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
        self.run_diskpart(diskpart_commands)
        self.append_info("✅ Pendrive repair process completed with NTFS file system.\n")

    def repair_pendrive_gui(self):
        """Show a GUI to select disk number for repair and perform the operation."""
        # Raise the main window to the front
        self.app.lift()

        # Ask for disk number using simpledialog
        disk_number = simpledialog.askinteger("Disk Number", "Enter the disk number of your pendrive (⚠️ Make sure it is correct):")
        if disk_number is None:
            self.append_info("Operation cancelled. No disk number provided.\n")
            return
        
        # Confirm if the user wants to continue
        confirm = simpledialog.askstring("Confirm", f"Are you sure you want to clean and format Disk {disk_number}? (yes/no):").strip().lower()
        if confirm != 'yes' or ' ':
            self.append_info("Operation cancelled.\n")
            return
        
        # Proceed with the repair (always NTFS)
        self.repair_pendrive(disk_number)

if __name__ == "__main__":
    app = DiskManager()
    app.run()

