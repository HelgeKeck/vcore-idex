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

# USE IT AT YOUR OWN RISK!
- contains experimental code

# Hardware
- Left toolhead must be the ```Dual Carriage``` toolhead
- Right toolhead must be the ```X``` toolhead
- Name your extruders ```extruder``` and ```extruder1```
- Name your toolboards ```toolboard``` and ```toolboardb```
- Name your toolboard adxl ```adxl345 toolboard``` and ```adxl345 toolboardb```
- Name your part cooling fans ```heater_fan toolhead_cooling_fan``` and ```heater_fan toolhead_cooling_fanb```
- The z-probe MUST be on to the right toolhead

# Toolhead Offsets
- copy [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) into your ```config``` folder
- Enter the offsets from the left toolhead
- restart klipper

Only change this!
```
[Variables]
yoffset = 0.0
xoffset = 0.0
zoffset = 0.0
```

Do not touch this!
```
[Variables]
applied_offset = 1
xcontrolpoint = 100.0
ycontrolpoint = 100.0
zcontrolpoint = 100.0
zoffsetcontrolpoint = 100.0
```

# Secondary EBB42 Toolboard autoflashing
- copy the content of the RatOS board folder into your RatOS board folder
- ssh into the PI and run `sudo ~/printer_data/config/RatOS/scripts/ratos-update.sh`
- restart PI

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/gfx/ebb42_autoflash.jpg" alt="" width="640"/>

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

# IDEX modes
- by default the printer will be in single toolhead mode.
- to enable the Copy or Mirror mode for the next print, home your printer and then execute the ```IDEX_COPY``` or ```IDEX_MIRROR``` GCODE macro.
- execute ```IDEX_SINGLE``` to switch back to normal mode.