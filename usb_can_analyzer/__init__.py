#!/usr/bin/env python3
# coding: utf-8


from os import system
system("python3 -m pip install --user pyserial rospkg")
system("python3 -m pip install --user --upgrade pyserial rospkg")

from usb_can_analyzer.sensorManager import SensorManager


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
