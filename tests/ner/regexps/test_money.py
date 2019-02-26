from unittest import TestCase

from legal_ner.ner.regexps.money import normalize_money_amount, GermanEuros, GermanCurrencies


class MoneyNormalizationTestCase(TestCase):

    def test_money_amount_normalization(self):
        self.assertEqual('0.10', normalize_money_amount('0,10'))
        self.assertEqual('6666.66', normalize_money_amount('6.666,66'))
        self.assertEqual('42.00', normalize_money_amount('42,00'))
        self.assertEqual('42.00', normalize_money_amount('42'))


class GermanEurosTestCase(TestCase):
    regexp = GermanEuros()
    text = 'Der Kläger lebte bis Ende 2006 in B., zog dann nach Ba. um und Anfang ' \
           '2008 nach B. zurück. Er bezog bereits bei seinem ersten B.- Aufenthalt ' \
           'Leistungen der Grundsicherung für Arbeitsuchende nach dem SGB II. Der in ' \
           'B. für ihn zuständige Grundsicherungsträger, die Arge E., gewährte ihm ' \
           'bis Dezember 2007 Leistungen zur Sicherung des Lebensunterhalts - ohne ' \
           'sanktionsbedingten oder sonstigen Abzug - in Höhe von 537,52 Euro (' \
           'Regelleistung: 347 Euro und Leistungen für Unterkunft und Heizung: 190,' \
           '52 Euro). Durch Bescheid vom 14.1.2008 hob sie die Bewilligung mit ' \
           'Wirkung ab dem 1.2.2008 wegen des Wechsels der Zuständigkeit auf Grund ' \
           'des Umzugs des Klägers auf. Am 25.1.2008 bewilligte der Beklagte dem ' \
           'Kläger für den Zeitraum vom 1.2.2008 bis 30.6.2008 ' \
           'Grundsicherungsleistungen in Gestalt einer Regelleistung von 347 Euro ' \
           'und für Kosten der Unterkunft von 193,19 Euro.'
    matches = ['537,52 Euro', '347 Euro', '190,52 Euro', '347 Euro', '193,19 Euro']
    entities = ['537.52', '347.00', '190.52', '347.00', '193.19']

    def test_regexp(self):
        for i, match in enumerate(self.regexp.regexp_obj().finditer(self.text)):
            self.assertEqual(self.matches[i], match.group(0))
            self.assertEqual(self.entities[i], self.regexp.normalize(match.groupdict(), match.group(0)), )

    def test_euro_amounts(self):
        euros = ['1€', '1000000€', '3.000€', '3.000.000 €', '999,99€', '100 Euro', '1,20Euro']
        for euro in euros:
            self.assertTrue(self.regexp.regexp_obj().match(euro))

    def test_non_euro_amounts(self):
        not_euros = ['€1', '10$', '30.00€', '100,000€', 'Euro', 'Euro 1000']
        for not_euro in not_euros:
            self.assertFalse(self.regexp.regexp_obj().match(not_euro))


class GermanCurrenciesTestCase(TestCase):
    regexp = GermanCurrencies()
    text = 'Dieser Text enthält Werte in USD, Britischen Pfund und Euro. Zum 23.12.2018 ' \
           'sind 1€ ungefähr 0,9 Britische Pfund und 1,14 USD.'
    matches = ['1€', '0,9 Britische Pfund', '1,14 USD']
    entities = [('EUR', '1.00'), ('GBP', '0.90'), ('USD', '1.14')]

    def test_regexp(self):
        for i, match in enumerate(self.regexp.regexp_obj().finditer(self.text)):
            self.assertEqual(self.matches[i], match.group(0))
            self.assertEqual(self.entities[i], self.regexp.normalize(match.groupdict(), match.group(0)), )

    def test_currency_code_computation(self):
        self.assertEqual('EUR', self.regexp.compute_currency_code('EUR'))
        self.assertEqual('EUR', self.regexp.compute_currency_code('€'))
        self.assertEqual('EUR', self.regexp.compute_currency_code('Euro'))
        self.assertEqual('EUR', self.regexp.compute_currency_code('Euros'))
        self.assertEqual('USD', self.regexp.compute_currency_code('USD'))
        self.assertEqual('USD', self.regexp.compute_currency_code('$'))
        self.assertEqual('USD', self.regexp.compute_currency_code('US-Dollar'))
        self.assertEqual('USD', self.regexp.compute_currency_code('US-Dollars'))
        self.assertEqual('USD', self.regexp.compute_currency_code('Dollar'))
        self.assertRaises(ValueError, self.regexp.compute_currency_code, 'Hallo')
