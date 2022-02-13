import json
import pdfplumber

def extract(input_path):
    """Returns metadata of given pdf as Dictionary"""
    with pdfplumber.open(input_path) as pdf:
        return pdf.metadata

