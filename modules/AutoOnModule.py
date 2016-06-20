from modules.BaseModule import BaseModule
import subprocess
import time

class AutoOnModule(BaseModule):
    """Automatically turns off the display on a Raspberry Pi"""
    def __init__(self):
        super(AutoOnModule, self).__init__()
        # Returns the current display power status (0=off, 1=on):
        self.current_status = get_display_status()
        self.updatedelay = 60

    def update(self):
        hour = time.localtime()[3]
        if self.current_status == 0 and hour == 7:
            subprocess.call(["vcgencmd", "display_power", "1"])
            self.current_status = get_display_status()
        if self.current_status == 1 and hour == 21:
            subprocess.call(["vcgencmd", "display_power", "0"])
            self.current_status = get_display_status()
        return []

    def exit(self):
        subprocess.call(["vcgencmd", "display_power", "1"])


def get_display_status():
    return int(subprocess.check_output(["vcgencmd", "display_power"]).decode("UTF-8")[-2])
