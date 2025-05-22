"""
@author: Brandon Jose Tenorio Noguera
@email: nsplitter@bjtn.me

Split algorithm inspired by https://github.com/AnalogMan151/splitNSP/blob/master/splitNSP.py
This program splits large files into small chunks. It's also capable of merging those files back together
Useful for archiving things into a FAT32 formatted drive or any drive with size limitations.
"""

import argparse
import math
import os
import shutil
import time
import re

THIRTY_TWO_KB = 0x8000 # 32,768 bytes
FOUR_GB = 0xFFFF0000 # 4,294,901,760 bytes
MAX_SPLIT_SIZE = 0xFFFF0000 # 4,294,901,760 bytes
FOUR_MB = 4 * 1024 * 1024


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
    elapsed = time.time() - start_time
    hours, remainder = divmod(int(elapsed), 3600)
    minutes, seconds = divmod(remainder, 60)
    # milliseconds = int((elapsed - int(elapsed)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def is_split_file(filepath: str) -> bool:
    """
    Returns True if the filename matches the pattern <name>.split.<ext>
    """
    filename = os.path.basename(filepath[:-1])
    # Match: anything + ".split." + extension
    return bool(re.match(r'^.+\.split\.[^.]+$', filename))


def merge_file(folderpath: str, dry_run: bool = False, buf_size: int = FOUR_MB) -> str:
    """
    Merges a <filename>.split.<extension> file back into a <filename>.<extension> file.
    
    Args:
        folderpath (str): Path to the split folder to be merged.
        dry_run (bool): If True, simulate the merge without writing files.
    
    Returns:
        str: Path to the newly merged file.
    """

    if not is_split_file(folderpath):
        print(f"❌ {os.path.basename(folderpath)} is not a split file")
        return ""

    merged_filename = os.path.basename(folderpath).replace(".split", "")
    merged_filename_path = os.path.abspath(os.path.join(os.path.dirname(folderpath), merged_filename))

    # this ensures the files will be in order when they get merged
    part_files = sorted(
        [os.path.abspath(os.path.join(folderpath, fname)) for fname in os.listdir(folderpath)],
        key=lambda f: int(os.path.basename(f))
    )

    print_banner(f"MERGING {os.path.basename(folderpath)}")

    start_time = time.time()

    with open(merged_filename_path, "wb") as outfile:
        for part in part_files:
            print(f"ℹ️ Merging part {os.path.basename(part)}...")

            if not dry_run:
                with open(part, "rb") as infile:
                    shutil.copyfileobj(infile, outfile, length=buf_size)

    print(f"⏳ Merge took {format_elapsed_time(start_time)}")
    print(f"\n✅ {merged_filename_path} successfully merged")

    shutil.rmtree(folderpath)

    return f"{merged_filename_path}"


def split_file(filepath: str, buf_size: int = THIRTY_TWO_KB, dry_run: bool = False, clean: bool = False) -> str:
    """
    Splits a large file into multiple 4GB chunks and stores them in a dedicated split directory.

    The output files are named numerically (e.g., 00, 01, 02...) and stored in a new directory
    located next to the original file, named <filename>.split. The original file is deleted
    after splitting is completed.

    Args:
        filepath (str): The full path to the file to be split.
        bufsize  (int): The size of the buffer where we store bytes to be read and written

    Returns:
        str: Path of the newly created split directory
    """

    filesize: int = os.path.getsize(filepath)

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
    split_dir = os.path.abspath(os.path.join(parent_dir, f"{filename_without_extension}.split.{file_extension}"))
    os.makedirs(split_dir, exist_ok=True)

    print_banner(f"SPLITTING {filename}")

    # open file in read-binary mode
    with open(filepath, "rb") as infile:
        # run this loop for as many splits as will be needed for this specific file
        for split in range(num_splits):
            # create and name the split file {filename}/{nn} where nn is the split number beginnign at 00
            split_path = os.path.join(split_dir, f"{split:02}")

            start_time = time.time()
            last_printed_seconds = -1

            if not dry_run:
                # begin loop to write to the newly created split file
                with open(split_path, "wb") as outfile:
                    bytes_written = 0
                    # each split will be 4,294,901,760 bytes
                    while bytes_written < (MAX_SPLIT_SIZE):

                        # timer display
                        elapsed_seconds = int(time.time() - start_time)
                        if elapsed_seconds != last_printed_seconds:
                            print(f"ℹ️ Splitting part {split:02}... Elapsed: {format_elapsed_time(start_time)}", end="\r")
                            last_printed_seconds = elapsed_seconds

                        # read the input file (file to be split) in chunks of 32KB 
                        chunk = infile.read(buf_size)
                        # if there is no more bytes to be read, break out of the loop
                        if not chunk:
                            break
                        # write the 32KB chunk we just read fromn the infile to the outfile
                        outfile.write(chunk)
                        # increment loop-stopping condition
                        bytes_written += len(chunk)
            # flush a clean line. part of timer display
            print()

    if clean:
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
    collected_files = []

    for root, dirs, files in os.walk(directory):
        if split:
            for file in files:
                if file.endswith(f".{extension}"):
                    path = os.path.join(root, file)
                    if not is_split_file(path):
                        collected_files.append(path)
        else:
            for dir in dirs:
                path = os.path.join(root, dir)
                if is_split_file(path):
                    collected_files.append(path)

        if not recursive:
            break

    return collected_files


