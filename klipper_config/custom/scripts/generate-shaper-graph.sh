#!/bin/bash

DISABLE_Y=0
DISABLE_X=0

if [ "$1" = "x" ]
then
	DISABLE_Y=1
fi
if [ "$1" = "y" ]
then
	DISABLE_X=1
fi

if [ ! -d "/home/pi/printer_data/config/input_shaper" ]
then
    mkdir /home/pi/printer_data/config/input_shaper
fi

T0=1
T1=1

if [ "$2" == "0" ]
then
	T1=0
fi
if [ "$2" == "1" ]
then
	T0=0
fi

DATE=$(date +'%Y-%m-%d-%H%M%S')
if [ $DISABLE_Y -eq 0 ]
then
	[ -e "/tmp/left_toolhead_y.csv" ] && rm /tmp/left_toolhead_y.csv
	[ -e "/tmp/right_toolhead_y.csv" ] && rm /tmp/right_toolhead_y.csv

	if [ $T0 -eq 1 ]
	then
		if [ ! -e "/tmp/resonances_y_t0.csv" ]
		then
			echo "ERROR: No y data found for the left toolhead (T0)"
			exit 1
		fi
		cp /tmp/resonances_y_t0.csv /tmp/left_toolhead_y.csv
		/home/pi/klipper/scripts/calibrate_shaper.py /tmp/left_toolhead_y.csv -o /home/pi/printer_data/config/input_shaper/left_toolhead_resonances_y_$DATE.png
	fi

	if [ $T1 -eq 1 ]
	then
		if [ ! -e "/tmp/resonances_y_t1.csv" ]
		then
			echo "ERROR: No y data found for right toolhbead (T1)"
			exit 1
		fi
		cp /tmp/resonances_y_t1.csv /tmp/right_toolhead_y.csv
		/home/pi/klipper/scripts/calibrate_shaper.py /tmp/right_toolhead_y.csv -o /home/pi/printer_data/config/input_shaper/right_toolhead_resonances_y_$DATE.png
	fi
fi

if [ $DISABLE_X -eq 0 ]
then
	[ -e "/tmp/left_toolhead_x.csv" ] && rm /tmp/left_toolhead_x.csv
	[ -e "/tmp/right_toolhead_x.csv" ] && rm /tmp/right_toolhead_x.csv

	if [ $T0 -eq 1 ]
	then
		if [ ! -e "/tmp/resonances_x_t0.csv" ]
		then
			echo "ERROR: No x data found for the left toolhead (T0)"
			exit 1
		fi
		cp /tmp/resonances_x_t0.csv /tmp/left_toolhead_x.csv
		/home/pi/klipper/scripts/calibrate_shaper.py /tmp/left_toolhead_x.csv -o /home/pi/printer_data/config/input_shaper/left_toolhead_resonances_x_$DATE.png
	fi

	if [ $T1 -eq 1 ]
	then
		if [ ! -e "/tmp/resonances_x_t1.csv" ]
		then
			echo "ERROR: No x data found for right toolhbead (T1)"
			exit 1
		fi
		cp /tmp/resonances_x_t1.csv /tmp/right_toolhead_x.csv
		/home/pi/klipper/scripts/calibrate_shaper.py /tmp/right_toolhead_x.csv -o /home/pi/printer_data/config/input_shaper/right_toolhead_resonances_x_$DATE.png
	fi
fi
