from unittest import TestCase

import spacy
from spacy.symbols import LEMMA
from legal_ner.ner.pattern_based import PatternBasedMatcher


class RuleBasedMatcherTestCase(TestCase):

    def test_call(self):
        nlp = spacy.load('de_core_news_sm')
        patterns = [[{LEMMA: 'Kläger'}]]
        doc = nlp('Der Name des Klägers stand nicht auf der streitigen Liste.')
        matcher = PatternBasedMatcher(nlp, patterns, 'test')
        doc = matcher.__call__(doc)
        self.assertEqual(len(doc.ents), 1)
        self.assertEqual(doc.ents[0].text, 'Klägers')
