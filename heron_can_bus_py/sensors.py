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
            "MAX_RANGE": 1.5,
            "FRAME_ID": "IR"
        },
        "US": {
            "RADIATION_TYPE": ULTRASOUND,
            "FIELD_OF_VIEW": (120 * pi) / 180,
            "MIN_RANGE": 0.5,
            "MAX_RANGE": 3,
            "FRAME_ID": "US"
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

    def getDistance(self):
        return self.distance


class IR_EDUCATSensor(EDUCATSensor):
    RADIATION_TYPES = [EDUCATSensor.SENSORS["IR"]["RADIATION_TYPE"]] * 5
    FIELD_OF_VIEW = [EDUCATSensor.SENSORS["IR"]["FIELD_OF_VIEW"]] * 5
    MIN_RANGE = [EDUCATSensor.SENSORS["IR"]["MIN_RANGE"]] * 5
    MAX_RANGE = [EDUCATSensor.SENSORS["IR"]["MAX_RANGE"]] * 5
    FRAME_ID = [EDUCATSensor.SENSORS["IR"]["FRAME_ID"]] * 5

    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        super().manageMsg(msgType, serviceID, msgPayload)
        #if (serviceID == 2):
        self.distance = [int(msgPayload[0:2].hex(), base=16),
                        msgPayload[2],
                        msgPayload[3],
                        msgPayload[4],
                        msgPayload[5]
        ]


class IRUS_EDUCATSensor(EDUCATSensor):
    RADIATION_TYPES = [None] + [EDUCATSensor.SENSORS["US"]["RADIATION_TYPE"]] + [EDUCATSensor.SENSORS["IR"]["RADIATION_TYPE"]] * 3
    FIELD_OF_VIEW = [None] + [EDUCATSensor.SENSORS["US"]["FIELD_OF_VIEW"]] + [EDUCATSensor.SENSORS["IR"]["FIELD_OF_VIEW"]] * 3
    MIN_RANGE = [min(EDUCATSensor.SENSORS["US"]["MIN_RANGE"], EDUCATSensor.SENSORS["IR"]["MIN_RANGE"])] + [EDUCATSensor.SENSORS["US"]["MIN_RANGE"]] + [EDUCATSensor.SENSORS["IR"]["MIN_RANGE"]] * 3
    MAX_RANGE = [max(EDUCATSensor.SENSORS["US"]["MAX_RANGE"], EDUCATSensor.SENSORS["IR"]["MAX_RANGE"])] + [EDUCATSensor.SENSORS["US"]["MAX_RANGE"]] + [EDUCATSensor.SENSORS["IR"]["MAX_RANGE"]] * 3
    FRAME_ID = ["IR_US"] + [EDUCATSensor.SENSORS["US"]["FRAME_ID"]] + [EDUCATSensor.SENSORS["IR"]["FRAME_ID"]] * 3

    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        super().manageMsg(msgType, serviceID, msgPayload)
        #if (serviceID == 2):
        self.distance = [int(msgPayload[0:2].hex(), base=16),
                        int(msgPayload[2:4].hex(), base=16),
                        msgPayload[4],
                        msgPayload[5],
                        msgPayload[6]
        ]


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
