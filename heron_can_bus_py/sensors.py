#!/usr/bin/env python3
# coding: utf-8


from abc import ABCMeta, abstractmethod
from typing import Tuple
from math import pi


class EDUCATSensor(metaclass=ABCMeta):
    ULTRASOUND = 0
    INFRARED = 1
    SENSORS = {
        "IR": {
            "RADIATION_TYPE": INFRARED,
            "FIELD_OF_VIEW": (27 * pi) / 180,
            "MIN_RANGE": 0.05,
            "MAX_RANGE": 1.5
            #"FRAME_ID": "IR"
        },
        "US": {
            "RADIATION_TYPE": ULTRASOUND,
            "FIELD_OF_VIEW": (120 * pi) / 180,
            "MIN_RANGE": 0.5,
            "MAX_RANGE": 3
            #"FRAME_ID": "US"
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

    def __init__(self, ID: int, position: str):
        self.ID = ID
        self.distance = []
        self.position = position

    @abstractmethod
    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        pass

    def correctDistance(self):
        for i in range(len(self.distance)):
            if self.distance[i] == 0:  self.distance[i] = -1
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
        if (serviceID == 2):
            self.distance = [int(msgPayload[0:2].hex(), base=16),
                            msgPayload[2],
                            msgPayload[4],  # Capteurs 2 et 3 inversés dans les nodes
                            msgPayload[3],  # Capteurs 2 et 3 inversés dans les nodes
                            msgPayload[5]
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
        if (serviceID == 2):
            self.distance = [int(msgPayload[0:2].hex(), base=16),
                            int(msgPayload[2:4].hex(), base=16),
                            msgPayload[4],
                            msgPayload[5],
                            msgPayload[6]
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
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
