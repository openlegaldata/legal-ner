import re

from decimal import Decimal

from legal_ner.nlp.ner.regexps.base import Regexp

PERCENTAGE_VALUE_GROUP = 'value'
PERCENTAGE_SYMBOL_GROUP = 'symbol'


def normalize_percentage_value(value: str) -> str:
    return value.replace(',', '.')


class GermanPercentages(Regexp):
    VALUE = r'\d+([,\.]\d+)?'
    SYMBOL_MAP = {
        100: r'%|Prozent|vo[nm] Hundert|Hundertstel|v\.? ?H',
        1000: r'‰|Promille|Tausendstel'
    }
    SYMBOLS = r'|'.join(SYMBOL_MAP.values())
    FLAGS = re.IGNORECASE

    def regexp_obj(self):
        return re.compile(r'(?:\b)(?P<{value_group}>{value})(?: ?)(?P<{symbol_group}>{symbols})'
                          .format(value_group=PERCENTAGE_VALUE_GROUP,
                                  symbol_group=PERCENTAGE_SYMBOL_GROUP,
                                  value=self.VALUE,
                                  symbols=self.SYMBOLS),
                          self.FLAGS)

    def normalize(self, groups: dict, full_match: str):
        """Returns a percentage as decimal string."""
        for divisor, regex in self.SYMBOL_MAP.items():
            if re.search(regex, groups[PERCENTAGE_SYMBOL_GROUP], self.FLAGS) is not None:
                return str(Decimal(normalize_percentage_value(groups[PERCENTAGE_VALUE_GROUP]) /
                                   Decimal(divisor)))
        raise ValueError('Percentage {} could not be normalized!'.format(full_match))
