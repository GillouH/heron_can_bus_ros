#!/usr/bin/env python3
# coding: utf-8


from os import system
system("python3 -m pip install --user usb_can_analyzer rospkg")
system("python3 -m pip install --user --upgrade usb_can_analyzer rospkg")

from usb_can_analyzer import Converter
from heron_can_bus_py.sensorManager import SensorManager


__all__ = [
    "SensorManager"
]


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
