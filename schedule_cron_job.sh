#!/bin/bash
echo "" >>/etc/crontab
echo "* * * * * pi cd /home/pi/PiTempSensor && python tempsensor.py" >>/etc/crontab
