# V-Ccore IDEX For RatOS 2.02
This is a temporary RatOS IDEX Implementation. It will be online until RatOS gets this feature
- RatOS macro compatibility 
- octopus v1.1 idex board configuration 
- dual EBB42 toolboards with autoflashing
- native IDEX copy and mirror mode 
- adaptive bed meshing for both toolheads
- ultra fast toolchanges

# V-Core IDEX Toolchange Video
[![V-Core IDEX Toolchange](https://img.youtube.com/vi/lKBVmPfxjEk/maxresdefault.jpg)](https://youtu.be/lKBVmPfxjEk)

# Hardware Installation
- Left toolhead **MUST** be the ```Dual Carriage``` toolhead
- Right toolhead **MUST** be the ```X``` toolhead
- Name your extruders ```extruder``` *left* and ```extruder1``` *right*
- Name your toolboards ```toolboard``` *left* and ```toolboardb``` *right*
- Name your toolboard adxl ```adxl345 toolboard``` *left* and ```adxl345 toolboardb``` *right*
- Name your part cooling fans ```heater_fan toolhead_cooling_fan``` *left* and ```heater_fan toolhead_cooling_fanb``` *right*
- The z-probe **MUST** be on to the right toolhead

# Secondary BTT EBB42 V1.2 autoflashing
- copy the [btt-ebb42-12b](/klipper_config/RatOS/boards) folder into the ```~/printer_data/config/RatOS/boards``` folder on your raspberry PI
- ssh into the PI and run `sudo ~/printer_data/config/RatOS/scripts/ratos-update.sh`
- restart the PI
- you can now flash and autoflash the secondary toolboard

<img src="gfx/ebb42_autoflash.jpg" alt="" width="480"/>

# Toolhead Offsets
- copy the [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) file into the ```~/printer_data/config/``` folder on your raspberry PI
- do not touch the content of the file!
- restart klipper
- make sure your left toolhead z-offset is not negative, means it should not be lower then the nozzle from the right toolhead
- for the X and Y calibration use the `calibrate_separation` macro to print the calibration lines, you are responsible for heating up your bed and extruders, dont forget to z-tilt and the bed mesh
- use the `SET_SEPARATION` macro to enter your toolhead offsets from the left toolhead

<img src="gfx/set_separation.jpg" alt="" width="320"/>

- *`X=1` to set the x-offset to 1*
- *`X_ADJUST=1` to add 1 to the current x-offset*
- *`X_ADJUST=-1` to subtract 1 from the current x-offset*

# Toolchange Configuration
- `ZHOP` Z-Hop before and after the toolchange, in addition to the slicer z-hop 
- `COMBINED_ZHOP` 0=OFF 1=ON. Combines z-hop/z-drop with retraction/deretraction moves
- `M400` 0=OFF 1=ON. Turn M400, for the z-hops and z-drops, on or off
- `RETRACT` Retraction before the toolchange
- `EXTRUDE` Extrusion after the toolchange
- `FEEDRATE` Feedrate for retract/extrude
- `SPEED` XY Travel Speed
- `ACCEL` XY Travel Accel
- `SYNC_FANS` 0=OFF 1=ON. Forces fan synchronisation in single mode

<img src="gfx/toolchange.jpg" alt="" width="320"/>

# IDEX modes
- by default the printer will be in single toolhead mode.
- to enable the Copy or Mirror mode for the next print, home your printer and then execute the ```IDEX_COPY``` or ```IDEX_MIRROR``` GCODE macro.
- execute ```IDEX_SINGLE``` to switch back to normal mode.
# Prusa Slicer / Super Slicer

- Start G-Code
```ini
START_PRINT EXTRUDER_TEMP={first_layer_temperature[0]} EXTRUDER_TEMP_1={first_layer_temperature[1]} EXTRUDER_OTHER_LAYER_TEMP={temperature[0]} EXTRUDER_OTHER_LAYER_TEMP_1={temperature[1]} BED_TEMP=[first_layer_bed_temperature] X0={first_layer_print_min[0]} Y0={first_layer_print_min[1]} X1={first_layer_print_max[0]} Y1={first_layer_print_max[1]} INITIAL_TOOL={initial_tool}
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
