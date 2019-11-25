#!/usr/bin/env python3
# coding: utf-8

from threading import Thread
from typing import Union, Tuple

from usb_can_analyzer.sensors import IRSensor, IRUSSensor
from usb_can_analyzer.converter import Converter


class SensorManager(Thread):
    def __init__(self, converter : Tuple[str, int, int], IRSensors : Union[int] = [], IRUSSensors : Union[int] = []):
        Thread.__init__(self)
        self.converter = Converter(*converter)
        self.sensors = {}
        for ID in IRSensors:
            self.sensors[ID] = IRSensor(ID)
        for ID in IRUSSensors:
            self.sensors[ID] = IRUSSensor(ID)

    def sendMessage(self, msgType: int, serviceID: int, nodeID : int, payload : str):
        self.converter.sendMessage(msgType, serviceID, nodeID, payload)

    def run(self):
        while True:
            msgType, serviceID, nodeID, msgPayload = self.converter.readMessage()
            self.sensors[nodeID].manageMsg(msgType, serviceID, msgPayload)


if __name__ == "__main__":
    try:
        sensorManager = SensorManager(("COM7",), [0, 1, 2, 44, 45], [3, 43])
        sensorManager.start()
        payload = 0x00
        while True :
            sensorManager.sendMessage(Converter.TYPE_MSG[0], 0b1010, 0b111010, format(payload, '02x'))
            if (payload < 0xFF):
                payload += 1
            else:
                payload = 0x00
            #time.sleep(1)	#pause nécessaire pour la carte arduino ISEN, sinon elle peut ne plus fonctionner correctement + faire 'import time' pour utiliser cette méthode
    except KeyboardInterrupt:
        pass
    finally:
        pass
