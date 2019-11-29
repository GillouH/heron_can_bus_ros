#!/usr/bin/env python3
# coding: utf-8


from abc import ABCMeta, abstractmethod
from typing import Tuple


class EDUCATSensor(metaclass=ABCMeta):
    @staticmethod
    def compactedMsgID(serviceID: int, nodeID: int) -> int:
        return (serviceID << 6) + nodeID

    @staticmethod
    def decompactedMsgID(msgID: int) -> Tuple[int, int]:
        serviceID = msgID >> 6
        nodeID = msgID - (serviceID << 6)
        return serviceID, nodeID

    def __init__(self, ID : int):
    	self.ID = ID
    	self.distance = []

    @abstractmethod
    def manageMsg(self, msgType: int, serviceID: int, msgPayload: bytes):
        pass

    def getDistance(self):
        return self.distance


class IR_EDUCATSensor(EDUCATSensor):
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
