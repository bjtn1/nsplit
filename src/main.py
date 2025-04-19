"""
@author: Brandon Jose Tenorio Noguera
@email: nsplitter@bjtn.me

Contains the logic to interact with the nsplitter CLI
"""

import argparse
import os
import shutil
import time
from core import split_file, collect_files, format_elapsed_time, FOUR_GB


def main() -> None:
    parser = argparse.ArgumentParser()

    # we do mutually-exclusive group because we expect either a directory to be searched, or a series of 1 or more files to be split
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="Directory of files to split")
    group.add_argument("-f", "--files", nargs="+", help="Specific files to split")

    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process files in directories")
    parser.add_argument("-e", "--extension", required=True, help="File extension to process (e.g., .mp4)")
    args = parser.parse_args()

    extension = args.extension.lstrip(".")
    # this is an array where we'll save the files that the user wants to split
    files: list[str] = args.files or []

    if args.directory:
        files.extend(collect_files(args.directory, extension, args.recursive))

    if not files:
        print("No files found to process.")
        return

    start_time: float = time.time()
    split_count: int = 0

    for filepath in files:
        if not os.path.isfile(filepath):
            print(f"File not found: {filepath}")
            continue

        file_extension = os.path.splitext(filepath)[1].lstrip(".")
        if file_extension != extension:
            print(f"Skipping {filepath}: Extension mismatch.")
            continue

        filesize = os.path.getsize(filepath)
        if filesize <= FOUR_GB:
            print(f"Skipping {filepath}: File size under 4GB.")
            continue

        # this checks that there;s enough storage on disk for the splitting process to take place
        available_storage = shutil.disk_usage(filepath).free
        if filesize > available_storage:
            print(f"Skipping {filepath}: Insufficient storage space.")
            continue

        split_file(filepath, filesize)
        split_count += 1

    elapsed_time = format_elapsed_time(start_time)
    print(f"\nProcessed {split_count} files in {elapsed_time}.")

if __name__ == "__main__":
    main()
