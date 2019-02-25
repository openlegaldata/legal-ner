from unittest import TestCase

import spacy

from legal_ner.ner.entity_relations import EntityRelationExtractor, merge_spans, extract_relations_en, \
    extract_relations_de


class EntityRelationsTestCase(TestCase):

    def test_extract_pobj_en(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp('The man resides in the USA.')
        relations = extract_relations_en(doc[5])  # USA
        self.assertEqual(('man', 'reside'), relations)

    def test_extract_dobj_en(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp('The cat owns 1000 €.')
        merge_spans(doc.ents)
        relations = extract_relations_en(doc[3])  # 1000 €
        self.assertEqual(('cat', 'own'), relations)

    def test_extract_relations_oa_de(self):
        nlp = spacy.load('de_core_news_sm')
        doc = nlp('Der Hund begrüßt Anton.')
        relations = extract_relations_de(doc[3])  # Anton
        self.assertEqual(('Hund', 'begrüßen'), relations)

    def test_extract_relations_nk_de(self):
        nlp = spacy.load('de_core_news_sm')
        doc = nlp('Der Vogel verbringt den Winter in Afrika.')
        relations = extract_relations_de(doc[6])  # Afrika
        self.assertEqual(('Vogel', 'in'), relations)


class EntityRelationExtractorTestCase(TestCase):

    def test_call(self):
        nlp = spacy.load('de_core_news_sm')
        doc = nlp('Der Vogel verbringt den Winter in Afrika.')
        extractor = EntityRelationExtractor('LOC', 'de_core_news_sm')
        doc = extractor.__call__(doc)
        self.assertEqual('Vogel', doc.ents[0]._.get('entity_relation_subj'))
        self.assertEqual('in', doc.ents[0]._.get('entity_relation_root'))
