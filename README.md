# vcore-idex
This is a temporary RatOS IDEX Implementation. It will be online until RatOS gets this feature 
- all RatOS macros are idex friendly now, inclusive homing, sensorless homing, input shaper generation, belt tension macros, ..... 
- octopus v1.1 idex board configuration 
- dual EBB42 toolboard config 
- idex hardware configs 
- based on ratos alpha4
- heats up extruder on demand
- can put extruders into standby mode 
- works with or without purge tower

# V-Core IDEX Toolchange Video
[![V-Core IDEX Toolchange](https://img.youtube.com/vi/vpZX4UYmQUg/maxresdefault.jpg)](https://youtu.be/vpZX4UYmQUg)

# Issues
- no mirror or duplication mode yet
- no initial configuration script to choose from, when installing ratos 
- there is no autoupdate for the two toolboards
- secondary toolboard needs to be flashed with a different name ```usb-Klipper_stm32g0b1xx_btt-ebb42-12b-if00``` instead of ```usb-Klipper_stm32g0b1xx_btt-ebb42-12-if00```

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

# Toolhead control

- ```T0``` and ```T1``` changes the active toolhead
- ```PARK TOOLHEAD``` to park the active toolhead

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/toolhead_macros.jpg" alt="" width="441"/>

# Parking config

- ```Z HOP``` Z-Hop before parking
- ```Z SPEED``` Z-Speed for the Z-Hop
- ```RETRACT``` Retract in mm before Z-Hop
- ```USE STANDBY``` Reduces the extruder temp if a toolhead is in parking mposition, 0=off, 1=on, dont change mid print

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/parking.jpg" alt="" width="196"/>

# Preextrude config

- ```EXTRUDE``` Extrude in mm before going back to the print job, enter ```0``` to deactivate this feature
- ```RETRACT``` Retract in mm after ```EXTRUDE``` and before going back to the print job
- ```FEEDRATE``` Feedrate for ```EXTRUDE``` and ```RETRACT AFTER``` 

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/preextrude.jpg" alt="" width="196"/>

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
START_PRINT FIRST_LAYER_TEMP={first_layer_temperature} OTHER_LAYER_TEMP={temperature} BED_TEMP={first_layer_bed_temperature} INITIAL_TOOL={initial_tool} TOTAL_TOOLCHANGES={total_toolchanges} WIPE_TOWER={wipe_tower}
```

- End G-Code
```ini
END_PRINT
```

- Before layer change G-Code
```ini
_LAYER_CHANGE
```

- Tool change G-Code
```ini
_T T=[next_extruder] PRINTING=1
```

# Oozeguards

[STL](/oozeguard/)

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/oozeguard.jpg" alt="" width="800"/>
