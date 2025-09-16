import difflib


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
