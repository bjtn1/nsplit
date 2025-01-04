import argparse
import math
import os
import shutil
import time

ONE_MB = 2**20
FOUR_GB = 4 * 2**30
CHECKMARK = u'\u2705'


def format_elapsed_time(start_time):
    """
    Formats the elapsed time since `start_time`.
    """
    elapsed_seconds = time.time() - start_time
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_seconds))


def split_file(filepath, filename, filesize):
    """
    Splits a file into 4GB chunks.
    """
    num_splits = math.ceil(filesize / FOUR_GB)
    parent_dir = os.path.dirname(filepath)
    split_dir = os.path.join(parent_dir, f"{filename}.split")
    os.makedirs(split_dir, exist_ok=True)

    start_time = time.time()
    total_bytes_written = 0

    with open(filepath, "rb") as infile:
        for split in range(num_splits):
            split_path = os.path.join(split_dir, f"{split:02}")
            with open(split_path, "wb") as outfile:
                bytes_written = 0
                while bytes_written < FOUR_GB:
                    chunk = infile.read(ONE_MB)
                    if not chunk:
                        break
                    outfile.write(chunk)
                    bytes_written += len(chunk)
                    total_bytes_written += len(chunk)

            elapsed_time = format_elapsed_time(start_time)
            progress = total_bytes_written / filesize
            print(
                f"[{elapsed_time}] [{split + 1}/{num_splits}] "
                f"[{progress:.2%}] {total_bytes_written:_}/{filesize:_} bytes",
                end="\r" if total_bytes_written < filesize else "\n",
            )

    os.remove(filepath)
    # print(f"{CHECKMARK} Split complete: {filename}")


def collect_files(directory, extension, recursive):
    """
    Collects files with the given extension from a directory.
    """
    collected_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                collected_files.append(os.path.join(root, file))
        if not recursive:
            break
    return collected_files


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="Directory of files to split")
    group.add_argument("-f", "--files", nargs="+", help="Specific files to split")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process files in directories")
    parser.add_argument("-e", "--extension", required=True, help="File extension to process (e.g., .mp4)")
    args = parser.parse_args()

    extension = args.extension.lstrip(".")
    files = args.files or []
    if args.directory:
        files.extend(collect_files(args.directory, extension, args.recursive))

    if not files:
        print("No files found to process.")
        return

    start_time = time.time()
    split_count = 0

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

        available_storage = shutil.disk_usage(filepath).free
        if filesize > available_storage:
            print(f"Skipping {filepath}: Insufficient storage space.")
            continue

        filename = os.path.basename(filepath)
        split_file(filepath, filename, filesize)
        split_count += 1

    elapsed_time = format_elapsed_time(start_time)
    print(f"\nProcessed {split_count} files in {elapsed_time}.")


if __name__ == "__main__":
    main()
