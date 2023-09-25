# V-Core IDEX for RatOS 2.X
This is a temporary RatOS IDEX Implementation. It will be online until RatOS gets this feature
- RatOS macro compatibility 
- octopus v1.1 idex board configuration 
- dual EBB42 toolboards with autoflashing
- native IDEX copy and mirror mode 
- adaptive bed meshing for both toolheads
- **NEW!** - ultra fast toolchanges, up to 0.3 seconds
- **NEW!** - visual assisted toolhead offset calibration
- **NEW!** - built in z-offset probe support
- **NEW!** - [better oozeguards](oozeguard)
<!-- - **NEW!** - IDEX ***spool mode***, infinite spool feature  
- **NEW!** - IDEX ***mixed mode***, inversed multicolor prints in copy and mirror mode  
- **NEW!** - IDEX ***free mode***, soon  -->

# V-Core IDEX toolchange video
[![V-Core IDEX Toolchange](https://img.youtube.com/vi/lKBVmPfxjEk/maxresdefault.jpg)](https://youtu.be/lKBVmPfxjEk)

# **CHANGE**! Inverted hybrid core-xy
You need to activate the new `inverted` setting in your `dual_carriage` configuration
```
[dual_carriage]
inverted: True
```

# **CHANGE**! Toolhead order
The `X` and `Dual Carriage` positions have changed. Make sure your toolheads are on the correct side, you might need to swap the stepper connectors on your board.
- Left toolhead **MUST** be the ```X``` toolhead
- Right toolhead **MUST** be the ```Dual Carriage``` toolhead

# **CHANGE**! Probing with both toolheads
You can now put the z-probe on any of the toolheads. Configure it with the RatOS Variable `default_toolhead`.
```
[gcode_macro RatOS]
variable_default_toolhead: 1 		# 0 = Left, 1 = Right
```

# Hardware
- Left toolhead **MUST** be the ```X``` toolhead
- Right toolhead **MUST** be the ```Dual Carriage``` toolhead
- Name your extruders ```extruder``` *left* and ```extruder1``` *right*
- Name your toolboards ```toolboard``` *left* and ```toolboardb``` *right*
- Name your toolboard adxl ```adxl345 toolboard``` *left* and ```adxl345 toolboardb``` *right*
- Name your part cooling fans ```heater_fan toolhead_cooling_fan``` *left* and ```heater_fan toolhead_cooling_fanb``` *right*
- make sure the nozzle from the z-probe toolhead is **NOT** higher then the other nozzle, ideally they have the same z-offset
- place the `X` and `DUAL_CARRIAGE` endstop stoppers as much outside as possible, to their max positions where they still work
- tune the `X` and `DUAL_CARRIAGE` `endstop_position` values to its correct positions 
- your toolhead offsets should be less than 1mm

# Install RatOS IDEX
- install RatOS for V-Core 3
- update klipper
- clone the idex repo
```
cd ~/
git clone https://github.com/HelgeKeck/vcore-idex.git
bash ~/vcore-idex/install.sh
```
- add the update manager entry to the moonraker.conf file in your config folder
```ini
[update_manager IDEX]
type: git_repo
primary_branch: main
path: ~/vcore-idex
origin: https://github.com/HelgeKeck/vcore-idex.git
managed_services:
	klipper
```
- reboot, not your laptop

# IDEX modes
- by default the printer will be in single toolhead mode.
- to enable the Copy or Mirror mode for the next print, home your printer and then execute the ```IDEX_COPY``` or ```IDEX_MIRROR``` GCODE macro.
- execute ```IDEX_SINGLE``` to switch back to normal mode.

# Toolchange configuration
- `ZHOP` Z-Hop before and after the toolchange, in addition to the slicer z-hop 
- `COMBINED_ZHOP` 0=OFF 1=ON. Combines z-hop/z-drop with retraction/deretraction moves
- `M400` 0=OFF 1=ON. Turn M400, for the z-hops and z-drops, on or off
- `RETRACT` Retraction before the toolchange
- `EXTRUDE` Extrusion after the toolchange
- `FEEDRATE` Feedrate for retract/extrude
- `SPEED` XY Travel Speed
- `ACCEL` XY Travel Accel
- `SYNC_FANS` 0=OFF 1=ON. Forces fan synchronisation in single mode. *Helpful because the new ultra fast toolchanges can be **MUCH** faster than your part cooling fan spin up time. **TIP! The Sanyo Denki 9GAX0412P3S001 4028 is almost as fast as the toolchanges***   

<img src="gfx/toolchange.jpg" alt="" width="320"/>

# Manual toolhead offset calibration
- for the X and Y calibration use the `calibrate_separation` macro to print the calibration lines, you are responsible for heating up your bed and extruders, dont forget to z-tilt and the bed mesh
- use the `SET_SEPARATION` macro to enter your toolhead offsets from the left toolhead

<img src="gfx/set_separation.jpg" alt="" width="320"/>

- *`X=1` to set the x-offset to 1*
- *`X_ADJUST=1` to add 1 to the current x-offset*
- *`X_ADJUST=-1` to subtract 1 from the current x-offset*

# Visual assisted toolhead offset calibration
Utilize an affordable camera such as the Raspberry Pi 5MP for swift and precise toolhead offset adjustments, accomplished in mere seconds.

[read more](doc/vaoc.md)

<img src="gfx/nozzle_calibration2.jpg" alt="" width="480"/>

# IDEX Mainsail modifications

Idex mode controls 

<img src="gfx/toolheadpanel.jpg" alt="" width="320"/>

Idex extruder controls 

<img src="gfx/extruderpanel.jpg" alt="" width="320"/>

# Prusa Slicer / Super Slicer

- Start G-Code
```ini
START_PRINT EXTRUDER_TEMP={first_layer_temperature[0]} EXTRUDER_TEMP_1={first_layer_temperature[1]} EXTRUDER_OTHER_LAYER_TEMP={temperature[0]} EXTRUDER_OTHER_LAYER_TEMP_1={temperature[1]} BED_TEMP=[first_layer_bed_temperature] X0={first_layer_print_min[0]} Y0={first_layer_print_min[1]} X1={first_layer_print_max[0]} Y1={first_layer_print_max[1]} INITIAL_TOOL={initial_tool} COLOR={extruder_colour[0]} COLOR_1={extruder_colour[1]}
```

- End G-Code
```ini
END_PRINT
```

- Before layer change G-Code
```ini
_LAYER_CHANGE
```

- Tool change G-Code. 
Both lines are important
```ini
;tool change post processor tag
T[next_extruder] P1
```

- G-code substitutions

<img src="gfx/color.jpg" alt="" width="640"/>

- Post processing script. 
Optional but recommended, tells klipper if all toolheads are in use.
```ini
ENTER_YOUR_PATH_TO_PYTHON\python3.exe "ENTER_YOUR_PATH_TO_THE_FILE\postprocessor.py"
```

- Super fast tool changes post processing script. 
EXPERIMENTAL, ultra fast and seamless IDEX toolchanges. 
```ini
ENTER_YOUR_PATH_TO_PYTHON\python3.exe "ENTER_YOUR_PATH_TO_THE_FILE\ftc.py"
```
