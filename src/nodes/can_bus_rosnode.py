#!/usr/bin/env python3
# coding: utf-8


from heron_can_bus_py import SensorManager


if __name__ == "__main__":
    test = SensorManager(("/dev/ttyUSB0",))
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
