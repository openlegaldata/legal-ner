from decimal import Decimal
from unittest import TestCase

from legal_ner.ner.regexps.percents import GermanPercentages, normalize_percentage_value


class PercentsTestCase(TestCase):
    regexp = GermanPercentages()
    text = 'Dies ist ein Beispiel für Prozent- und Promillewerte: 1% = 10 Promille, 99,' \
           '5 Prozent von 100€ entsprechen 99,5€. Die Promillegrenze liegt bei 0,0 ‰.'
    matches = ['1%', '10 Promille', '99,5 Prozent', '0,0 ‰']
    entities = ['0.010', '0.010', '0.995', '0.000']

    def test_regexp(self):
        for i, match in enumerate(self.regexp.regexp_obj().finditer(self.text)):
            self.assertEqual(self.matches[i], match.group(0))
            self.assertEqual(self.entities[i], self.regexp.normalize(match.groupdict(), match.group(0)), )

    def test_percentage_value_normalization(self):
        self.assertEqual(Decimal('0.1'), normalize_percentage_value('0,10'))
        self.assertEqual(Decimal('100'), normalize_percentage_value('100'))
        self.assertEqual(Decimal('100'), normalize_percentage_value('100.0'))
        self.assertEqual(Decimal('100'), normalize_percentage_value('100,0'))
