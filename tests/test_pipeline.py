from unittest import TestCase

from legal_ner.entity_extractors import EntityExtractor
from legal_ner.pipeline import StatisticalPipeline, RuleBasedPipeline


class PipelineTestCase(TestCase):

    def test_rule_based_extraction(self):
        extractor = EntityExtractor(RuleBasedPipeline('de_core_news_sm'))
        extractor.run('Der Kläger, Herr X., ist ein ehemaliger Minister für Energie und Kohleindustrie der Ukraine.\n'
                      '(2) Der Rat hat am 3. März 2014 beschlossen, im Hinblick auf die Stärkung und Unterstützung der '
                      'Rechtsstaatlichkeit sowie die Achtung der Menschenrechte in der Ukraine restriktive Maßnahmen '
                      'für das Einfrieren und die Einziehung von Vermögenswerten auf Personen, die als für die '
                      'Veruntreuung staatlicher Vermögenswerte der Ukraine verantwortlich identifiziert wurden, sowie '
                      'auf für Menschenrechtsverletzungen verantwortliche Personen zu konzentrieren.')
        self.assertEqual(['Kläger'], [ent[0] for ent in extractor.get_entities('PARTY')])
        self.assertEqual(['3. März 2014'], [ent[0] for ent in extractor.get_entities('DATE')])

    def test_statistical_extraction(self):
        extractor = EntityExtractor(StatisticalPipeline('de_core_news_sm'))
        extractor.run('Der Kläger, Herr X., ist ein ehemaliger Minister für Energie und Kohleindustrie der Ukraine.\n'
                      '(2) Der Rat hat am 3. März 2014 beschlossen, im Hinblick auf die Stärkung und Unterstützung der '
                      'Rechtsstaatlichkeit sowie die Achtung der Menschenrechte in der Ukraine restriktive Maßnahmen '
                      'für das Einfrieren und die Einziehung von Vermögenswerten auf Personen, die als für die '
                      'Veruntreuung staatlicher Vermögenswerte der Ukraine verantwortlich identifiziert wurden, sowie '
                      'auf für Menschenrechtsverletzungen verantwortliche Personen zu konzentrieren.')
        self.assertEqual(['Ukraine', 'Ukraine', 'Ukraine'], [ent[0] for ent in extractor.get_entities('LOC')])
