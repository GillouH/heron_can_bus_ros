#!/usr/bin/env python3
# coding: utf-8


from threading import Thread
from typing import Union, Tuple
from time import sleep

from rospy import Publisher, init_node, is_shutdown, ROSInterruptException, get_time
from std_msgs.msg import String

from heron_can_bus_py import Converter
from heron_can_bus_py.sensors import EDUCATSensor, IR_EDUCATSensor, IRUS_EDUCATSensor


class SensorManager():
    def __init__(self, converter : Tuple[str, int, int], period:int = 1, IR_EDUCATSensors : Union[int] = [], IRUS_EDUCATSensors : Union[int] = []):
        self.converter = Converter(*converter)
        self.period = period
        self.sensors = {}
        for ID in IR_EDUCATSensors:
                self.sensors[ID] = IR_EDUCATSensor(ID)
        for ID in IRUS_EDUCATSensors:
                self.sensors[ID] = IRUS_EDUCATSensor(ID)
        self.readingMessage = self.readMessage(self.converter, self.period, self.sensors)
        self.runningNode = self.runNode(self.converter, self.period, self.sensors)
        self.publishingROS = self.publishROS(self.converter, self.period, self.sensors)

    def startThread(self):
        self.readingMessage.start()
        self.runningNode.start()
        self.publishingROS.start()


    class readMessage(Thread):
        def __init__(self, converter, period, sensors):
            Thread.__init__(self)
            self.converter = converter
            self.period = period
            self.sensors = sensors

        def run(self):
            self.reading = True
            while self.reading:
                infoMsg = self.converter.readMessage()
                if infoMsg == -1: continue
                msgType, msgID, payload = infoMsg
                serviceID, nodeID = EDUCATSensor.decompactedMsgID(msgID)
                if nodeID in self.sensors.keys(): self.sensors[nodeID].manageMsg(msgType, serviceID, payload)

        def stop(self):
            self.reading = False


    class runNode(Thread):
        def __init__(self, converter, period, sensors):
            Thread.__init__(self)
            self.converter = converter
            self.period = period
            self.sensors = sensors
            self.initNode()

        def initNode(self):
            period =  format(self.period, "x")
            if (len(period) % 2) != 0 : period = "0" + period
            for nodeID in self.sensors.keys():
                self.converter.sendMessage(Converter.DATA, EDUCATSensor.compactedMsgID(1, nodeID), period)


        def run(self):
            self.running = True
            while self.running:
                for nodeID in self.sensors.keys():
                    self.converter.sendMessage(Converter.REMOTE, EDUCATSensor.compactedMsgID(2, nodeID))
                sleep(self.period)

        def stop(self):
            self.running = False


    class publishROS(Thread):
            def __init__(self, converter, period, sensors):
                Thread.__init__(self)
                self.converter = converter
                self.period = period
                self.sensors = sensors

            def run(self):
                self.publishing = True
                while self.publishing:
                    for node in self.sensors.values():
                        print(str(node.ID) + ":", node.getDistance())
                    print()

            def initROS(self):
                init_node("IR_IRUS_sensors")
                self.publisher = Publisher("ir_irus", String, queue_size=10)
                while not is_shutdown():
                    test = "%s" % get_time()
                    self.publisher.publish(test)
                    sleep(1)
                #self.publisher = Publisher("battery", BatteryMsg, queue_size=5)
                #self.msg = BatteryMsg()
                #for data in self.dataSet:
                #    if "topic_name" and "unit" in data.keys():
                #        getattr(self.msg, data["topic_name"]).unit = data["unit"]

            def publish(self):
                for data in self.dataSet:
                    if "topic_name" in data.keys():
                        getattr(self.msg, data["topic_name"]).value = data["value"]
                self.publisher.publish(self.msg)

            def launch(self):
                try:
                    self.initROS()
                    self.USBcomm.open()
                    while not is_shutdown():
                        if self.process(self.USBcomm.read(size=Battery.NB_BYTES).hex()):
                            self.publish()
                    print(self)
                except ROSInterruptException:
                    pass

            def stop(self):
                self.publishing = False

    def stopThread(self):
        self.readingMessage.stop()
        self.runningNode.stop()
        self.publishingROS.stop()

    def __del__(self):
        del self.readingMessage
        del self.runningNode
        del self.publishingROS
        del self.converter


if __name__ == "__main__":
    sensorManager = SensorManager(("/dev/ttyUSB0",), 1, [10, 11, 13, 29, 43, 45], [2, 3])
    sensorManager.startThread()
    try:
        while True: pass
    except KeyboardInterrupt:
        pass
    finally:
        sensorManager.stopThread()
        del sensorManager
