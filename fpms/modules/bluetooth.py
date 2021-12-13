import time
import os.path
import subprocess
import fpms.modules.wlanpi_oled as oled
import sys
import re

from fpms.modules.pages.simpletable import SimpleTable
from fpms.modules.pages.pagedtable import PagedTable
from fpms.modules.pages.alert import Alert

from fpms.modules.constants import MAX_TABLE_LINES

class Bluetooth(object):

    def __init__(self, g_vars):

        # create paged table
        self.paged_table_obj = PagedTable(g_vars)

        # create alert
        self.alert_obj = Alert(g_vars)

    def bluetooth_present(self):
        try:
            cmd = "systemctl is-active --quiet bluetooth"
            subprocess.check_output(cmd, shell=True)
            try:
                cmd = "bt-adapter -l"
                subprocess.check_output(cmd, shell=True)
                return True
            except subprocess.CalledProcessError as exc:
                return False
        except subprocess.CalledProcessError as exc:
            return False

    def bluetooth_name(self):
        try:
            cmd = "bt-adapter -i | grep Name | awk '{ print $2 }'"
            name = subprocess.check_output(cmd, shell=True).decode().strip()
            return name
        except subprocess.CalledProcessError as exc:
            return None

    def bluetooth_alias(self):
        try:
            cmd = "bt-adapter -i | grep Alias | awk '{ print $2 }'"
            alias = subprocess.check_output(cmd, shell=True).decode().strip()
            return alias
        except subprocess.CalledProcessError as exc:
            return None

    def bluetooth_address(self):
        try:
            cmd = "bt-adapter -i | grep Address | awk '{ print $2 }'"
            address = subprocess.check_output(cmd, shell=True).decode().strip()
            return address
        except subprocess.CalledProcessError as exc:
            return None

    def bluetooth_power(self):
        try:
            cmd = "bt-adapter -i | grep Powered | awk '{ print $2 }'"
            power = subprocess.check_output(cmd, shell=True).decode().strip()
            if power == "1":
                return True
            else:
                return False
        except subprocess.CalledProcessError as exc:
            return False

    def bluetooth_set_power(self, power):
        bluetooth_is_on = self.bluetooth_power()

        try:
            if power:
                if bluetooth_is_on:
                    return True
                cmd = "bt-adapter --set Powered 1 && echo 1 > /etc/wlanpi-bluetooth/state"
            else:
                if not bluetooth_is_on:
                    return True
                cmd = "bt-adapter --set Powered 0 && echo 0 > /etc/wlanpi-bluetooth/state"
            subprocess.run(cmd, shell=True)
            return True
        except subprocess.CalledProcessError as exc:
            return False

    def bluetooth_paired_devices(self):
        '''
        Returns a dictionary of paired devices, indexed by MAC address
        '''

        if not self.bluetooth_present():
            return None

        try:
            cmd = "bluetoothctl -- paired-devices"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            if len(output) > 0:
                output = re.sub("Device *", "", output).split('\n')
                return dict([line.split(" ", 1) for line in output])
            else:
                return None
        except subprocess.CalledProcessError as exc:
            return None

    def bluetooth_status(self, g_vars):
        status = []

        if not self.bluetooth_present():
            self.alert_obj.display_alert_error(g_vars, "Bluetooth adapter not found.")
            g_vars['display_state'] = 'page'
            return

        status.append("Name:"  + self.bluetooth_name())
        status.append("Alias:" + self.bluetooth_alias())
        status.append("Addr:"  + self.bluetooth_address().replace(":", ""))

        if self.bluetooth_power():
            status.append("Power:On")
        else:
            status.append("Power:Off")

        paired_devices = self.bluetooth_paired_devices()

        if paired_devices != None:
            status.append("---")
            status.append("PAIRED DEVICES")
            status.append("---")
            for mac in paired_devices:
                status.append("Name:" + paired_devices[mac])
                status.append("Addr:" + mac.replace(":", ""))

        self.paged_table_obj.display_list_as_paged_table(g_vars, status, title="Status")

        g_vars['display_state'] = 'page'

    def bluetooth_pair(self, g_vars):

        if not self.bluetooth_present():
            self.alert_obj.display_alert_error(g_vars, "Bluetooth adapter not found.")
            g_vars['display_state'] = 'page'
            return

        ok = False
        alert_msg = None
        if self.bluetooth_set_power(True):
            if not g_vars['result_cache']:
                # Unpair existing paired devices
                self.alert_obj.display_popup_alert(g_vars, "Entering pairing mode...")
                paired_devices = self.bluetooth_paired_devices()
                if paired_devices != None:
                    self.alert_obj.display_popup_alert(g_vars, "Unpairing existing device...")
                    for dev in paired_devices:
                        try:
                            cmd = f"bluetoothctl -- remove {dev}"
                            subprocess.run(cmd, shell=True)
                        except:
                            pass
            else:
                paired_devices = self.bluetooth_paired_devices()
                if paired_devices != None:
                    for dev in paired_devices:
                        alert_msg = f"Paired to {paired_devices[dev]}"
                        ok = True
                        break
                else:
                    alias = self.bluetooth_alias()
                    try:
                        cmd = "systemctl start bt-timedpair"
                        subprocess.run(cmd, shell=True).check_returncode()
                        alert_msg = "Bluetooth is on. Discoverable as \"" + alias + "\""
                        ok = True
                    except subprocess.CalledProcessError as exc:
                        alert_msg = "Failed to set as discoverable."
        else:
            alert_msg = "Failed to turn on bluetooth."

        if alert_msg != None:
            if ok:
                self.alert_obj.display_alert_info(g_vars, alert_msg, title="Success")
            else:
                self.alert_obj.display_alert_error(g_vars, alert_msg)

        g_vars['result_cache'] = True
        g_vars['display_state'] = 'page'

    def bluetooth_on(self, g_vars):

        if not self.bluetooth_present():
            self.alert_obj.display_alert_error(g_vars, "Bluetooth adapter not found.")
            g_vars['display_state'] = 'page'
            return

        ok = False
        if self.bluetooth_set_power(True):
            alert_msg = "Bluetooth is on."
            ok = True
        else:
            alert_msg = "Failed to turn on bluetooth."

        if ok:
            self.alert_obj.display_alert_info(g_vars, alert_msg, title="Success")
        else:
            self.alert_obj.display_alert_error(g_vars, alert_msg)

        g_vars['display_state'] = 'page'

    def bluetooth_off(self, g_vars):

        if not self.bluetooth_present():
            self.alert_obj.display_alert_error(g_vars, "Bluetooth adapter not found.")
            g_vars['display_state'] = 'page'
            return

        ok = False
        if self.bluetooth_set_power(False):
            alert_msg = "Bluetooth is off."
            ok = True
        else:
            alert_msg = "Failed to turn off bluetooth."

        if ok:
            self.alert_obj.display_alert_info(g_vars, alert_msg, title="Success")
        else:
            self.alert_obj.display_alert_error(g_vars, alert_msg)

        g_vars['display_state'] = 'page'
