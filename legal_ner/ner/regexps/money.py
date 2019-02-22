import re
from decimal import Decimal
from typing import Pattern

from legal_ner.ner.regexps.base import Regexp

MONEY_AMOUNT_GROUP = 'amount'
MONEY_CURRENCY_GROUP = 'currency'


def normalize_money_amount(value: str) -> str:
    return str(Decimal(value.replace('.', '').replace(',', '.')).quantize(Decimal('0.01')))


class GermanEuros(Regexp):
    MONEY_AMOUNT = r'(([1-9]{1}[0-9]{0,2})*(\.\d{3})+|\d+)(,\d{1,2})?'
    EUROS = r'€|Euros?'

    def regexp_obj(self):
        return re.compile(
            r'(?:\b)(?P<{amount_group}>{amount})(?: ?)(?P<{currency_group}>{currency})'
                .format(amount_group=MONEY_AMOUNT_GROUP,
                        currency_group=MONEY_CURRENCY_GROUP,
                        amount=self.MONEY_AMOUNT,
                        currency=self.EUROS),
            re.IGNORECASE)

    def normalize(self, groups: dict, full_match: str):
        """Returns the amount in euros as decimal string."""
        return normalize_money_amount(groups[MONEY_AMOUNT_GROUP])


class GermanCurrencies(Regexp):
    AMOUNT = r'(([1-9]{1}[0-9]{0,2})*(\.\d{3})+|\d+)(,\d{1,2})?'
    CURRENCIES_MAP = {
        'EUR': r'€|Euros?',
        'USD': r'\$|(US[ -]?)?Dollar',
        'GBP': r'£|britische.? Pfund|Pfund Sterling'
    }
    CURRENCIES = r'|'.join(list(CURRENCIES_MAP.values()) + list(CURRENCIES_MAP.keys()))
    FLAGS = re.IGNORECASE

    def regexp_obj(self):
        return re.compile(r'(?P<{amount_group}>{amount})(?: ?)(?P<{currency_group}>{currency})'
                          .format(amount_group=MONEY_AMOUNT_GROUP,
                                  currency_group=MONEY_CURRENCY_GROUP,
                                  amount=self.AMOUNT,
                                  currency=self.CURRENCIES),
                          self.FLAGS)

    def compute_currency_code(self, currency: str) -> str:
        if currency in self.CURRENCIES_MAP.keys():
            return currency
        else:
            for code, regex in self.CURRENCIES_MAP.items():
                if re.search(regex, currency, self.FLAGS) is not None:
                    return code
            raise ValueError('Currency {} not found!'.format(currency))

    def normalize(self, groups: dict, full_match: str):
        """Returns a tuple with the ISO 4217 currency code and the amount as decimal string."""
        return self.compute_currency_code(groups[MONEY_CURRENCY_GROUP]), normalize_money_amount(
            groups[MONEY_AMOUNT_GROUP])


class EnglishCurrencies(Regexp):
    MONEY_AMOUNT = r'(([1-9]{1}[0-9]{0,2})*(,\d{3})+|\d+)(\.\d{2})?'

    def regexp_obj(self) -> Pattern:
        raise NotImplementedError()
