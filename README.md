# Copy Files

Copy files of a specified extension from a source to destination.

## Overview

- Execute `python3 copy_files.py -h` for help
- Copy files of specified extension from `source` to `destination` directory
- `-r` flag to recursively copy, i.e., copy files of specified extension from `source` directory tree -including all 
  matching file types in all child directories
- `-f` flag to force copy files (by default files of the same name and size are not copied again, saving time for 
  copying, e.g., large media files)

## Examples

- `python3 copy_files.py ./ ../backups -e .txt`: copy all `.txt` files in the current present/current working directory 
  (only) to a parent `backups` directory
- `python3 copy_files.py ~/Documents ./copy-test -e .pdf`: copy all `.pdf` files in the current user's `Documents` 
  directory tree (i.e., including all sub-directories) to a `copy-test` directory in the current present/current 
  working directory.
- `python3 copy_files.py ./ ../backups -e .txt -f True`: force copy all `.txt` files in the current present/current 
  working directory (only) to a parent `backups` directory 
