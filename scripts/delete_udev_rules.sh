#!/bin/bash

echo "delete remap the device serial port(ttyUSBX) to usb_can_analyzer"
echo "sudo rm /lib/udev/rules.d/usb_can_analyzer.rules"
sudo rm /lib/udev/rules.d/usb_can_analyzer.rules
echo " "
echo "Restarting udev"
echo "sudo service udev reload"
sudo service udev reload
echo "sudo service udev restart"
sudo service udev restart
echo "finish delete"
