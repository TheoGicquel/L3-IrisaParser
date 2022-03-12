from colorama import Fore

title_debug=False
debug_prefix = Fore.LIGHTBLACK_EX + "(title)"
import pdfplumber

def title_metadata(pdf: pdfplumber.PDF):
    

    meta_title = pdf.metadata.get("Title")
    meta_title = meta_title.strip()
    if len(meta_title) < 5:
        return None

    invalid_chars = [
        "/",
        "\\",
        "(",
        ")",
    ]

    for c in meta_title:
        if c in invalid_chars:
            return None

    if meta_title is None:
        if title_debug:
            print(
                debug_prefix
                + Fore.RED
                + "[*]ERROR : NO VALID METADATA FOUND"
                + Fore.RESET
            )
        return None

    return meta_title


def parse_potential_titles(lines_input, potential_titles):
    """
    check extracted lines against found titles
    if they both match, add the title to result array
    """
    lines = lines_input
    res = []

    for pot_title in potential_titles:
        prev = ""

        for line in lines:

            raw_title = pot_title.replace(" ", "")
            raw_line = line.replace(" ", "")

            if raw_line == raw_title:
                res.append(line)

            """
            Try joining extracted text lines to form a title match
            This is used to parse a title if a newline was present in a title.
            """
            prev_raw_line = prev.replace(" ", "")
            concat_prev = prev_raw_line + raw_line

            if concat_prev == raw_title:
                res.append((prev + " " + line))

            prev = line
    return res


