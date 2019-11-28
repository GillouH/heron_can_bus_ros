#!/usr/bin/env python3
# coding: utf-8


#from usb_can_analyzer.useful import ImplementError


class Sensor:
    def __init__(self, ID: int):
        self.ID = ID
#    def manageMsg(self, msgType: int, serviceID: int, msgPayload: str):
#        raise ImplementError("Not implemented method")

class IRSensor(Sensor):
    def __init__(self, ID: int):
        super().__init__(ID)
#    def manageMsg(self, msgType: int, serviceID: int, msgPayload: str):
#        pass

class IRUSSensor(Sensor):
    def __init__(self, ID: int):
        super().__init__(ID)
#    def manageMsg(self, msgType: int, serviceID: int, msgPayload: str):
#        pass


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
