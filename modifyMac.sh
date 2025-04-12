#!/bin/bash

xStep=$1
yStep=$2
xStepSize=200
yStepSize=200

xDirStep=$3
yDirStep=$4
xDirStepSize=0.2
yDirStepSize=0.2


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set MACRO_FILE as the WCSim.mac in current directory of this script
MACRO_FILE="${SCRIPT_DIR}/WCSim.mac"

#================== find the line ==================#
original_direction=$(grep '^/gun/direction' "$MACRO_FILE")
original_position=$(grep '^/gun/position' "$MACRO_FILE")


#================== load original position ==================#
# /gun/direction -0.4 0 0.6 #x, y, z
dir_x=$(echo "$original_direction" | awk '{print $2}')
dir_y=$(echo "$original_direction" | awk '{print $3}')
dir_z=$(echo "$original_direction" | awk '{print $4}')

# /gun/position 500 -144 1200 mm #x, y, z
pos_x=$(echo "$original_position" | awk '{print $2}')
pos_y=$(echo "$original_position" | awk '{print $3}')
pos_z=$(echo "$original_position" | awk '{print $4}')

echo "==== before ===="
echo "Original direction: $original_direction"
echo "Original position : $original_position"
echo

#================== new direction ==================#
# direction
new_dir_x=$(echo "scale=6; $dir_x + $xDirStep * $xDirStepSize" | bc)
new_dir_x=$(echo "$new_dir_x" | sed 's/^\./0./')
new_dir_y=$(echo "scale=6; $dir_y + $yDirStep * $yDirStepSize" | bc)
new_dir_y=$(echo "$new_dir_y" | sed 's/^\./0./')
new_dir_z="$dir_z"  

# position
new_pos_x=$(echo "scale=6; $pos_x + $xStep * $xStepSize" | bc)
new_pos_y=$(echo "scale=6; $pos_y + $yStep * $yStepSize" | bc)
new_pos_z="$pos_z"

# new lines
new_direction_line="/gun/direction $new_dir_x $new_dir_y $new_dir_z "
new_position_line="/gun/position $new_pos_x $new_pos_y $new_pos_z mm "

echo "==== after (writing) ===="
echo "New direction: $new_direction_line"
echo "New position : $new_position_line"
echo


sed -i "s@^/gun/direction.*@${new_direction_line}@" "$MACRO_FILE"
sed -i "s@^/gun/position.*@${new_position_line}@" "$MACRO_FILE"


echo "==== WCSim.mac modified to be: ===="
cat "$MACRO_FILE"

