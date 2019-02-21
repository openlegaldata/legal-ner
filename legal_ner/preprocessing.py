import html
import re

import numpy as np


class HtmlConcealer:

    def __init__(self, html_str):
        self.content = html_str
        self.pos_table = np.arange(len(self.content))

    def conceal(self):
        self.remove_pattern(r'<br.*>', replace_with='\n')  # html linebreaks
        self.remove_pattern(r'<[^>]+>')  # html tags
        self.remove_pattern(r'(\xa0)+|(' '){2,}', replace_with=' ')  # excess whitespace
        self.remove_pattern(r'(^ *)|( * $)', flags=re.MULTILINE)  # leading or trailing whitespace
        self.remove_pattern(r'\n{2,}', replace_with='\n')  # excess newlines
        self.replace_html_special_ents()
        self.remove_pattern(r'^(\d{1,3}|[a-z]|I{1,3})(\)|\.)? ?', flags=re.MULTILINE)  # enumeration numbers

    def get_content(self):
        return self.content

    def concealed_to_html_pos(self, pos_start, pos_end):
        return self.pos_table[pos_start], self.pos_table[pos_end]

    def remove_pattern(self, regex, replace_with='', flags=0):
        pattern = re.compile(regex, flags=flags)
        while True:
            m = re.search(pattern, self.content)
            if m is None:
                break
            self.content = self.content[:m.start(0)] + replace_with + self.content[m.end(0):]
            self.pos_table = np.delete(self.pos_table, np.arange(m.start(0) + len(replace_with), m.end(0)))

    def replace_html_special_ents(self):
        pattern = re.compile(r'&#\d{1,4};|&\w{1,6};')
        while True:
            m = re.search(pattern, self.content)
            if m is None:
                break
            unicode = html.unescape(m.group(0))
            self.content = self.content[:m.start(0)] + unicode + self.content[m.end(0):]
            self.pos_table = np.delete(self.pos_table, np.arange(m.start(0) + 1, m.end(0)))
