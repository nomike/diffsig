from diffsig.core import filter_diff, is_significant_block_change


def test_significant_block_change_detected():
    block1 = ["This is a test."]
    block2 = ["This is a completely different test."]
    assert is_significant_block_change(block1, block2, threshold=0.2)

def test_insignificant_block_change_ignored():
    block1 = ["This is a test."]
    block2 = ["This is a test!"]
    assert not is_significant_block_change(block1, block2, threshold=0.2)

def test_filter_diff_detects_changes():
    diff_text = """diff --git a/file.txt b/file.txt
--- a/file.txt
+++ b/file.txt
@@ -1 +1 @@
-Hello world
+Hello brave new world
"""
    changes = filter_diff(diff_text, threshold=0.2)
    assert "file.txt" in changes
    assert len(changes["file.txt"]) == 1
