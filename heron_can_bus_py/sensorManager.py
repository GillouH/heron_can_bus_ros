#!/usr/bin/env python3
# coding: utf-8


from threading import Thread
from typing import Union, Tuple, List
from time import sleep, time

import rospy
from rospy import Publisher, init_node, is_shutdown, ROSInterruptException, get_time

from heron_can_bus_ros.msg import CANSensors
from heron_can_bus_py import Converter
from heron_can_bus_py.sensors import EDUCATSensor, IR_EDUCATSensor, IRUS_EDUCATSensor


class SensorManager():
    def __init__(self, converter: Tuple[str, int, int], period: int = 1, IR_EDUCATSensors: List[Tuple[int, str]] = [], IRUS_EDUCATSensors: List[Tuple[int, str]] = []):
        self.converter = Converter(*converter)
        self.period = period
        self.sensors = {}
        for sensor in IR_EDUCATSensors:
                self.sensors[sensor[0]] = IR_EDUCATSensor(sensor[0], sensor[1])
        for sensor in IRUS_EDUCATSensors:
                self.sensors[sensor[0]] = IRUS_EDUCATSensor(sensor[0], sensor[1])
        self.readingMessage = self.readMessage(self.converter, self.period, self.sensors)
        self.runningNode = self.runNode(self.converter, self.period, self.sensors)
        self.publishingROS = self.publishROS(self.converter, self.period, self.sensors)

    def startThread(self):
        self.readingMessage.start()
        self.runningNode.start()
        self.publishingROS.start()
        self.publishingROS.join()


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
                if type(infoMsg) == int: continue
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
            period = format(int(self.period * 1000), "x")
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
                self.initROS()

            def initROS(self):
                init_node("IR_IRUS_sensors")
                self.publisher = Publisher("ir_irus", CANSensors, queue_size=10)

            def run(self):
                seq = 0
                while not is_shutdown():
                    self.publish(seq)
                    seq += 1
                    print()

            def publish(self, seq: int):
                msg = CANSensors()
                for node in self.sensors.values():
                    distances = node.getDistance()
                    for i in range(len(distances)):
                        getattr(msg, node.position)[i].radiation_type = node.RADIATION_TYPES[i]
                        getattr(msg, node.position)[i].field_of_view = node.FIELD_OF_VIEW[i]
                        getattr(msg, node.position)[i].min_range = node.MIN_RANGE[i]
                        getattr(msg, node.position)[i].max_range = node.MAX_RANGE[i]
                        getattr(msg, node.position)[i].range = distances[i]
                        getattr(msg, node.position)[i].header.seq = seq
                        getattr(msg, node.position)[i].header.stamp.secs = int(time())
                        getattr(msg, node.position)[i].header.stamp.nsecs = int((time() - getattr(msg, node.position)[i].header.stamp.secs) * 10**9)
                        #getattr(msg, node.position)[i].header.frame_id = node.FRAME_ID[i]
                        getattr(msg, node.position)[i].header.frame_id = node.position
                    print(str(node.ID) + ":", node.getDistance())
                self.publisher.publish(msg)
                sleep(self.period)

    def stopThread(self):
        self.runningNode.stop()
        self.readingMessage.stop()

    def __del__(self):
        del self.readingMessage
        del self.runningNode
        del self.publishingROS
        del self.converter


if __name__ == "__main__":
    sensorManager = SensorManager(
        ("/dev/ttyUSB0", 115200),
        0.1,
        [
            (11, "ir_front_left"), (12, "ir_front_right"),
            (13, "ir_back_left"), (14, "ir_back_right"),
            (15, "ir_back"),
            (21, "ir_us_left"), (22, "ir_us_right")
        ]
    )
    try:
        sensorManager.startThread()
    except KeyboardInterrupt:
        pass
    finally:
        sensorManager.stopThread()
        del sensorManager