def main() -> None:
    parser = argparse.ArgumentParser()

    # we do mutually-exclusive group because we expect either a directory to be searched, or a series of 1 or more files to be split
    # splitting and merging are mutually-exclusive
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-s", "--split", action="store_true", help="Split files")
    mode.add_argument("-m", "--merge", action="store_true", help="Merge split folders")

    parser.add_argument("-d", "--directory", help="Directory of files to split or merge")
    parser.add_argument("-e", "--extension", help="File extension to process (e.g., nsp, mp4)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process files in directories")
    parser.add_argument("files", nargs="*", help="Optional list of specific file paths to split/merge")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the operations without modifying files")

    args = parser.parse_args()

    if not args.split and not args.merge:
        exit("❌ One of -s/--split or -m/--merge option is required")

    extension = None

    files = args.files or []
    split_filenames: list[str] = []
    merge_filenames: list[str] = []

    if args.directory and not args.extension:
            exit("❌ -e/--extension is required when using -d/--directory.")

    if args.directory:
        extension = args.extension.lstrip(".")
        to_split_or_not_to_split = bool(args.split)
        files.extend(collect_files(args.directory, extension, args.recursive, split=to_split_or_not_to_split))

    if not files:
        print("❌ No files found to process.")
        return

    start_time: float = time.time()
    split_count: int = 0
    merge_count: int = 0

    for filepath in files:
        if args.split and not os.path.isfile(filepath):
            # print(f"❌ File not found: {filepath}")
            continue

        elif args.merge and not is_split_file(filepath):
            # print(f"❌ File not found: {filepath}")
            continue

        file_extension = os.path.splitext(filepath)[1].lstrip(".")
        if args.directory and file_extension != extension:
            # print(f"⏭️ Skipping {os.path.basename(filepath)}: Extension mismatch.")
            continue

        if args.split and os.path.getsize(filepath) <= FOUR_GB:
            # print(f"⏭️ Skipping {os.path.basename(filepath)}: File size under 4GB.")
            continue

        # this checks that there;s enough storage on disk for the splitting process to take place
        if args.split and os.path.getsize(filepath) > shutil.disk_usage(filepath).free:
            print(f"⏭️ Skipping {filepath}: Insufficient storage space.")
            continue

        if args.split:
            full_path = os.path.abspath(filepath)

            split_filenames.append(split_file(filepath, dry_run=args.dry_run))

            split_count += 1

        elif args.merge:
            full_path = os.path.abspath(filepath)
            normalized_path = os.path.normpath(full_path)

            merge_filenames.append(merge_file(normalized_path, dry_run=args.dry_run))

            merge_count += 1

    elapsed_time = format_elapsed_time(start_time)

    if args.split:
        print_banner("SUMMARY")
        for name in sorted(split_filenames):
            print(f"✅ {name}")
        print(f"\nSplit {split_count} files in {elapsed_time}")
    elif args.merge:
        print_banner("SUMMARY")
        for name in sorted(merge_filenames):
            print(f"✅ {name}")
        print(f"\nMerged {merge_count} files in {elapsed_time}")


if __name__ == "__main__":
    print()
    main()
