import tkinter as tk
from tkinter import scrolledtext
import psutil
import wmi

class BatteryHealthTool:
    def __init__(self):
        self.wmi_interface = wmi.WMI(namespace="root\\WMI")
        self.app = tk.Tk()
        self.app.title("Battery Health Tool")
        self.app.geometry("750x500")

        self.output_field = scrolledtext.ScrolledText(self.app, wrap=tk.WORD, bg="black", fg="lime",
                                                      insertbackground='lime', font=("Consolas", 11))
        self.output_field.pack(expand=True, fill='both', padx=10, pady=10)

        button_frame = tk.Frame(self.app, bg="black")
        button_frame.pack(fill='x')

        tk.Button(button_frame, text="Check Battery Health", command=self.check_battery_health, width=20).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_screen, width=15).pack(side=tk.RIGHT, padx=5, pady=5)

    def run(self):
        self.app.mainloop()

    def append_info(self, text):
        self.output_field.insert(tk.END, text + "\n")
        self.output_field.see(tk.END)

    def clear_screen(self):
        self.output_field.delete(1.0, tk.END)

    def check_battery_health(self):
        self.append_info("🔍 Fetching battery info via WMI...\n")
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.append_info(f"Battery Percentage: {battery.percent}%")
                self.append_info(f"Plugged In: {'Yes' if battery.power_plugged else 'No'}")
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    mins, secs = divmod(battery.secsleft, 60)
                    hrs, mins = divmod(mins, 60)
                    self.append_info(f"Estimated Time Left: {hrs}h {mins}m\n")
                else:
                    self.append_info("Estimated Time Left: Charging or Unlimited\n")
            else:
                self.append_info("⚠️ Battery status not found.\n")

            static = self.wmi_interface.BatteryStaticData()[0]
            full = self.wmi_interface.BatteryFullChargedCapacity()[0].FullChargedCapacity
            status = self.wmi_interface.BatteryStatus()[0]

            design = static.DesignedCapacity
            health = (full / design) * 100 if design else 0

            self.append_info(f"Design Capacity: {design} mWh")
            self.append_info(f"Full Charge Capacity: {full} mWh")
            self.append_info(f"🔋 Health: {health:.2f}%\n")

            self.append_info(f"Voltage: {status.Voltage} mV")
            self.append_info(f"Discharge Rate: {status.DischargeRate} mW")
            self.append_info(f"Remaining Capacity: {status.RemainingCapacity} mWh")
        except Exception as e:
            self.append_info(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    BatteryHealthTool().run()
