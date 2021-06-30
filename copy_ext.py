#!/usr/bin/env python
import argparse
import os
import shutil
from pathlib import Path

# Global variables
DIRECTORY_DESTINATION = ""
DIRECTORY_SOURCE = ""
EXTENSION_TO_COPY = ""
FORCE_COPY = False
RECURSIVE = False


"""Setup"""


def _get_flag_arguments():
    # Apply arguments' values to global variables
    global DIRECTORY_DESTINATION
    global DIRECTORY_SOURCE
    global EXTENSION_TO_COPY
    global FORCE_COPY
    global RECURSIVE

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination", type=str)
    parser.add_argument("-e", "--extension", type=str, required=True,
                        help="file extension/type to copy (required)")
    parser.add_argument("-f", "--force", type=bool, required=False,
                        help="copy all files, overwriting identical-size "
                             "files (default: False)")
    parser.add_argument("-r", "--recursive", type=bool, required=False,
                        help="copy all files in specified directory tree "
                             "(default: False)")

    args = parser.parse_args()
    if args.source:
        DIRECTORY_SOURCE = args.source
    if args.destination:
        DIRECTORY_DESTINATION = args.destination
    if args.extension:
        EXTENSION_TO_COPY = args.extension
    if args.force:
        FORCE_COPY = args.force
    if args.recursive:
        RECURSIVE = args.recursive


"""Copy functionality"""


def _handle_copy():
    # Call to copy either just target directory or target directory recursively
    if RECURSIVE:
        _copy_filetype_recursive(Path(DIRECTORY_SOURCE),
                                 Path(DIRECTORY_DESTINATION),
                                 EXTENSION_TO_COPY)
    else:
        _copy_filetype(Path(DIRECTORY_SOURCE), Path(DIRECTORY_DESTINATION),
                       EXTENSION_TO_COPY)


def _copy_filetype(dir_source, dir_destination, filetype):
    # Copy only files in target directory
    glob_pattern = f"*{filetype}"
    os.makedirs(dir_destination, exist_ok=True)

    for file in dir_source.glob(glob_pattern):
        if Path(file).suffix == filetype:
            if _is_dest_copied_file_different(Path(dir_source), dir_destination,
                                              file):
                shutil.copy(Path(file), Path(dir_destination))


def _copy_filetype_recursive(dir_source, dir_destination, filetype):
    # Copy files in target directory and all children directories, recursively
    os.makedirs(dir_destination, exist_ok=True)

    for directory, sub_directories, files in os.walk(dir_source):
        for file in files:
            if Path(file).suffix == filetype:
                if _is_dest_copied_file_different(Path(directory),
                                                  dir_destination, file):
                    shutil.copy((Path(directory) / Path(file)),
                                Path(dir_destination))


"""Helpers"""


def _is_dest_copied_file_different(dir_source, dir_destination, file):
    # Return whether specified file at destination and source are different size
    if (Path(dir_destination) / Path(file)).is_file():
        return os.path.getsize(Path(dir_destination) / Path(file)) != \
               os.path.getsize(Path(dir_source) / Path(file))
    return True


def _delete_dir_if_empty(dir_dest):
    # Remove created destination directory if empty
    for _, _, files in os.walk(Path(dir_dest)):
        if not files:
            Path(dir_dest).rmdir()


def main():
    """Program entry point"""
    global DIRECTORY_DESTINATION
    _get_flag_arguments()
    _handle_copy()
    _delete_dir_if_empty(DIRECTORY_DESTINATION)


main()
