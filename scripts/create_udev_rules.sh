#!/bin/bash

echo "remap the device serial port(ttyUSBX) to usb_can_analyzer"
echo "sudo cp `rospack find usb_can_analyzer_ros`/scripts/usb_can_analyzer.rules  /lib/udev/rules.d"
sudo cp `rospack find usb_can_analyzer_ros`/scripts/usb_can_analyzer.rules  /lib/udev/rules.d
echo " "
echo "Restarting udev"
echo "sudo service udev reload"
sudo service udev reload
echo "sudo service udev restart"
sudo service udev restart
echo "finish"
