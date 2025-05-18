<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->
# nsplitter

**Author:** Brandon Jose Tenorio Noguera  
**Email:** [nsplitter@bjtn.me](mailto:nsplitter@bjtn.me)

`nsplitter` is a command-line utility that splits large files into 4GB chunks and merges them back again. It's especially useful for transferring files to FAT32 drives or other filesystems with size limits.

---

* [🔧 Features](#-features)
* [💻 Requirements](#-requirements)
* [📦 Installation](#-installation)
* [🚀 Usage](#-usage)
  + [Split files](#split-files)
  + [Merge files](#merge-files)
  + [Split all `.nsp` files in a directory (non-recursive)](#split-all-nsp-files-in-a-directory-non-recursive)
  + [Merge recursively and clean up after](#merge-recursively-and-clean-up-after)
* [🔤 Options](#-options)
* [📁 Output Structure](#-output-structure)
* [🧪 Example](#-example)
* [🛠 How It Works](#-how-it-works)
* [⚠️ Notes](#-notes)
* [📝 License](#-license)
* [📫 Contact](#-contact)

<!-- TOC end -->

---

<!-- TOC --><a name="-features"></a>
## 🔧 Features

- Split large files into `4GB - 64KB` chunks
- Merge `.split.*` directories back into original files
- Supports dry runs to simulate actions without writing to disk
- Cleans up original files or directories after processing (optional)
- Works recursively on directories
- Supports extension filtering

---

<!-- TOC --><a name="-requirements"></a>
## 💻 Requirements

- Python 3.7 or higher

---

<!-- TOC --><a name="-installation"></a>
## 📦 Installation

No installation needed. Just download or clone the repository and run the script directly:

```bash
python nsplitter.py [OPTIONS]
```

---

<!-- TOC --><a name="-usage"></a>
## 🚀 Usage

<!-- TOC --><a name="split-files"></a>
### Split files

```bash
python nsplitter.py --split FILE1 FILE2 ...
```

<!-- TOC --><a name="merge-files"></a>
### Merge files

```bash
python nsplitter.py --merge FOLDER1 FOLDER2 ...
```

<!-- TOC --><a name="split-all-nsp-files-in-a-directory-non-recursive"></a>
### Split all `.nsp` files in a directory (non-recursive)

```bash
python nsplitter.py -s -d /path/to/dir -e nsp
```

<!-- TOC --><a name="merge-recursively-and-clean-up-after"></a>
### Merge recursively and clean up after

```bash
python nsplitter.py -m -d /path/to/dir -e nsp -r -c
```

---

<!-- TOC --><a name="-options"></a>
## 🔤 Options

| Option            | Description |
|-------------------|-------------|
| `-s`, `--split`   | Split mode (mutually exclusive with merge) |
| `-m`, `--merge`   | Merge mode (mutually exclusive with split) |
| `-d`, `--directory DIR` | Directory to scan for files/folders |
| `-e`, `--extension EXT` | File extension to filter (required with `-d`) |
| `-r`, `--recursive`     | Recursively scan subdirectories |
| `-c`, `--clean`         | Delete original file (when splitting) or folder (when merging) |
| `--dry-run`             | Simulate the operation without making changes |
| `files`                 | List of individual files or folders to process |

---

<!-- TOC --><a name="-output-structure"></a>
## 📁 Output Structure

For a file like `game.nsp`, the split output will be:

```
game.split.nsp/
├── 00
├── 01
├── ...
```

The merged result will recreate `game.nsp` in the same directory.

---

<!-- TOC --><a name="-example"></a>
## 🧪 Example

```bash
python nsplitter.py -s my_game.nsp
# Output: my_game.split.nsp/00, 01, ...
```

```bash
python nsplitter.py -m my_game.split.nsp
# Output: my_game.nsp
```

---

<!-- TOC --><a name="-how-it-works"></a>
## 🛠 How It Works

- **Split**: Reads the input file in chunks (default 32KB buffer) and writes up to ~4GB per part.
- **Merge**: Reassembles the chunks in numeric order into a single file.
- **Timers**: Elapsed time is printed for each split/merge operation for visibility.

---

<!-- TOC --><a name="-notes"></a>
## ⚠️ Notes

- FAT32 has a 4GB file size limit. This tool creates splits that comply with this constraint.
- Ensure you have enough free disk space when splitting files.
- Original files/folders can be removed automatically with `--clean`.

---

<!-- TOC --><a name="-license"></a>
## 📝 License

MIT License

---

<!-- TOC --><a name="-contact"></a>
## 📫 Contact

For bugs, questions, or suggestions, email [nsplitter@bjtn.me](mailto:nsplitter@bjtn.me) or open an issue
