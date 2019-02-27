import re

import dateparser

from legal_ner.ner.regexps.base import Regexp


class GermanDates(Regexp):

    def regexp_obj(self):
        return re.compile(r'\b((0?[1-9]|[123]\d)\..?)?'
                          r'(((0?[1-9]|1[012])\.)|((Jan|Feb|Mrz|Mä|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)[a-z]{0,6}\.? ))'
                          r'([12]\d)?\d{2}\b')

    def normalize(self, groups: dict, full_match: str):
        """Returns the date formatted in ISO."""
        return dateparser.parse(full_match).date().isoformat()
