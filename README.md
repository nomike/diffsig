
# diffsig

**diffsig** is a command-line tool that analyzes unified diff output and reports only **significant changes** based on a configurable character-level difference threshold.

It’s especially useful for developers working with configuration files, infrastructure-as-code, or large diffs where minor changes (like reordered hostnames or whitespace tweaks) can clutter reviews.

---

## 🔧 Features

- ✅ Filters out trivial changes
- ✅ Detects meaningful modifications across multiple lines
- ✅ Supports input from files or `stdin`
- ✅ Configurable threshold (default: 20%)

## Usage
From a file:

```Shell
./diffsig.py diff_output.txt
```

From a pipe:

```Shell
diff -ru folder1 folder2 | ./diffsig.py -
```

With a custom threshold:

```Shell
./diffsig.py diff_output.txt --threshold 0.1
```

## 📥 Input Format
diffsig expects unified diff format, such as the output from:

```Shell
diff -ru folder1 folder2
```

## 📤 Output
Only blocks of changes where the character-level difference exceeds the threshold are printed. Each block is prefixed with:

```
Significant change detected:
```

## 🛠 Example

```Diff
- http_proxy: 'http://proxy.pr.euc1.paysafecard.at:8080'
+ http_proxy: 'http://proxy.pr.euw1.paysafecard.at:8080'
```

This will be ignored unless the overall block change exceeds the threshold.

## 📄 License
MIT License

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

## 📫 Contact
For questions or suggestions, open an issue or reach out via GitHub.
