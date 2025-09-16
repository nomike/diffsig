import difflib

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def is_significant_block_change(block1, block2, threshold=0.2):
    """Check if the character-level difference between two blocks exceeds the threshold."""
    text1 = "\n".join(block1)
    text2 = "\n".join(block2)
    sm = difflib.SequenceMatcher(None, text1, text2)
    similarity = sm.ratio()
    return (1 - similarity) > threshold

def filter_diff(diff_text, threshold):
    """Process diff output and report significant changes per file."""
    lines = diff_text.splitlines()
    significant_changes_by_file = {}

    current_file = None
    removed_block = []
    added_block = []

    for line in lines:
        if line.startswith("diff --git"):
            parts = line.split()
            if len(parts) >= 3:
                current_file = parts[2][2:]  # Remove 'b/' prefix
        elif line.startswith("--- ") or line.startswith("+++ "):
            continue  # Ignore these lines for now
        elif line.startswith('-') and not line.startswith('---'):
            removed_block.append(line[1:].strip())
        elif line.startswith('+') and not line.startswith('+++'):
            added_block.append(line[1:].strip())
        else:
            if removed_block and added_block:
                if is_significant_block_change(removed_block, added_block, threshold):
                    significant_changes_by_file.setdefault(current_file, []).append((removed_block, added_block))
                removed_block = []
                added_block = []
            elif removed_block or added_block:
                removed_block = []
                added_block = []

    if removed_block and added_block:
        if is_significant_block_change(removed_block, added_block, threshold):
            significant_changes_by_file.setdefault(current_file, []).append((removed_block, added_block))

    return significant_changes_by_file

def print_changes(changes_by_file, use_color):
    """Print significant changes grouped by filename."""
    for filename, changes in changes_by_file.items():
        print(f"\nFile: {filename}")
        for old_block, new_block in changes:
            print("Significant change detected:")
            for line in old_block:
                prefix = "- "
                print(f"{RED if use_color else ''}{prefix}{line}{RESET if use_color else ''}")
            for line in new_block:
                prefix = "+ "
                print(f"{GREEN if use_color else ''}{prefix}{line}{RESET if use_color else ''}")
            print()
