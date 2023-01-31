# vcore-idex
v-core idex config with octopus v1.1 and two EBB42 toolboards

# Hardware
- Left toolhead must be the dual carriage toolhead
- Right toolhead must be the right toolhead
- Name your toolboards ```toolboard``` and ```toolboardb```
- Name your toolboard adxl ```adxl345 toolboard``` and ```adxl345 toolboardb```
- Put the z-probe to the right toolhead, it lets you probe the whole bed this way

# RatOS
- copy [ratos-variables.cfg](/klipper_config/ratos-variables.cfg) into your ```config``` folder
- Enter the offsets from the secondary toolhead, that doesnt has the probe, into the ```ratos-variables.cfg``` file 

# Macros

Toohead control

<img src="https://github.com/HelgeKeck/vcore-idex/blob/main/img/toolhead_macros.jpg" alt="" width="441"/>

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
