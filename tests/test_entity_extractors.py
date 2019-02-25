from unittest import TestCase

import spacy

from legal_ner.entity_extractors import EntityExtractor, HtmlEntityExtractor
from legal_ner.pipeline import Pipeline


class SimplePipe(Pipeline):
    def run(self, text):
        nlp = spacy.load(self.model)
        doc = nlp(text)
        return doc


class EntityExtractorTestCase(TestCase):

    def test_extraction(self):
        extractor = EntityExtractor(SimplePipe('de_core_news_sm'))
        extractor.run('Der Kläger, Herr X., ist ein ehemaliger Minister für Energie und Kohleindustrie der Ukraine.\n'
                      '(2) Der Rat hat am 3. März 2014 beschlossen, im Hinblick auf die Stärkung und Unterstützung der '
                      'Rechtsstaatlichkeit sowie die Achtung der Menschenrechte in der Ukraine restriktive Maßnahmen '
                      'für das Einfrieren und die Einziehung von Vermögenswerten auf Personen, die als für die '
                      'Veruntreuung staatlicher Vermögenswerte der Ukraine verantwortlich identifiziert wurden, sowie '
                      'auf für Menschenrechtsverletzungen verantwortliche Personen zu konzentrieren.')
        self.assertEqual(['Ukraine', 'Ukraine', 'Ukraine'], [ent[0] for ent in extractor.get_entities('LOC')])


class HtmlEntityExtractorTestCase(TestCase):

    def test_extraction(self):
        extractor = HtmlEntityExtractor(SimplePipe('de_core_news_sm'))
        extractor.run('<p>&nbsp;&nbsp;&nbsp;Der Kl&auml;ger, Herr X., ist ein ehemaliger '
                      'Minister für Energie und Kohleindustrie der Ukraine.</p>')
        self.assertEqual(['Ukraine'], [ent[0] for ent in extractor.get_entities('LOC')])
