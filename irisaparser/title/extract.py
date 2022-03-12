import pdfplumber
import title.filters
from colorama import Fore
import title.parse
debug_prefix = Fore.LIGHTBLACK_EX + "(title)"
title_debug = False


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
    # find every fonts in page
    for char in page.chars:
        scan = round(char.get("size"), 4)
        # only add to list fonts that are different
        if scan not in page_fonts:
            page_fonts.append(scan)

    # sort fonts from largest to smallest
    page_fonts.sort(reverse=True)
    page_fonts = page_fonts[: font_amount - 1]

    return page_fonts


def get_largest_sentences(page, largest_fonts_list):
    """
    for every large font:
        get corresponding text in page into line and store it in array
    """
    sentences = []
    for font in largest_fonts_list:
        scan = ""
        for char in page.chars:
            if round(char.get("size"), 4) == font:
                scan = scan + char.get("text")
        sentences.append(scan)
    return sentences




def best_title(pdf: pdfplumber.PDF):
    
    
    
    # get Only 1/3 of pdf's first page
    page = pdf.pages[0]

    # get text line by line
    raw_text = page.extract_text(x_tolerance=3, y_tolerance=3)
    # store in list
    lines = raw_text.split("\n")

    # remove useless lines and keep only first 5 valid lines
    lines = title.filters.filter_lines(lines)


    # fetch only 5 largest fonts in page
    largest_fonts_list = get_largest_fonts_list(pdf, 5)

    # only use fonts above threshold
    largest_fonts_list = title.filters.filter_fonts(largest_fonts_list)

    # find in whole page, sequences of text matching largest fonts
    potential_titles = get_largest_sentences(page, largest_fonts_list)

    # filtering ridiculously long or short files and containing some characters
    potential_titles = title.filters.filter_potential_titles(potential_titles)


    matched = title.parse.parse_potential_titles(lines, potential_titles)

    # filter duplicates
    matched = title.filters.filter_duplicates(matched)
    final_title = ""
    ##### FALLBACKS
    errcount = 0
    if len(matched) > 1:  # more than one title found -> keep largest one
        errcount = errcount + 1
        if title_debug:
            print(
                debug_prefix
                + Fore.BLUE
                + "[*]WARN : multiple titles ! selecting [0] by default"
                + Fore.RESET
            )
        final_title = matched[0]

    if len(matched) == 1:
        final_title = matched[0]

    if (
        len(matched) == 0
    ):  # title not found -> consult metadata -> if not accurate, first line is used
        if title_debug:
            print(
                debug_prefix
                + Fore.BLUE
                + "[*]WARN : NO REGULAR TITLE FOUND ! falling back on metadata"
                + Fore.RESET
            )
        meta_title = title.parse.title_metadata(pdf)
        if meta_title is None:
            if title_debug:
                print(
                    debug_prefix
                    + Fore.BLUE
                    + "[*]WARN : NO TITLE METADATA FOUND ! falling back on first line..."
                    + Fore.RESET
                )
            final_title = lines[0]
        else:
            final_title = meta_title

    if title_debug:
        print(
            debug_prefix
            + Fore.GREEN
            + '[>]RESULT : "'
            + Fore.RESET
            + final_title
            + Fore.GREEN
            + '"\n'
        )

    return final_title
