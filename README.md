# vcore-idex
v-core idex config

slicer start gcode:
START_PRINT FIRST_LAYER_TEMP={first_layer_temperature} OTHER_LAYER_TEMP={temperature} BED_TEMP={first_layer_bed_temperature} INITIAL_TOOL={initial_tool} TOTAL_TOOLCHANGES={total_toolchanges} WIPE_TOWER={wipe_tower}

slicer end gcode:
END_PRINT

before layer change gcode:
_LAYER_CHANGE

tool change gcode:
T[next_extruder] PRINTING=1

