import random
from pathlib import Path

import plac
import spacy
from spacy.util import minibatch, compounding

from legal_ner.utils.data import load_data
from legal_ner.training.test import test

INSTALLED_MODELS = {'de': 'de_core_news_sm', 'en': 'en_core_web_sm'}


def train(train_data, pipe, n_epochs, nlp, blank_model, verbose, init_batch_size, init_dropout_rate, batch_comp_rate):
    max_batch_size = len(train_data)

    other_pipes = [p for p in nlp.pipe_names if p != pipe]
    with nlp.disable_pipes(*other_pipes):
        if blank_model:
            nlp.begin_training()

        for epoch in range(1, n_epochs + 1):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=compounding(init_batch_size, max_batch_size, batch_comp_rate))
            dropout = linear_decay(init_dropout_rate, epoch)
            for batch in batches:
                texts, labels = zip(*batch)
                nlp.update(
                    texts,
                    labels,
                    drop=dropout,
                    losses=losses,
                )
            if verbose:
                print('Epoch {} - Loss: {}'.format(epoch, losses['ner']))
                test(train_data, nlp, False)


def linear_decay(rate, epoch, decay=1.0):
    return rate / (epoch * decay)


def add_pipe(nlp, pipe, last=True):
    ner = nlp.create_pipe(pipe)
    nlp.add_pipe(ner, last=last)


def get_ner_labels(data):
    for _, annotations in data:
        for ent in annotations.get('entities'):
            yield ent[2]


def add_labels(pipe, labels):
    for label in labels:
        pipe.add_label(label)


def save_model(nlp, path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(path)


@plac.annotations(
    train_data_dir=('Training data directory', 'option', 't', Path),
    test_data_dir=('Optional test data directory', 'option', 'l', Path),
    output_dir=('Optional output directory', 'option', 'o', Path),
    lang=('Model language', 'option'),
    blank_model=('Train a blank model or base training on existing model', 'flag', 'b'),
    verbose=('Print detailed training progress', 'flag', 'v'),
    epochs=('Number of training epochs', 'option', 'e', int),
    init_batch_size=('Initial size of mini batches', 'option', 'm', int),
    init_dropout_rate=('Initial dropout rate', 'option', 'd', float),
    batch_comp_rate=('Batch compound rate', 'option', 'c', float),
)
def main(train_data_dir, test_data_dir=None, output_dir=None, lang='de', blank_model=False, verbose=False, epochs=100,
         init_batch_size=1, init_dropout_rate=0.5, batch_comp_rate=1.001):
    if blank_model:
        nlp = spacy.blank(INSTALLED_MODELS[lang])
        add_pipe(nlp, 'ner')
    else:
        nlp = spacy.load(INSTALLED_MODELS[lang])

    train_data = load_data(train_data_dir)
    add_labels(nlp.get_pipe('ner'), get_ner_labels(train_data))

    train(train_data, 'ner', epochs, nlp, blank_model, verbose, init_batch_size, init_dropout_rate, batch_comp_rate)

    if test_data_dir is not None:
        test_data = load_data(test_data_dir)
        print('\nPerformance on test data:')
        test(test_data, nlp, False)

    if output_dir:
        save_model(nlp, output_dir)


if __name__ == '__main__':
    plac.call(main)
