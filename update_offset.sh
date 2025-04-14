#!/bin/bash

# Check if a new value is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <new_number>"
    exit 1
fi

NEW_VALUE=$1
TARGET_FILE="./macros/primaries_directory.mac"

# Check if the target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "File $TARGET_FILE does not exist"
    exit 1
fi

# Use sed to replace the line that starts with /mygen/primariesoffset and has a number
# Create a backup of the original file with .bak extension
sed -i.bak -E "s|^(/mygen/primariesoffset )[0-9]+$|\1$NEW_VALUE|" "$TARGET_FILE"

echo "Updated primariesoffset to $NEW_VALUE. Backup created at ${TARGET_FILE}.bak"

