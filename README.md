# vcore-idex
v-core idex config with octopus v1.1 and two EBB42 toolboards

# Hardware
- Left toolhead must be the ```Dual Carriage``` toolhead
- Right toolhead must be the ```X``` toolhead
- Name your toolboards ```toolboard``` and ```toolboardb```
- Name your toolboard adxl ```adxl345 toolboard``` and ```adxl345 toolboardb```
- Put the z-probe to the right toolhead, it lets you probe the whole bed this way

# RatOS
- copy [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) into your ```config``` folder
- Enter the offsets from the secondary toolhead, that doesnt has the probe, into the ```ratos-variables.cfg``` file 

# Toolhead control

- ```T0``` and ```T1``` changes the active toolhead
- ```PARK TOOLHEAD``` to park the active toolhead

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/toolhead_macros.jpg" alt="" width="441"/>

Parking config
- ```Z HOP``` Z-Hop before parking
- ```Z SPEED``` Z-Speed for the Z-Hop
- ```RETRACT``` Retract in mm before Z-Hop

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/parking.jpg" alt="" width="192"/>

Preextrude config
- ```EXTRUDE``` Extrude in mm before going back to the print job
- ```RETRACT AFTER``` Retract in mm after ```EXTRUDE``` and before going back to the print job
- ```FEEDRATE``` Feedrate for ```EXTRUDE``` and ```RETRACT AFTER``` 

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/preextrude.jpg" alt="" width="194"/>

# Input shaper

- ```FREQUENCY START``` sets the start frequency
- ```FREQUENCY END``` sets the end frequency
- ```TOOLHEAD``` if empty = all toolheads, or ```0``` or ```1```
- ```AXIS``` if empty = all axis, or ```X``` or ```Y```

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/shaper.jpg" alt="" width="200"/>

# Load / Unload Filament

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
