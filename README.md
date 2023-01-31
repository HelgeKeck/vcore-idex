# vcore-idex
v-core idex config

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
