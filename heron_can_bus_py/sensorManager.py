#!/usr/bin/env python3
# coding: utf-8


from threading import Thread
from typing import Union, Tuple, List
from time import sleep, time

from rospy import Publisher, init_node, is_shutdown, ROSException, get_time

from sensor_msgs.msg import Range
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
        self.readingMessage = self.readMessage(self.converter, self.sensors)
        self.runningNode = self.runNode(self.converter, self.period, self.sensors)
        self.publishingROS = self.publishROS(self.converter, self.period, self.sensors)

    def launchThreads(self):
        self.readingMessage.start()
        self.runningNode.start()
        self.publishingROS.start()
        self.publishingROS.join()
        self.runningNode.stop()
        self.readingMessage.stop()


    class readMessage(Thread):
        def __init__(self, converter, sensors):
            Thread.__init__(self)
            self.converter = converter
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
                nb_pub = 0
                for sensor in self.sensors.values():
                    if sensor.FRAME_ID != None: nb_pub += len(sensor.FRAME_ID)
                self.publisher = Publisher("ir_irus", Range, queue_size=nb_pub)
                self.msg = Range()

            def run(self):
                while not is_shutdown():
                    self.publish()
                    print()

            def publish(self):
                for node in self.sensors.values():
                    distances = node.getDistance()
                    print(str(node.ID) + ":", distances)
                    for i in range(len(distances)):
                        self.msg.header.stamp.secs = int(time())
                        self.msg.header.stamp.nsecs = int((time() - self.msg.header.stamp.secs) * 10**9)
                        self.msg.header.frame_id = node.name + " " + node.FRAME_ID[i]
                        self.msg.radiation_type = node.RADIATION_TYPES[i]
                        self.msg.field_of_view = node.FIELD_OF_VIEW[i]
                        self.msg.min_range = node.MIN_RANGE[i]
                        self.msg.max_range = node.MAX_RANGE[i]
                        self.msg.range = distances[i]
                        try :
                            self.publisher.publish(self.msg)
                        except ROSException as e :
                            if not is_shutdown(): print(e)
                            # /!\ is_shutdown() reste à False un certain temps entre le début d'arrêt de la node
                            #     (et l'arrêt du topic associé si aucune autre node le maintient)
                            #     et l'arrêt définitif de la node
                sleep(self.period)

            def __del__(self):
                del self.msg
                del self.publisher


    def __del__(self):
        del self.publishingROS
        del self.runningNode
        del self.readingMessage
        for sensor in self.sensors.values():
            del sensor
        del self.converter


if __name__ == "__main__":
    sensorManager = SensorManager(
        ("/dev/ttyUSB0", 115200),
        0.001,
        [
            (11, "ir_front_left"), (12, "ir_front_right"),
            (13, "ir_back_left"), (14, "ir_back_right"),
            (15, "ir_back"),
            (21, "ir_us_left"), (22, "ir_us_right")
        ]
    )
    sensorManager.launchThreads()
    del sensorManager
