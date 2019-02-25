from unittest import TestCase

import spacy
from spacy.symbols import ORTH, LEMMA, POS, NORM

from legal_ner.tokenization.tokenizer import create_custom_tokenizer


class TokenizationTestCase(TestCase):

    def test_create_custom_tokenizer(self):
        nlp = spacy.load('de_core_news_sm')
        nlp.tokenizer = create_custom_tokenizer(nlp)
        doc = nlp('Ehefrau A. des Klägers A1. hat am 12. Dezember in Schl.-Holst. ein Haus gekauft.')
        self.assertEqual(['Ehefrau', 'A.', 'des', 'Klägers', 'A1.', 'hat', 'am', '12.', 'Dezember', 'in',
                          'Schl.-Holst.', 'ein', 'Haus', 'gekauft', '.'], [token.text for token in doc])

    def test_special_cases(self):
        nlp = spacy.load('de_core_news_sm')
        special_cases = {u'Art.': [{ORTH: u'Art.', LEMMA: u'Artikel', NORM: u'Artikel', POS: u'NOUN'}],
                         u'Buchst.': [{ORTH: u'Buchst.', LEMMA: u'Buchstabe', NORM: u'Buchstabe', POS: u'NOUN'}]}
        for word, special_case in special_cases.items():
            nlp.tokenizer.add_special_case(word, special_case)
        doc = nlp('Art. 21 Abs. 2 Buchst. b EUV')
        self.assertEqual(['Art.', '21', 'Abs.', '2', 'Buchst.', 'b', 'EUV'], [token.text for token in doc])
        self.assertTrue('Artikel' in [token.lemma_ for token in doc])
