from PyQt5 import QtWidgets
from Logic.battery_gui import Ui_Form
import psutil
import wmi


class BatteryHealthLogic:
    def __init__(self):
        self.wmi_interface = wmi.WMI(namespace="root\\WMI")

    def get_battery_info(self):
        output = []
        output.append("🔍 Fetching battery info via WMI...\n")
        try:
            battery = psutil.sensors_battery()
            if battery:
                output.append(f"Battery Percentage: {battery.percent}%")
                output.append(f"Plugged In: {'Yes' if battery.power_plugged else 'No'}")
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    mins, secs = divmod(battery.secsleft, 60)
                    hrs, mins = divmod(mins, 60)
                    output.append(f"Estimated Time Left: {hrs}h {mins}m\n")
                else:
                    output.append("Estimated Time Left: Charging or Unlimited\n")
            else:
                output.append("⚠️ Battery status not found.\n")

            static = self.wmi_interface.BatteryStaticData()[0]
            full = self.wmi_interface.BatteryFullChargedCapacity()[0].FullChargedCapacity
            status = self.wmi_interface.BatteryStatus()[0]

            design = static.DesignedCapacity
            health = (full / design) * 100 if design else 0

            output.append(f"Design Capacity: {design} mWh")
            output.append(f"Full Charge Capacity: {full} mWh")
            output.append(f"🔋 Health: {health:.2f}%\n")

            output.append(f"Voltage: {status.Voltage} mV")
            output.append(f"Discharge Rate: {status.DischargeRate} mW")
            output.append(f"Remaining Capacity: {status.RemainingCapacity} mWh")
        except Exception as e:
            output.append(f"❌ Error: {str(e)}")
        return "\n".join(output)


class BatteryHealthApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.logic = BatteryHealthLogic()

        self.ui.label_2.setText("Battery Info")
        self.ui.pushButton.setText("Battery Health")
        self.ui.pushButton_2.setText("Clear")

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.display_battery_info)
        self.ui.pushButton_2.clicked.connect(self.clear_output)

    def display_battery_info(self):
        result = self.logic.get_battery_info()
        self.append_output(result)

    def clear_output(self):
        self.ui.outputScreen.clear()

    def append_output(self, text):
        self.ui.outputScreen.append(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = BatteryHealthApp()
    window.show()
    sys.exit(app.exec_())
