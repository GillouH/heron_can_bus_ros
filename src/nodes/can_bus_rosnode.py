#!/usr/bin/env python3
# coding: utf-8


from rospy import get_caller_id, init_node, Subscriber, spin

from heron_can_bus_ros.msg import CANSensors


def callback(data):
	print(get_caller_id())
	for position in ("ir_front_left", "ir_back_right"):
		sensorSet = getattr(data, position)
		affichage = "\t" + sensorSet[0].header.frame_id + ": ["
		for sensor in sensorSet[:-1]:
			affichage += str(round(sensor.range*100, 3)) + ", "
		affichage += str(round(sensorSet[len(sensorSet)-1].range*100, 3)) + "]"
		print(affichage)


if __name__ == "__main__":
	try:
		init_node("Presentation")
		Subscriber("ir_irus", CANSensors, callback)
		spin()
	except KeyboardInterrupt:
		pass
	finally:
		pass
