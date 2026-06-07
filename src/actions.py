"""
Defines a set of deterministic filesystem operations used to execute validated plans the execution system.

These functions are not directly invoked by the LLM.
"""

from __future__ import annotations

import os
import shutil
from typing import List

def list_files(path: str) -> List[str]:
    """
    Returns a flat list of files and top level folders in a directory as paths.

    Args:
        path: Target directory path

    Returns:
        List of file and folder paths.
    """

    if not os.path.isdir(path):
        print(f"Invalid directory: {path}")
        raise SystemExit

    items = []
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)
        items.append(full_path)

    return items

def move_item(src: str, dst_folder: str) -> None:
    """
    Moves a file or folder to a destination folder.

    Args:
        src: Full source file or folder path
        dst_folder: Destination directory (NOT full file path)

    Behavior:
        - Preserves original name
        - Moves files or folders as atomic units
        - Creates destination folder if it doesn't exist
        - Prevents accidental overwrite by auto-renaming
    """

    if not os.path.exists(src):
        raise ValueError(f"Source path does not exist: {src}")

    if not os.path.isdir(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)

    name = os.path.basename(src)
    dst_path = os.path.join(dst_folder, name)

    # Prevent overwrite safely
    if os.path.exists(dst_path):
        base, ext = os.path.splitext(name)
        counter = 1

        while os.path.exists(dst_path):
            new_name = f"{base} ({counter}){ext}"
            dst_path = os.path.join(dst_folder, new_name)
            counter += 1

    shutil.move(src, dst_path)
    print("Moved   " + name + "   to   " + dst_path)

def create_folder(path: str) -> None:
    """
    Creates a folder if it does not already exist.

    Args:
        path: Folder path to create
    """
    os.makedirs(path, exist_ok=True)
    print("Created folder   " + os.path.basename(path) + "   at   " + path)

