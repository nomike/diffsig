import argparse
import sys

from diffsig.__version__ import __version__
from diffsig.core import filter_diff, print_changes


def main():
    parser = argparse.ArgumentParser(description="Filter diff output for significant changes.")
    parser.add_argument("filename", nargs='?', default="-",
                        help="Filename to read diff from, or '-' for stdin (default: '-')")
    parser.add_argument("--threshold", type=float, default=0.2,
                        help="Threshold for character-level difference (default: 0.2 = 20%%)")
    parser.add_argument("--color", action="store_true",
                        help="Force color output even if not writing to a terminal")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable color output even if writing to a terminal")
    parser.add_argument("--version", action="version", version=f"diffsig {__version__}")
    args = parser.parse_args()

    output_is_terminal = sys.stdout.isatty()
    use_color = args.color or (output_is_terminal and not args.no_color)

    if args.filename == "-":
        diff_text = sys.stdin.read()
    else:
        with open(args.filename, "r", encoding="utf-8") as f:
            diff_text = f.read()


    changes_by_file = filter_diff(diff_text, args.threshold)
    print_changes(changes_by_file, use_color)


if __name__ == "__main__":
    main()
