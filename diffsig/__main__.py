import argparse
import difflib
import sys

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def is_significant_block_change(block1, block2, threshold=0.2):
    """Check if the character-level difference between two blocks exceeds the threshold."""
    text1 = "\n".join(block1)
    text2 = "\n".join(block2)
    sm = difflib.SequenceMatcher(None, text1, text2)
    similarity = sm.ratio()
    return (1 - similarity) > threshold

def filter_diff(diff_text, threshold):
    """Process diff output and report significant changes."""
    lines = diff_text.splitlines()
    significant_changes = []

    removed_block = []
    added_block = []

    for line in lines:
        if line.startswith('-') and not line.startswith('---'):
            removed_block.append(line[1:].strip())
        elif line.startswith('+') and not line.startswith('+++'):
            added_block.append(line[1:].strip())
        else:
            if removed_block and added_block:
                if is_significant_block_change(removed_block, added_block, threshold):
                    significant_changes.append((removed_block, added_block))
                removed_block = []
                added_block = []
            elif removed_block or added_block:
                removed_block = []
                added_block = []

    if removed_block and added_block:
        if is_significant_block_change(removed_block, added_block, threshold):
            significant_changes.append((removed_block, added_block))

    return significant_changes

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

    changes = filter_diff(diff_text, args.threshold)
    print_changes(changes, use_color)

if __name__ == "__main__":
    main()
