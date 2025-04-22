
<!-- TOC --><a name="-nsplitter"></a>
# 🪓 nsplitter

**nsplitter** is a Python-based command-line tool that efficiently splits large files into 4GB chunks — perfect for backup, archiving, or transferring large media and binary files on platforms with size limitations (such as FAT32 formatted drives).

---

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

* [🚀 Features](#-features)
* [📦 Installation](#-installation)
* [🛠️ Usage](#-usage)
    + [Split specific files:](#split-specific-files)
    + [Split all matching files in a directory:](#split-all-matching-files-in-a-directory)
    + [Options](#options)
* [💡 Examples](#-examples)
* [📁 Output Structure](#-output-structure)
* [🧪 Running Tests](#-running-tests)
* [📄 License](#-license)
* [👨‍💻 Author](#-author)
* [✨ Contributing](#-contributing)

<!-- TOC end -->

---

<!-- TOC --><a name="-features"></a>
## 🚀 Features

- 🔹 Splits files into 4GB chunks
- 🔹 Supports individual files or entire directories
- 🔹 Optional recursive search for nested folders
- 🔹 Deletes original file after splitting to save space
- 🔹 Simple CLI with live progress display
- 🔹 Pure Python, no external dependencies

---

<!-- TOC --><a name="-installation"></a>
## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/bjtn1/nsplitter.git
cd nsplitter
```

Run it with:

```bash
python src/main.py ...
```

> ✅ Requires Python 3.8 or higher

---

<!-- TOC --><a name="-usage"></a>
## 🛠️ Usage

<!-- TOC --><a name="split-specific-files"></a>
### Split specific files:

```bash
python src/main.py -f file1.mp4 file2.mp4
```


> ⚠️ The -e/--extension flag is not required when using -f/--files.

<!-- TOC --><a name="split-all-matching-files-in-a-directory"></a>
### Split all matching files in a directory:

```bash
python src/main.py -d /path/to/files -e mp4
```
> ⚠️ The -e/--extension flag IS required when using -d/--directory.

<!-- TOC --><a name="options"></a>
### Options

| Flag | Description |
|------|-------------|
| `-f, --files`      | One or more specific files to split |
| `-d, --directory`  | Path to directory of files to split |
| `-e, --extension`  | File extension to match (e.g. `mp4`) |
| `-r, --recursive`  | Recursively include files in subdirectories |

---

<!-- TOC --><a name="-examples"></a>
## 💡 Examples

**Split all `.mkv` files in `/videos` recursively:**

```bash
python main.py -d /videos -e mkv -r
```

**Split specific files:**

```bash
python main.py -f movie.mkv backup.img -e mkv
```

---

<!-- TOC --><a name="-output-structure"></a>
## 📁 Output Structure

After splitting, a new directory `<filename>.split/` is created next to the original file:

```
📁 movie.mkv.split/
├── 00
├── 01
├── 02
...
```

⚠️ The original file is **deleted** once the split is complete.

---

<!-- TOC --><a name="-running-tests"></a>
## 🧪 Running Tests

```bash
python -m unittest test_nsplitter.py
```

---

<!-- TOC --><a name="-license"></a>
## 📄 License

This project is licensed under the [MIT License](https://github.com/bjtn1/nsplitter?tab=MIT-1-ov-file).

---

<!-- TOC --><a name="-author"></a>
## 👨‍💻 Author

**Brandon Jose Tenorio Noguera**  
📧 nsplitter@bjtn.me  
🌐 [bjtn.me](https://bjtn.me)  
🔗 [LinkedIn](https://www.linkedin.com/in/brandon-jose-tenorio-noguera/)

---

<!-- TOC --><a name="-contributing"></a>
## ✨ Contributing

Pull requests are welcome! Feel free to open an issue or submit a feature suggestion.

