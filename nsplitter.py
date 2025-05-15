"""
@author: Brandon Jose Tenorio Noguera
@email: nsplitter@bjtn.me

This program splits large files into small chunks. It's also capable of merging those files back together
Useful for archiving things into a FAT32 formatted drive or any drive with size limitations
"""

import argparse
import os
import shutil
import time
import math
import os
import time
import re

ONE_KB = 2**10
THIRTY_TWO_KB = 32 * ONE_KB
SIXTY_FOUR_KB = 64 * ONE_KB
ONE_MB = 2**20
FOUR_GB = 4 * 2**30
MAX_SPLIT_SIZE = FOUR_GB - SIXTY_FOUR_KB


def print_banner(msg: str) -> None:
    banner = f"== {msg} =="
    border = "=" * len(banner)
    print(f"\n{border}\n{banner}\n{border}")


def format_elapsed_time(start_time: float) -> str:
    """
    Returns the formatted elapsed time since the given start time.

    Args:
        start_time (float): The starting time in seconds since the epoch (as returned by time.time()).

    Returns:
        str: Elapsed time formatted as "HH:MM:SS".
    """
    elapsed_seconds = time.time() - start_time
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_seconds))


def is_split_file(filepath: str) -> bool:
    """
    Returns True if the filename matches the pattern <name>.split.<ext>
    """
    filename = os.path.basename(filepath[:-1])
    # Match: anything + ".split." + extension
    return bool(re.match(r'^.+\.split\.[^.]+$', filename))


