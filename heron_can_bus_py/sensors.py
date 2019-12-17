#!/usr/bin/env python3
# coding: utf-8


from abc import ABCMeta, abstractmethod
from typing import Tuple
from math import pi


from heron_can_bus_py import Converter


class EDUCATSensor(metaclass=ABCMeta):
    FRAME_ID = None
    RADIATION_TYPES = None
    FIELD_OF_VIEW = None
    MIN_RANGE = None
    MAX_RANGE = None

    SENSORS = {
        "IR": {
            "RADIATION_TYPE": 1,
            "FIELD_OF_VIEW": (27 * pi) / 180,
            "MIN_RANGE": 0.05,
            "MAX_RANGE": 1.5
        },
        "US": {
            "RADIATION_TYPE": 0,
            "FIELD_OF_VIEW": (120 * pi) / 180,
            "MIN_RANGE": 0.5,
            "MAX_RANGE": 3
        }
    }

    @staticmethod
    def compactedMsgID(serviceID: int, nodeID: int) -> int:
        return (serviceID << 6) + nodeID

    @staticmethod
    def decompactedMsgID(msgID: int) -> Tuple[int, int]:
        serviceID = msgID >> 6
        nodeID = msgID - (serviceID << 6)
        return serviceID, nodeID

    def __init__(self, ID: int, name: str):
        self.ID = ID
        self.name = name
        self.distance = []

    @abstractmethod
    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        pass

    def correctDistance(self):
        self.distance[0] = -1
        for i in range(1, len(self.distance)):
            if self.distance[i] == 0:  self.distance[i] = -1
            elif self.distance[i] < self.MIN_RANGE[i]: self.distance[i] = self.MIN_RANGE[i]
            elif self.distance[i] > self.MAX_RANGE[i]: self.distance[i] = self.MAX_RANGE[i]
            if self.distance[i] != -1 and (self.distance[0] > self.distance[i] or self.distance[0] == -1):  self.distance[0] = self.distance[i]

    def getDistance(self):
        return self.distance


class IR_EDUCATSensor(EDUCATSensor):
    FRAME_ID = ["MIN", "IR_0", "IR_1", "IR_2", "IR_3"]
    RADIATION_TYPES = [EDUCATSensor.SENSORS["IR"]["RADIATION_TYPE"]] * 5
    FIELD_OF_VIEW = [EDUCATSensor.SENSORS["IR"]["FIELD_OF_VIEW"]] * 5
    MIN_RANGE = [EDUCATSensor.SENSORS["IR"]["MIN_RANGE"]] * 5
    MAX_RANGE = [EDUCATSensor.SENSORS["IR"]["MAX_RANGE"]] * 5

    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        super().manageMsg(msgType, serviceID, msgPayload)
        if msgType == Converter.DATA:
            if serviceID == 2 and len(msgPayload) == 6:
                self.distance = [int(msgPayload[0:2].hex(), base=16)/100,
                                msgPayload[2]/100,
                                msgPayload[4]/100,  # Les 2 capteurs au centre inversés dans les nodes
                                msgPayload[3]/100,  # Les 2 capteurs au centre inversés dans les nodes
                                msgPayload[5]/100
                ]
                super().correctDistance()



class IRUS_EDUCATSensor(EDUCATSensor):
    FRAME_ID = ["MIN", "US_0", "IR_0", "IR_1", "IR_2"]
    RADIATION_TYPES = [None] + [EDUCATSensor.SENSORS["US"]["RADIATION_TYPE"]] + [EDUCATSensor.SENSORS["IR"]["RADIATION_TYPE"]] * 3
    FIELD_OF_VIEW = [None] + [EDUCATSensor.SENSORS["US"]["FIELD_OF_VIEW"]] + [EDUCATSensor.SENSORS["IR"]["FIELD_OF_VIEW"]] * 3
    MIN_RANGE = [None] + [EDUCATSensor.SENSORS["US"]["MIN_RANGE"]] + [EDUCATSensor.SENSORS["IR"]["MIN_RANGE"]] * 3
    MAX_RANGE = [None] + [EDUCATSensor.SENSORS["US"]["MAX_RANGE"]] + [EDUCATSensor.SENSORS["IR"]["MAX_RANGE"]] * 3

    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        super().manageMsg(msgType, serviceID, msgPayload)
        if msgType == Converter.DATA:
            if serviceID == 2 and len(msgPayload) == 6:
                self.distance = [int(msgPayload[0:2].hex(), base=16)/100,
                                int(msgPayload[2:4].hex(), base=16)/100,
                                msgPayload[4]/100,
                                msgPayload[5]/100,
                                msgPayload[6]/100
                ]
                super().correctDistance()
                self.updateInfosNode()

    def updateInfosNode(self):
        if (self.distance[0] == self.distance[1]):
            self.RADIATION_TYPES[0] = EDUCATSensor.SENSORS["US"]["RADIATION_TYPE"]
            self.FIELD_OF_VIEW[0] = EDUCATSensor.SENSORS["US"]["FIELD_OF_VIEW"]
            self.MIN_RANGE[0] = EDUCATSensor.SENSORS["US"]["MIN_RANGE"]
            self.MAX_RANGE[0] = EDUCATSensor.SENSORS["US"]["MAX_RANGE"]
        elif (self.distance[0] in self.distance[2:5]):
            self.RADIATION_TYPES[0] = EDUCATSensor.SENSORS["IR"]["RADIATION_TYPE"]
            self.FIELD_OF_VIEW[0] = EDUCATSensor.SENSORS["IR"]["FIELD_OF_VIEW"]
            self.MIN_RANGE[0] = EDUCATSensor.SENSORS["IR"]["MIN_RANGE"]
            self.MAX_RANGE[0] = EDUCATSensor.SENSORS["IR"]["MAX_RANGE"]


if __name__ == "__main__":
    try:
        IR = IR_EDUCATSensor(11, "test")
        IR.manageMsg(0, 2, b'\x00\x56\x00\x23\xB3\xF5')
    except KeyboardInterrupt:
        pass
    finally:
        pass
