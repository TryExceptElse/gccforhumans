#!/usr/bin/env python3

import re
import sys
import typing as ty


def clean_comparisons(s: str) -> str:
    quotes = get_quotes(s)
    if len(quotes) >= 2 or 'candidate:' in s:
        if any(
            reduce_templates(quotes[i]) ==
            reduce_templates(quotes[i + 1]) for 
            i in range(len(quotes) - 1)
        ):
            return s

        out = s
        for quote in quotes:
            out = out.replace(quote, reduce_templates(quote))
        return out
    else:
        return s


def reduce_templates(s: str) -> str:
    level = 0
    out = ''
    for c in s:
        if c == '>':
            level -= 1
        if not level:
            out += c
        if c == '<':
            level += 1
    return out


def get_quotes(s: str) -> ty.List[str]:
    quotes = []
    quote = ''
    in_quote = False
    for c in s:
        if c in (chr(8216), chr(8217)):  # ‘
            if in_quote:
                quotes.append(quote)
                quote = ''
                in_quote = False
            else:
                in_quote = True
        elif in_quote:
            quote += c
    return quotes


def hide_lib_versions(s: str) -> str:
    return re.sub(r'::__cxx[0-9][0-9]::', '::', s)


class CandidateShortener:
    def __init__(self):
        self.i = 0
        self.ignore = set()
        
    def shorten(self, s: str) -> str:
        if 'candidate:' in s:
            for i in range(self.i + 4, self.i + 10):
                self.ignore.add(i)
        r = None if self.i in self.ignore else s
        self.i += 1
        return r


def main():
    candidate_shortener = CandidateShortener()

    for line in sys.stdin:
        line = clean_comparisons(line)
        line = hide_lib_versions(line)
        line = candidate_shortener.shorten(line)
        if line:
            print(line, end='')  # read-in line has newline
        
if __name__ == '__main__':
    main()
