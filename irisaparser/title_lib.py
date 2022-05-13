# -*- coding: utf-8 -*-

import pdfplumber
from .title_filters import *

def largest_titles(pdf: pdfplumber.PDF, max_sentences, font_list):
    """return array with x largest sentences in pdf file using font list"""
    res = []
    page = pdf.pages[0]

    num_sentences = len(font_list)
    i = 0
    potent_title = ""
    while i < num_sentences:
        for char in page.chars:
            if char.get("size") == font_list[i]:
                potent_title += char.get("text")
        res.append(potent_title)
        potent_title = ""
        i = i + 1

    return res


def get_largest_fonts_list(page, font_amount):
    """Return array with x largest fonts in page"""

    page_fonts = []
    
    for char in page.chars:
        font_size = round(char.get("size"), 4)
        # only add to list fonts that are different
        if font_size not in page_fonts:
            page_fonts.append(font_size)

    # sort fonts from largest to smallest
    page_fonts.sort(reverse=True)

    return page_fonts[: font_amount - 1]


def regroup_chars_by_fonts(page, largest_fonts_list):
    """
    returns sentences with chars of provided font_sizes
    """
    sentences = []
    for font in largest_fonts_list:
        sentence = ""
        for char in page.chars:
            # char has same font size as current font
            if round(char.get("size"), 4) == font:
                sentence = sentence + char.get("text")
        sentences.append(sentence)
    return sentences

def get_title_from_metadata(pdf: pdfplumber.PDF):
    
    meta_title = pdf.metadata.get("Title")
    
    if not meta_title:
        return None

    meta_title = meta_title.strip()

    if len(meta_title) < 5:
        return None

    invalid_chars = ["/","\\","(",")",]

    for ic in invalid_chars:
        if ic in meta_title:
            return None

    return meta_title


def match_potential_titles(lines_input, potential_titles):
    """
    check extracted lines against found titles (using font regrouping)
    if they both match, add the title to result array
    """
    lines = lines_input
    res = []

    for pot_title in potential_titles:
        prev = ""

        for line in lines:
            
            # removes spaces
            raw_title = pot_title.replace(" ", "")
            raw_line = line.replace(" ", "")

            if raw_line == raw_title:
                res.append(line)

            """
            Try joining current lines with precedent one to form a title match
            This is used to parse a title if a newline was present in a title.
            """
            prev_raw_line = prev.replace(" ", "")
            concat_prev = prev_raw_line + raw_line

            if concat_prev == raw_title:
                res.append((prev + " " + line))

            prev = line
    return res

def get_title(pdf: pdfplumber.PDF):
    
    page = pdf.pages[0] # get Only first page

    # get text line by line
    raw_text = page.extract_text(x_tolerance=3, y_tolerance=3)
    # store in list
    lines = raw_text.split("\n")

    # remove useless lines and keep only first 5 valid lines
    lines = get_first_lines(lines,5)

    # fetch only 5 largest fonts in page
    largest_fonts_list = get_largest_fonts_list(pdf, 5)

    # only use fonts above size threshold
    largest_fonts_list = filter_fonts_by_minsize(largest_fonts_list,8.0)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = regroup_chars_by_fonts(page, largest_fonts_list)

    # filtering ridiculously long or short files and containing some characters
    potential_titles = filter_titles_by_length(potential_titles)

    # try to find titles by comparing extrated lines to titles detected using fonts regrouping
    matched = match_potential_titles(lines, potential_titles)

    # filter duplicates
    matched = filter_duplicates(matched)

    # trying to determine final title:
    final_title = ""
    errcount = 0

    if len(matched) == 1:
        final_title = matched[0]

    elif len(matched) > 1:  # more than one title found -> keep largest one
        errcount = errcount + 1
        final_title = matched[0]

    elif len(matched) == 0:  # title not found -> consult metadata -> if not accurate, first line is used
        final_title = get_title_from_metadata(pdf)
        
        if final_title is None:
            final_title = lines[0]

    return final_title