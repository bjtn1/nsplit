"""
@author: Brandon Jose Tenorio Noguera
@email: nsplitter@bjtn.me

Contains the core functions and logic needed for the nsplitter CLI to work such as (but not limited to):
- collect_files(directory, extension, recursive)
- split_file(filepath, filename, filesize)
- format_elapsed_time(start_time)
"""

import math
import os
import shutil
import time

ONE_MB = 2**20
FOUR_GB = 4 * 2**30
CHECKMARK = u'\u2705'

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


def split_file(filepath: str, filename: str, filesize: int) -> None:
    """
    Splits a large file into multiple 4GB chunks and stores them in a dedicated split directory.

    The output files are named numerically (e.g., 00, 01, 02...) and stored in a new directory
    located next to the original file, named <filename>.split. The original file is deleted
    after splitting is completed.

    Args:
        filepath (str): The full path to the file to be split.
        filename (str): The base name of the file.
        filesize (int): The size of the file in bytes.
    """

    # calculate how many splits we're gonna create for this file
    # use math.ceil to in case filesize is not perfectly divisible by 4GB
    num_splits = math.ceil(filesize / FOUR_GB)

    # get the name of the directory where this file is located
    # so that we know where to put the split files
    parent_dir = os.path.dirname(filepath)

    # creates a file named <filename>.split
    split_dir = os.path.join(parent_dir, f"{filename}.split")
    os.makedirs(split_dir, exist_ok=True)

    start_time = time.time()

    # needed for progress report what is this for?
    total_bytes_written = 0

    # open file in read-binary mode
    with open(filepath, "rb") as infile:
        # run this loop for as many splits as will be needed for this specific file
        for split in range(num_splits):
            # create and name the split file {filename}/{nn} where `nn` is the split number beginnign at `00`
            split_path = os.path.join(split_dir, f"{split:02}")
            # begin loop to write to the newly created split file
            with open(split_path, "wb") as outfile:
                bytes_written = 0
                # each split must be 4GB long
                while bytes_written < FOUR_GB:
                    # read the input file (file to be split) in chunks of 1MB 
                    chunk = infile.read(ONE_MB)
                    # if there is no more bytes to be read, break out of the loop
                    if not chunk:
                        break
                    # write the 1MB chunk we just read fromn the infile to the outfile
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
                f"[{progress:.2%}] {total_bytes_written:_}/{filesize:_} bytes",
                end="\r" if total_bytes_written < filesize else "\n",
            )

    # remove the file that was just  split
    os.remove(filepath)


def collect_files(directory: str, extension: str, recursive: bool) -> list[str]:
    """
    Collects all files with a given extension from a directory.

    Args:
        directory (str): Path to the directory to search.
        extension (str): File extension to match (e.g., ".mp4").
        recursive (bool): Whether to search subdirectories recursively.

    Returns:
        list[str]: A list of file paths matching the given extension.
    """
    collected_files: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                collected_files.append(os.path.join(root, file))
        if not recursive:
            break
    return collected_files
