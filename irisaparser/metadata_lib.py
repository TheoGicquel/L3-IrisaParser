import json
import pdfplumber

def get(input_path):
    """Returns metadata of given pdf as Dictionary"""
    with pdfplumber.open(input_path) as pdf:
        return pdf.metadata

def get_title(input_path):
    """Returns Title metadata of given pdf"""
    with pdfplumber.open(input_path) as pdf:
        return pdf.metadata.get('Title')
    