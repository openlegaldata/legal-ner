from unittest import TestCase

from legal_ner.ner.regexps.dates import GermanDates


class DatesTestCase(TestCase):
    regexp = GermanDates()
    text = 'Mit der Verordnung (EU) 2015/123 des Rates vom 29. Januar 2015 zur Änderung der Verordnung Nr. ' \
           '208/2014 (ABl. 2015, L 99, S. 1) wurde diese entsprechend dem Beschluss am 1.3.2015 2015/123 geändert.'
    matches = ['29. Januar 2015', '1.3.2015']
    entities = ['2015-01-29', '2015-03-01']

    def test_regexp(self):
        for i, match in enumerate(self.regexp.regexp_obj().finditer(self.text)):
            self.assertEqual(self.matches[i], match.group(0))
            self.assertEqual(self.entities[i], self.regexp.normalize(match.groupdict(), match.group(0)),)
