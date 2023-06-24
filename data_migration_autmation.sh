#!/bin/bash
log_file="$(dirname "$0")/sdmlog.txt"

while true; do
    # 1. Find the first non-"Macintosh HD" volume in /Volumes
    while read -r volume_name; do
        if [ "$volume_name" != "Macintosh HD" ] && [ "$volume_name" != "T7 Touch" ]; then
            volume_path="/Volumes/$volume_name"
            break
        fi
    done <<< "$(ls /Volumes)"

    # 2. Check if a non-"Macintosh HD" and non-"T7 Touch" volume was found
    if [ -z "$volume_path" ]; then
        sleep 3
        continue
    fi

    start_time=$(date +%s)

    # 3. Wait for the volume to be fully mounted before accessing its contents
    echo "Waiting for volume \"$volume_path\" to be fully mounted..."
    while ! diskutil info "$volume_path" >/dev/null 2>&1; do
        sleep 1
    done

    # 4. Find the highest integer value among the existing folders
    external_drive="/Volumes/T7 Touch/sleep"
    max_folder_name=0
    for folder in "$external_drive"/*; do
        if [ -d "$folder" ]; then
            folder_name=$(basename "$folder")
            if [[ "$folder_name" =~ ^[0-9]+$ ]]; then
                if [ "$folder_name" -gt "$max_folder_name" ]; then
                    max_folder_name=$folder_name
                fi
            fi
        fi
    done

    # Increment the highest integer value by one and create a new folder
    next_folder_name=$((max_folder_name + 1))
    next_folder_path="$external_drive/$next_folder_name"
    mkdir -p "$next_folder_path"

    # 4. Copy data from the volume to an external hard drive
    rsync -ac --exclude 'Video/' --exclude 'Reports/' --backup "$volume_path" "$next_folder_path"

    # Remove data in the CD
    # cd_device=$(drutil status | grep "Type: " | awk '{print $3}')

    # 5. Eject the CD
    drutil eject $cd_device

    end_time=$(date +%s)
    elapsed_time=$((end_time - start_time))
    minutes=$((elapsed_time / 60))
    seconds=$((elapsed_time % 60))

    echo "Data copied from \"$volume_path\" to \"$next_folder_path\""
    echo "${minutes}m ${seconds}s: $(date +%m/%d/%Y\ %H:%M:%S): Data copied from \"$volume_path\" to \"$next_folder_path\"" >> "$log_file"

    unset volume_path

done