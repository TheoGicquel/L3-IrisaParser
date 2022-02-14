import json
import pdfplumber

from pathlib import Path
corpus_dir = Path.cwd() / 'tests' / 'corpus'
custom_corpus_dir = Path.cwd() / 'tests' / 'custom'



def extract(input_path):
    """Returns metadata of given pdf as Dictionary"""
    with pdfplumber.open(input_path) as pdf:
        return pdf.metadata

