import pytest
import irisaparser.lib_metadata as lib_metadata
import os
from pathlib import Path

corpus_dir = Path.cwd() / 'tests' / 'corpus'
custom_corpus_dir = Path.cwd() / 'tests' / 'custom'


def test_meta_exists_Title():
    pdf = corpus_dir / 'Boudin-Torres-2006.pdf'
    expected = "A Scalable MMR Approach to Sentence Scoring for Multi-Document Update Summarization"
    actual = lib_metadata.extract(pdf)
    assert (expected) == actual["Title"]
    
    
def test_meta_exists_Titlea():
    pdf = custom_corpus_dir / 'test_metadata.pdf'
    expected = "Your PDF title"
    actual = lib_metadata.extract(pdf)
    assert (expected) == actual["Title"]