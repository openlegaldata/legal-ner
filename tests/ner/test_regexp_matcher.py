from unittest import TestCase

import spacy

from legal_ner.ner.regexp_matcher import RegexpEntityMatcher
from legal_ner.ner.regexps.dates import GermanDates


class RegexpEntityMatcherTestCase(TestCase):

    def test_call(self):
        nlp = spacy.load('de_core_news_sm')
        doc = nlp('Es war der 1. Feb. 1111.')
        extractor = RegexpEntityMatcher(nlp, 'test', GermanDates())
        doc = extractor.__call__(doc)
        self.assertEqual('1. Feb. 1111', doc.ents[0].text)
        self.assertEqual('1111-02-01', doc.ents[0]._.get('regexp_match'))
