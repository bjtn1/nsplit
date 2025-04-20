# 🪓 nsplitter

**nsplitter** is a Python-based command-line tool that efficiently splits large files into 4GB chunks — perfect for backup, archiving, or transferring large media and binary files on platforms with size limitations (such as FAT32 formatted drives).

---

## 🚀 Features

- 🔹 Splits files into 4GB chunks
- 🔹 Supports individual files or entire directories
- 🔹 Optional recursive search for nested folders
- 🔹 Deletes original file after splitting to save space
- 🔹 Simple CLI with live progress display
- 🔹 Pure Python, no external dependencies

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/nsplitter.git
cd nsplitter
```

Run it with:

```bash
python main.py ...
```

> ✅ Requires Python 3.8 or higher

---

## 🛠️ Usage

### Split specific files:

```bash
python main.py -f file1.mp4 file2.mp4 -e mp4
```

### Split all matching files in a directory:

```bash
python main.py -d /path/to/files -e mp4
```

### Options

| Flag | Description |
|------|-------------|
| `-f, --files`      | One or more specific files to split |
| `-d, --directory`  | Path to directory of files to split |
| `-e, --extension`  | File extension to match (e.g. `mp4`) |
| `-r, --recursive`  | Recursively include files in subdirectories |

---

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

## 🧪 Running Tests

```bash
python -m unittest test_nsplitter.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Brandon Jose Tenorio Noguera**  
📧 nsplitter@bjtn.me  
🌐 [bjtn.me](https://bjtn.me)  
🔗 [LinkedIn](https://www.linkedin.com/in/brandon-jose-tenorio-noguera/) • [GitHub](https://github.com/bjtn1)

---

## ✨ Contributing

Pull requests are welcome! Feel free to open an issue or submit a feature suggestion.

