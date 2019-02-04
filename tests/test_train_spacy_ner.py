from pathlib import Path
from unittest import TestCase

import spacy

from train_spacy_ner import load_data, train, add_labels, get_ner_labels, add_pipe, test


class TestTrainSpacy(TestCase):

    def test_load_data(self):
        data = load_data(Path('data/annotations.txt'))
        print(data)
        self.assertEqual(2, len(data))
        self.assertEqual('Die Revision des Klägers gegen das Urteil des 6. Zivilsenats des Oberlandesgerichts Köln '
                         'vom 16. Dezember 2016 wird zurückgewiesen.', data[0][0])
        self.assertEqual([(65, 88, 'ORG')], data[0][1]['entities'])

    def test_train_overfit(self):
        data = load_data(Path('data/annotations.txt'))
        nlp = spacy.load('de_core_news_sm')
        before_score = test(data, nlp, False)
        add_labels(nlp.get_pipe('ner'), get_ner_labels(data))
        train(data, 'ner', 100, nlp, True, True, 1, 0.5, 1.001)
        after_score = test(data, nlp, False)
        self.assertGreater(after_score, before_score)

    def test_train_blank(self):
        data = load_data(Path('data/annotations.txt'))
        nlp = spacy.blank('de')
        add_pipe(nlp, 'ner')
        add_labels(nlp.get_pipe('ner'), get_ner_labels(data))
        train(data, 'ner', 1, nlp, True, True, 1, 0.0, 1.0)
