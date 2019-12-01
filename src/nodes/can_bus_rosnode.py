#!/usr/bin/env python3
# coding: utf-8


from time import time
from heron_can_bus_ros.msg import CANSensors


if __name__ == "__main__":
    test = CANSensors()
    try:
        print(test.ir_front_left[0])
    except KeyboardInterrupt:
        pass
    finally:
        pass
