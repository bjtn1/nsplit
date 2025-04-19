"""
@author: Brandon Jose Tenorio Noguera
@email: nsplitter@bjtn.me
"""

import os
import tempfile
import unittest
import hashlib
from pathlib import Path
from core import format_elapsed_time, collect_files, split_file, ONE_MB, FOUR_GB

# TODO
# should I add a setUp and tearDown method?

class TestNSplitter(unittest.TestCase):
    def test_format_elapsed_time(self):
        import time
        start = time.time() - 3661
        self.assertEqual(format_elapsed_time(start), "01:01:01")

    def test_collect_files_non_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "video1.mp4"
            file2 = Path(tmpdir) / "video2.txt"
            file1.write_text("dummy")
            file2.write_text("dummy")
            collected = collect_files(tmpdir, ".mp4", recursive=False)
            self.assertIn(str(file1), collected)
            self.assertNotIn(str(file2), collected)

    def test_collect_files_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "sub"
            subdir.mkdir()
            file1 = subdir / "video1.mp4"
            file1.write_text("dummy")
            collected = collect_files(tmpdir, ".mp4", recursive=True)
            self.assertIn(str(file1), collected)

    def test_split_file_creates_chunks(self):
        """
        Checks that chunk files were created. DOES NOT check for integrity
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "bigfile.dat"
            test_filesize = FOUR_GB + ONE_MB
            with open(test_file, "wb") as f:
                f.write(os.urandom(test_filesize))

            split_dir = split_file(str(test_file), os.path.getsize(test_file))


            # check that the <filename>.split directory was properly created
            self.assertTrue(os.path.exists(split_dir))

            # this retrieves all files in this split directory
            parts = [file for file in os.listdir(split_dir) if os.path.isfile(os.path.join(split_dir, file))]

            # check that the directory has exactly filesize / FOUR_GB parts
            expected_parts = test_filesize / FOUR_GB
            self.assertGreaterEqual(len(parts), expected_parts)

            # test_file should be deleted after split_file is called on it
            self.assertFalse(test_file.exists())

    # TODO
    # I might want to make this more akin to like a for loop in case I wanna test a file with more than 2 split parts
    def test_split_file_integrity(self):
        """
        Checks the integrity of split_file

        1) create a tmp file >= 4GB
        2) get the md5 hex digest of the 1st 4GB of tmp file
        3) get the md5 hex digest of the nth split of tmp file
        3) split tmp file
        4) get the md5 hex digest of the split files (e.g., 00, 01, 02, etc..)
        5) compare hex digests between steps 2-3 and 5
        """
        og_tmp_file_md5 = hashlib.md5()
        split_tmp_file_md5 = hashlib.md5()

        # create tmp dir
        with tempfile.TemporaryDirectory() as tmpdir:
            # create tmp file
            tmp_file = Path(tmpdir) / "integrity_file_test.dat"

            # create arbitrary size for tmp file
            tmp_filesize = FOUR_GB + ONE_MB

            # write random bytes to tmp file
            with open(tmp_file, "wb") as f:
                f.write(os.urandom(tmp_filesize))


            # get the md5 hex digest of the 1st 4GB of tmp file
            with open(tmp_file, "rb") as f:
                # read the first 4gb of tmp file
                og_tmp_file_data = f.read(FOUR_GB)
                og_tmp_file_md5.update(og_tmp_file_data)

            og_tmp_file_md5_hex_digest = og_tmp_file_md5.hexdigest()

            # split tmp file
            split_dir = split_file(str(tmp_file), tmp_filesize)

            # this retrieves all the full path of all files in this split directory
            parts = [
                os.path.join(split_dir, file)
                for file in os.listdir(split_dir)
                if os.path.isfile(os.path.join(split_dir, file))
            ]
            
            # get the md5 hex digest of the first file (00) in the split directory
            with open(parts[0], "rb") as f:
                # read the whole file (should be 4GB)
                split_tmp_file_data = f.read()
                split_tmp_file_md5.update(split_tmp_file_data)

            split_tmp_file_md5_hex_digest = split_tmp_file_md5.hexdigest()

            # now compare og md5 with split md5
            self.assertEqual(og_tmp_file_md5_hex_digest, split_tmp_file_md5_hex_digest)
            



if __name__ == '__main__':
    unittest.main()
