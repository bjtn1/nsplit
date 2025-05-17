# nsplitter.py

**Author:** Brandon Jose Tenorio Noguera  
**Email:** [nsplitter@bjtn.me](mailto:nsplitter@bjtn.me)

`nsplitter.py` is a command-line tool for splitting and merging large files — ideal for managing files on FAT32-formatted drives or any storage medium with size constraints (like a 4GB limit). It cleanly divides large files into 4GB chunks and can later reconstruct them with full fidelity.

---

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

# Table of Contents
   * [🔧 Features](#-features)
   * [📦 Installation](#-installation)
   * [🚀 Usage](#-usage)
      + [🔹 Splitting Files](#-splitting-files)
      + [🔹 Merging Files](#-merging-files)
   * [🧪 Dry Run Mode](#-dry-run-mode)
   * [🧹 Clean Up](#-clean-up)
   * [🔤 Arguments](#-arguments)
   * [🧠 Notes](#-notes)
   * [🛠️ Example Split Folder](#-example-split-folder)
   * [📝 License](#-license)

<!-- TOC end -->


<!-- TOC --><a name="-features"></a>
## 🔧 Features

- 🔹 **Split** files larger than 4GB into chunks.
- 🔹 **Merge** `.split.<ext>` folders back into the original file.
- 🔹 Supports **batch processing** via directory scanning.
- 🔹 **Recursive** directory search.
- 🔹 Optional **dry-run** mode (simulate actions).
- 🔹 Optionally **delete original files** after processing.
- 🔹 Clear progress messages and summary output.

---

<!-- TOC --><a name="-installation"></a>
## 📦 Installation

No installation needed. Just ensure you have Python 3.7+ installed.

```bash
python nsplitter.py [OPTIONS]
```

---

<!-- TOC --><a name="-usage"></a>
## 🚀 Usage

<!-- TOC --><a name="-splitting-files"></a>
### 🔹 Splitting Files

Split a large file into 4GB chunks:

```bash
python nsplitter.py --split FILE1 [FILE2 ...]
```

Split all `.nsp` files in a directory (non-recursive):

```bash
python nsplitter.py -s -d /path/to/files -e nsp
```

Recursively split all `.mp4` files in a folder:

```bash
python nsplitter.py -s -d ./videos -e mp4 -r
```

<!-- TOC --><a name="-merging-files"></a>
### 🔹 Merging Files

Merge previously split files (i.e., `.split.nsp` folder):

```bash
python nsplitter.py --merge FOLDER1 [FOLDER2 ...]
```

Or merge all `.split.nsp` folders in a directory:

```bash
python nsplitter.py -m -d /path/to/splits -e nsp
```

---

<!-- TOC --><a name="-dry-run-mode"></a>
## 🧪 Dry Run Mode

Preview what would happen **without modifying files**:

```bash
python nsplitter.py -s -d ./isos -e iso --dry-run
```

---

<!-- TOC --><a name="-clean-up"></a>
## 🧹 Clean Up

Delete the original file after splitting or merging:

```bash
python nsplitter.py -s FILE --clean
```

---

<!-- TOC --><a name="-arguments"></a>
## 🔤 Arguments

| Argument               | Description                                                        |
|------------------------|--------------------------------------------------------------------|
| `-s`, `--split`        | Split file(s) into 4GB chunks.                                     |
| `-m`, `--merge`        | Merge `.split.<ext>` folders back into a single file.              |
| `-d`, `--directory`    | Directory of files or folders to process.                          |
| `-e`, `--extension`    | File extension to match (e.g., `nsp`, `mp4`). Required with `-d`.  |
| `-r`, `--recursive`    | Recurse into subdirectories.                                       |
| `-c`, `--clean`        | Delete original files after splitting or merging.                  |
| `--dry-run`            | Simulate the process without modifying any files.                  |
| `files`                | Optional list of specific files or folders to process.             |

---

<!-- TOC --><a name="-notes"></a>
## 🧠 Notes

- Files smaller than 4GB will be skipped during splitting.
- Merged files are restored to the same directory as the `.split.<ext>` folder.
- The `.split.<ext>` folder must be named like `<filename>.split.<extension>` for merging to work correctly.

---

<!-- TOC --><a name="-example-split-folder"></a>
## 🛠️ Example Split Folder

If you split `game.nsp`, a folder named `game.split.nsp` will be created, containing:

```
game.split.nsp/
├── 00
├── 01
├── 02
└── ...
```

Merging this folder recreates `game.nsp`.

---

<!-- TOC --><a name="-license"></a>
## 📝 License

This project is released as-is, with no license currently applied.
