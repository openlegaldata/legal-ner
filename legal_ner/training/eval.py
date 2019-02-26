from pathlib import Path

import plac
import spacy

from legal_ner.utils.data import load_data
from legal_ner.training.test import test

INSTALLED_MODELS = {'de': 'de_core_news_sm', 'en': 'en_core_web_sm'}


@plac.annotations(
    test_data_dir=('Test data directory', 'option', 'l', Path),
    model=('Name of installed model or directory', 'option', 'm', Path),
    verbose=('Print detailed training progress', 'flag', 'v'),
)
def main(test_data_dir, model='de', verbose=False):
    if model in INSTALLED_MODELS:
        model = INSTALLED_MODELS['de']

    nlp = spacy.load(model)
    test_data = load_data(test_data_dir)
    test(test_data, nlp, verbose)


if __name__ == '__main__':
    plac.call(main)
