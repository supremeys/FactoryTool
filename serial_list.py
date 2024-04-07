#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project:Factory_test
@File:serial_list.py
@Author:rivern.yuan
@Date:2022/9/6 15:59
"""

import time
import threading
import serial.tools.list_ports
from pubsub import pub


class SerialDetection(threading.Thread):
    """
    class for detection port list
    """
    def __init__(self):
        super(SerialDetection, self).__init__()
        self.serPort = serial.tools.list_ports
        self._exit = False

    def exit_event(self):
        self._exit = True

    def enter_event(self):
        self._exit = False

    def get_com_number(self):
        port_list = []
        repl_port = [("0x2C7C:0x0901", "x.8"),      # Unisoc
                     ("0x2C7C:0x6001", "x.5"),      # N 系列
                     ("0x2C7C:0x6002", "x.5"),      # M 系列
                     ("0x2C7C:0x6005", "x.5"),      # A 系列
                     ("0x2C7C:0x0700", "x.1"),      # BG95
                     ("0x2C7C:0x0903", "x.5"),      # Eigen
                     ("0x2C7C:0x6002", "x.20")]     # M 系列 新驱动
        for p in list(self.serPort.comports()):
            print(p.description)
            for vid_pid, location in repl_port:
                location_ = p.location if p.location is not None else ""
                if (p.vid == int(vid_pid.split(":")[0], 16) and p.pid == int(vid_pid.split(":")[1], 16) and location in location_) or "Quectel USB REPL Port" in p.description:
                    port_list.append(p.device)
                    break

        return port_list

    def run(self):
        serial_list = []
        while True:
            if self._exit:
                pass
            else:
                if serial_list == [] or serial_list != self.serPort.comports():
                    serial_list = self.serPort.comports()
                    serial_port = self.get_com_number()
                    pub.sendMessage('serialUpdate', arg1=serial_port)
            time.sleep(1)


if __name__ == '__main__':
    ser = SerialDetection()
    ser.setDaemon(False)
    ser.start()
