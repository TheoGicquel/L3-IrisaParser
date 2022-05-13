# -*- coding: utf-8 -*-

def get_first_lines(line_list,number_of_lines):
    """return the 5 first lines, ignore lines shorter than 2 characters"""
    res = []
    count = 0

    for line in line_list:
        valid = True
        # catching incorrect lines
        if len(line) < 2:
            valid = False

        # final check
        if valid:
            count+=1
            res.append(line)
            
        if count >= number_of_lines: break
    # return only first 5 valid lines
    return res


def filter_fonts_by_minsize(fonts,threshold):
    """Return only fonts above threshold"""
    res = []
    for font in fonts:
        if font > threshold:
            res.append(font)
    return res


def filter_titles_by_length(titles,min=2,max=80):
    """Filter invalid titles (too short,too long)"""
    res = []

    for title in titles:
        char_only = str(title).strip()
        length = len(char_only)

        # catch wrong titles
        if length > min and length < max:
            res.append(title)

    return res


def filter_duplicates(titles):
    test = titles
    res = []
    for i in test:
        i = i.strip()  # remove extra spaces at beginning and end
        i = " ".join(i.split())
        res.append(i)
    res = list(dict.fromkeys(res)) # seems ugly but it's the way ¯\_(ツ)_/¯
    return res