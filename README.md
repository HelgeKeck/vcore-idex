# V-Ccore IDEX For RatOS 2.02
This is a temporary RatOS IDEX Implementation. It will be online until RatOS gets this feature
# USE IT AT YOUR OWN RISK!
# THIS IS NOT A TUTORIAL! 
- RatOS macro compatibility 
- octopus v1.1 idex board configuration 
- dual EBB42 toolboards with autoflashing
- native IDEX copy and mirror mode 
- adaptive bed meshing for both toolheads

# Hardware
- Left toolhead must be the ```Dual Carriage``` toolhead
- Right toolhead must be the ```X``` toolhead
- Name your extruders ```extruder``` and ```extruder1```
- Name your toolboards ```toolboard``` and ```toolboardb```
- Name your toolboard adxl ```adxl345 toolboard``` and ```adxl345 toolboardb```
- Name your part cooling fans ```heater_fan toolhead_cooling_fan``` and ```heater_fan toolhead_cooling_fanb```
- Put the z-probe to the right toolhead, it lets you probe the whole bed this way

# RatOS
- copy [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) into your ```config``` folder
- Enter the offsets from the secondary toolhead, that doesnt has the probe, into the ```ratos-variables.cfg``` file 
- copy [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) into your ```config``` folder
- copy the content of the RatOS board folder into your RatOS board folder

# Input shaper and Belt Tension Macros

- ```FREQUENCY START``` sets the start frequency
- ```FREQUENCY END``` sets the end frequency
- ```TOOLHEAD``` if empty = all toolheads, or ```0``` or ```1```
- ```AXIS``` if empty = all axis, or ```X``` or ```Y```

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/shaper.jpg" alt="" width="195"/>

# Load / Unload Filament Macros

- ```T``` the toolhead for the loading/unloading process, ```-1``` all extruders simultaneously 
- ```TEMP``` the temperature for the loading/unloading process

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/load_filament.jpg" alt="" width="195"/>

# Prusa Slicer / Super Slicer

- Start G-Code
```ini
START_PRINT EXTRUDER_TEMP={first_layer_temperature} BED_TEMP={first_layer_bed_temperature} X0={first_layer_print_min[0]} Y0={first_layer_print_min[1]} X1={first_layer_print_max[0]} Y1={first_layer_print_max[1]} EXTRUDER_OTHER_LAYER_TEMP={temperature} INITIAL_TOOL={initial_tool}
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
Optional but recommended, it tells klipper if all toolheads are in use or not. The file is in this repo.
```ini
ENTER_YOUR_PATH_TO_PYTHON\python3.exe "ENTER_YOUR_PATH_TO_THE_FILE\postprocessor.py"
```

# IDEX modes
- by default the printer will be in single toolhead mode.
- to enable the Copy or Mirror mode for the next print, home your printer and then execute the ```IDEX_COPY``` or ```IDEX_MIRROR``` GCODE macro.
- execute ```IDEX_SINGLE``` to switch back to normal mode.