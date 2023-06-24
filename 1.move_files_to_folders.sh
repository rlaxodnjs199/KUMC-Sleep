#!/bin/bash

root_directory="$1"

# Function to create a new integer-named folder if needed
create_new_folder() {
    local dir="$1"
    local i=1
    while true; do
        if [ ! -d "$dir/$i" ]; then
            mkdir "$dir/$i"
            echo "$dir$i"
            break
        fi
        i=$((i + 1))
    done
}

# Iterate through all subdirectories of the root directory
cd "$root_directory"
for subdir in */; do
    if [ -d "$subdir" ]; then
        has_files=false

        # Check if there are files in the subdirectory
        for item in "$subdir"*; do
            if [ -f "$item" ]; then
                has_files=true
                break
            fi
        done

        # If files exist, create a new integer-named folder and move the files
        if [ "$has_files" = true ]; then
            new_folder=$(create_new_folder "$subdir")
            for item in "$subdir"*; do
                if [ -f "$item" ]; then
                    mv "$item" "$new_folder"
                fi
            done
            echo "Moved contents from $subdir to $new_folder"
        fi
    fi
done