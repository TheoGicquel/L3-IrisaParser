import pytest
import irisaparser.lib_metadata
import irisaparser.title
from pathlib import Path

corpus_dir = Path.cwd() / 'tests' / 'corpus'
custom_corpus_dir = Path.cwd() / 'tests' / 'custom'


def test_title_ok_meta():
    pdf = custom_corpus_dir / 'test_metadata.pdf'
    expected = "Your PDF title"
    actual = irisaparser.title.extract(pdf)
    assert (expected) == actual["Title"]
