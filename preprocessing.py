import subprocess
import sys
import os
import shutil
from pathlib import Path
import filecmp

"""
Step 0. Delete top folder layer
"""


def dir_depth(dir_path, depth=0):
    max_depth = depth
    for dir in Path(dir_path).iterdir():
        if dir.is_dir():
            max_depth = max(max_depth, dir_depth(dir, depth + 1))
    return max_depth


def delete_top_folder_layer(root_path):
    folder_to_remove = set()
    for dir in Path(root_path).iterdir():
        if dir.is_dir():
            for subdir in dir.iterdir():
                if subdir.is_dir():
                    folder_to_remove.add(subdir)
                    for content in subdir.iterdir():
                        if not str(content).endswith(".DS_Store"):
                            shutil.move(str(content), str(dir))
                else:
                    os.remove(str(subdir))
        else:
            os.remove(str(dir))
    for folder in folder_to_remove:
        shutil.rmtree(str(folder))


"""
Step 1. Move files to newly created folder
"""
bash_script = "./1.move_files_to_folders.sh"


"""
Step 2. Delete duplicates by comparing subfolders
"""


def find_and_remove_duplicate_folders(path):
    folders = [dir for dir in Path(path).iterdir() if dir.is_dir()]
    total_deleted = 0
    folders_to_delete = set()
    for i, folder1 in enumerate(folders):
        for folder2 in folders[i + 1 :]:
            duplicate_files = filecmp.dircmp(folder1, folder2).same_files
            if "SIGNAL.RAW" in duplicate_files:
                folder_to_delete = min(str(folder1), str(folder2))
                folders_to_delete.add(folder_to_delete)
    for folder in folders_to_delete:
        total_deleted += 1
        shutil.rmtree(folder)
        print(f"Deleted duplicate folder: {folder}")
    return total_deleted


"""
Step 3. Flatten folder structure right below root directory
"""


def flatten_dirs(root_dir_path):
    count = 0
    for dir in Path(root_dir_path).iterdir():
        for subdir in dir.iterdir():
            if subdir.is_dir():
                dir_list = os.listdir(root_dir_path)
                dir_name = subdir.name.split("/")[-1]
                if dir_name in dir_list:
                    new_name = 1
                    while str(new_name) in dir_list:
                        new_name += 1
                    new_path = os.path.join(root_dir_path, str(new_name))
                else:
                    new_path = os.path.join(root_dir_path, dir_name)
                shutil.move(str(subdir), new_path)
                print(f"Moved {subdir} -> {new_path}")
                count += 1
        shutil.rmtree(dir)
    print(f"\ntotal count: {count}")


"""
Step 4. Check folders which don't have SIGNAL.RAW
"""


def delete_folder_without_raw(root_dir_path):
    for dir in Path(root_dir_path).iterdir():
        if dir.is_dir():
            FOUND_RAW = False
            for file in dir.iterdir():
                filename = file.name.split("/")[-1].upper()
                if filename == "SIGNAL.RAW":
                    FOUND_RAW = True
            if not FOUND_RAW:
                os.remove(str(dir))
                print(f"folder without SIGNAL.RAW: {dir} -> Deleted")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        root_path = sys.argv[1]
    else:
        print("Please enter valid input path")
        exit()
    # 0 Delete top folder layers
    delete_top_folder_layer(root_path)
    # 1 Move files to newly created folders
    subprocess.run([bash_script, root_path])
    print("---------------------------------------------------------------")
    # 2 Delete duplicated folders
    subfolders = [dir for dir in Path(root_path).iterdir() if dir.is_dir()]
    total_deleted = 0
    for subdir in subfolders:
        total_deleted += find_and_remove_duplicate_folders(subdir)
    print(f"\ntotal deleted: {total_deleted}")
    print("---------------------------------------------------------------")
    # 3 Flatten folder structures under root
    flatten_dirs(root_path)
    print("---------------------------------------------------------------")
    # 4 Check corrupted folders
    delete_folder_without_raw(root_path)
