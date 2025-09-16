import argparse
import sys

from diffsig.core import filter_diff, print_changes

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def print_changes(changes, use_color):
    """Print the significant changes with optional color."""
    for old_block, new_block in changes:
        print("Significant change detected:")
        for line in old_block:
            prefix = "- "
            print(f"{RED if use_color else ''}{prefix}{line}{RESET if use_color else ''}")
        for line in new_block:
            prefix = "+ "
            print(f"{GREEN if use_color else ''}{prefix}{line}{RESET if use_color else ''}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Filter diff output for significant changes.")
    parser.add_argument("filename", nargs='?', default="-",
                        help="Filename to read diff from, or '-' for stdin (default: '-')")
    parser.add_argument("--threshold", type=float, default=0.2,
                        help="Threshold for character-level difference (default: 0.2 = 20%)")
    parser.add_argument("--color", action="store_true",
                        help="Force color output even if not writing to a terminal")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable color output even if writing to a terminal")
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
