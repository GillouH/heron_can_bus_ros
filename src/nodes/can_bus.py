#!/usr/bin/env python3
# coding: utf-8


from rospy import get_param, has_param, get_param_names

from heron_can_bus_py import SensorManager

converter = "/heron_can_bus_manager/converter"
period = "/heron_can_bus_manager/period"
IR_EDUCATSensors = "/heron_can_bus_manager/IR_EDUCATSensors"
IRUS_EDUCATSensors = "/heron_can_bus_manager/IRUS_EDUCATSensors"

defaultConverter = ("/dev/ttyUSB0", 115200)
defaultPeriod = 0.01
defaultIR_EDUCATSensors = [
							  (11, "ir_front_left"), (12, "ir_front_right"),
							  (13, "ir_back_left"), (14, "ir_back_right"),
							  (15, "ir_back"),
							  (21, "ir_us_left"), (22, "ir_us_right")
						  ]
defaultIRUS_EDUCATSensors = []

if __name__ == "__main__":
	print(get_param_names())
	print(has_param(converter))
	print(type(get_param(converter)))
	print(type([11, "test"]))
	"""sensorManager = SensorManager(
		get_param(converter) if has_param(converter) else defaultConverter,
		get_param(period) if has_param(period) else defaultPeriod,
		get_param(IR_EDUCATSensors) if has_param(IR_EDUCATSensors) else defaultIR_EDUCATSensors,
		get_param(IRUS_EDUCATSensors) if has_param(IRUS_EDUCATSensors) else defaultIRUS_EDUCATSensors
	)
	sensorManager.launch()
	del sensorManager"""