def merge_file(folderpath: str) -> str:
    """
    Merges a <filename>.split.<extension> file back into a <filename>.<extension> file
    """

    if not is_split_file(folderpath):
        print(f"❌ {os.path.basename(folderpath)} is not a split file")
        return ""

    merged_filename = os.path.basename(folderpath).replace(".split", "")

    merged_filename_path = os.path.abspath(os.path.join(os.path.dirname(folderpath), merged_filename))

    part_files = [
        os.path.abspath(os.path.join(folderpath, fname))
        for fname in os.listdir(folderpath)
    ]

    print_banner(f"MERGING {os.path.basename(folderpath)}")

    with open(merged_filename_path, "wb") as outfile:
        for i, part in enumerate(part_files):
            print(f"ℹ️ Merging part {i:02}...")
            with open(part, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    # shutil.rmtree(os.path.abspath(folderpath))

    print(f"✅ {merged_filename_path} successfully merged")

    return f"{merged_filename_path}"


def split_file(filepath: str, filesize: int, buf_size: int = THIRTY_TWO_KB) -> str:
    """
    Splits a large file into multiple 4GB chunks and stores them in a dedicated split directory.

    The output files are named numerically (e.g., 00, 01, 02...) and stored in a new directory
    located next to the original file, named <filename>.split. The original file is deleted
    after splitting is completed.

    Args:
        filepath (str): The full path to the file to be split.
        filesize (int): The size of the file in bytes.
        bufsize  (int): The size of the buffer where we store bytes to be read and written

    Returns:
        str: Path of the newly created split directory
    """

    # get the name of the file from the filepath
    filename: str = os.path.basename(filepath)

    # calculate how many splits we're gonna create for this file
    # use math.ceil to in case filesize is not perfectly divisible by 4GB
    num_splits = math.ceil(filesize / MAX_SPLIT_SIZE)

    # get the name of the directory where this file is located
    # so that we know where to put the split files
    parent_dir = os.path.dirname(filepath)

    # creates a file named <filename>.split.<file_extension>
    file_extension = os.path.splitext(filepath)[1].lstrip(".")
    filename_without_extension = os.path.splitext(os.path.basename(filepath))[0]
    split_dir = os.path.join(parent_dir, f"{filename_without_extension}.split.{file_extension}")
    os.makedirs(split_dir, exist_ok=True)

    print_banner(f"SPLITTING {filename}")

    start_time = time.time()

    # needed for progress report
    total_bytes_written = 0

    # open file in read-binary mode
    with open(filepath, "rb") as infile:
        # run this loop for as many splits as will be needed for this specific file
        for split in range(num_splits):
            # create and name the split file {filename}/{nn} where nn is the split number beginnign at 00
            split_path = os.path.join(split_dir, f"{split:02}")
            # begin loop to write to the newly created split file
            with open(split_path, "wb") as outfile:
                bytes_written = 0
                # each split must be 4GB - 64KB long
                while bytes_written < (MAX_SPLIT_SIZE):
                    # read the input file (file to be split) in chunks of 32KB 
                    chunk = infile.read(buf_size)
                    # if there is no more bytes to be read, break out of the loop
                    if not chunk:
                        break
                    # write the 32KB chunk we just read fromn the infile to the outfile
                    outfile.write(chunk)
                    # increment loop-stopping condition
                    bytes_written += len(chunk)
                    # this is just a fun metric to display once the process has finished
                    total_bytes_written += len(chunk)

            elapsed_time = format_elapsed_time(start_time)
            # get the progress of the splitting process for every file after each split
            progress = total_bytes_written / filesize
            # print report for each split
            print(
                f"[{elapsed_time}] [{split + 1}/{num_splits}] "
                f"[{progress:.2%}] {total_bytes_written:_}/{filesize:_} bytes | {filename}",
                end="\r" if total_bytes_written < filesize else "\n",
            )

    # remove the file that was just split
    os.remove(filepath)

    print(f"✅ {split_dir} successfully split")
    # return the path of the newly created .split directory
    return split_dir


def collect_files(directory: str, extension: str, recursive: bool, split: bool) -> list[str]:
    """
    Collects all files with a given extension from a directory.

    Args:
        directory (str): Path to the directory to search.
        extension (str): File extension to match (e.g., ".mp4").
        recursive (bool): Whether to search subdirectories recursively.
        split     (bool): Whether we are collecting files to split them or merge them

    Returns:
        list[str]: A list of file paths matching the given extension.
    """
    collected_files: list[str] = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                # only collect split files if we're merging
                if not split and is_split_file(full_path):
                    collected_files.append(full_path)
                # only collect full files (as opposed to split files) if we're splitting
                elif split and not is_split_file(full_path):
                    collected_files.append(full_path)
        if not recursive:
            break

    return collected_files


def main() -> None:
    parser = argparse.ArgumentParser()

    # we do mutually-exclusive group because we expect either a directory to be searched, or a series of 1 or more files to be split
    # splitting and merging are mutually-exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="Directory of files to split or merge (non-inclusive)")
    group.add_argument("-f", "--files", nargs="+", help="Specific files to split")

    group.add_argument("-s", "--split", nargs="+", help="Specific files to split")
    group.add_argument("-m", "--merge", nargs="+", help="Path to split folder to merge back into a file")

    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process files in directories")
    parser.add_argument("-e", "--extension", help="File extension to process (e.g., mp4, no dot) — required if using --directory")

    args = parser.parse_args()

    # this is an array where we'll save the files that the user wants to split or merge
    files: list[str] = args.files or []

    if args.split:
        # extension flag should only be required when directory flag is present
        if args.directory and not args.extension:
            parser.error("❌ --extension is required when using --directory.")

        if args.directory:
            extension = args.extension.lstrip(".")
            files.extend(collect_files(args.directory, extension, args.recursive, split=True))

        if not files:
            print("❌ No files found to split.")
            return

        start_time: float = time.time()
        split_count: int = 0

        for filepath in files:
            if not os.path.isfile(filepath):
                print(f"❌ File not found: {filepath}")
                continue

            file_extension = os.path.splitext(filepath)[1].lstrip(".")
            if args.directory and file_extension != extension:
                print(f"❌ Skipping {filepath}: Extension mismatch.")
                continue

            filesize = os.path.getsize(filepath)
            if filesize <= FOUR_GB:
                print(f"❌ Skipping {filepath}: File size under 4GB.")
                continue

            # this checks that there;s enough storage on disk for the splitting process to take place
            available_storage = shutil.disk_usage(filepath).free
            if filesize > available_storage:
                print(f"❌ Skipping {filepath}: Insufficient storage space.")
                continue

            # split_file(filepath, filesize)

            split_count += 1

        elapsed_time = format_elapsed_time(start_time)
        print(f"\n✅ Split {split_count} files in {elapsed_time}.")
        

    if args.merge:
        # extension flag should only be required when directory flag is present
        if args.directory and not args.extension:
            parser.error("❌ --extension is required when using --directory.")

        if args.directory:
            extension = args.extension.lstrip(".")
            files.extend(collect_files(args.directory, extension, args.recursive, split=False))

        if not files:
            print("❌ No files found to split.")
            return

        start_time: float = time.time()
        merge_count: int = 0

        for filepath in files:
            if not os.path.isfile(filepath):
                print(f"❌ File not found: {filepath}")
                continue

            file_extension = os.path.splitext(filepath)[1].lstrip(".")
            if args.directory and file_extension != extension:
                print(f"❌ Skipping {filepath}: Extension mismatch.")
                continue

            filesize = os.path.getsize(filepath)
            if filesize <= FOUR_GB:
                print(f"❌ Skipping {filepath}: File size under 4GB.")
                continue

            # this checks that there;s enough storage on disk for the splitting process to take place
            available_storage = shutil.disk_usage(filepath).free
            if filesize > available_storage:
                print(f"❌ Skipping {filepath}: Insufficient storage space.")
                continue

            # merge_file(filepath)

            merge_count += 1

        elapsed_time = format_elapsed_time(start_time)
        print(f"\n✅ Merged {merge_count} files in {elapsed_time}.")


if __name__ == "__main__":
    # merge_split_file("../TEST/Animal Crossing New Horizons [01006F8002326000][US][v0].split.nsp")
    main()
