from pathlib import Path
from unittest import TestCase

import spacy

from legal_ner.training.test import test
from legal_ner.training.train_ner import train, add_labels, get_ner_labels, add_pipe
from legal_ner.utils.data import load_data


class TestTrainNer(TestCase):
    ANNOTATIONS_PATH = Path('data/annotations.txt')

    def test_load_data(self):
        data = load_data(self.ANNOTATIONS_PATH)
        self.assertEqual(2, len(data))
        self.assertEqual('Die Revision des Klägers gegen das Urteil des 6. Zivilsenats des Oberlandesgerichts Köln '
                         'vom 16. Dezember 2016 wird zurückgewiesen.', data[0][0])
        self.assertEqual([(65, 88, 'ORG')], data[0][1]['entities'])

    def test_train_overfit(self):
        data = load_data(self.ANNOTATIONS_PATH)
        nlp = spacy.load('de_core_news_sm')
        before_score = test(data, nlp, False)
        add_labels(nlp.get_pipe('ner'), get_ner_labels(data))
        train(data, 'ner', 10, nlp, True, True, 1, 0.0, 1.0)
        after_score = test(data, nlp, False)
        self.assertGreater(after_score, before_score)

    def test_train_blank(self):
        data = load_data(self.ANNOTATIONS_PATH)
        nlp = spacy.blank('de')
        add_pipe(nlp, 'ner')
        add_labels(nlp.get_pipe('ner'), get_ner_labels(data))
        train(data, 'ner', 1, nlp, True, True, 1, 0.0, 1.0)
