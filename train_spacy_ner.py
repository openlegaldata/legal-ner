import json
import random
from pathlib import Path

import plac
import spacy
from spacy.util import minibatch, compounding

INSTALLED_MODELS = {'de': 'de_core_news_sm', 'en': 'en_core_web_sm'}


def fscore(ents, true_ents):
    if len(ents) == 0 or len(true_ents) == 0:
        return 0.0

    true_positives = sum(1 for ent in ents if ent in true_ents)
    false_negatives = sum(1 for ent in true_ents if ent not in ents)
    false_positives = sum(1 for ent in ents if ent not in true_ents)
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    if (precision + recall) == 0:
        return 0.0

    return (2 * precision * recall) / (precision + recall)


def test(test_data, nlp, verbose):
    avg_score = 0.0
    for sent, ents in test_data:
        doc = nlp(sent)
        score = fscore([(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents], ents['entities'])
        avg_score += score
        if verbose:
            print("Sentence: {}".format(sent))
            print("  Entities: {}".format([(ent.text, ent.label_) for ent in doc.ents]))
            print("  Tokens: {}".format([t.text for t in doc]))
            print("  F-Score: {}\n".format(score))

    avg_score /= len(test_data)
    print("F-Score: {}".format(avg_score))
    return avg_score


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


def linear_decay(initial_dropout_rate, epoch, decay=1.0):
    return initial_dropout_rate / (epoch * decay)


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


def load_data(data_dir: Path):  # TODO possibly make data_dir to path
    if not data_dir.exists():
        raise ValueError("Invalid path given: {}".format(data_dir))

    data = []
    with data_dir.open('r') as file:
        for line in file:
            json_dict = json.loads(line)
            sent = json_dict['text']
            ents = [(item[0], item[1], item[2]) for item in json_dict['entities']]
            data += [(sent, {'entities': ents})]
    return data


def save_model(nlp, path: Path):
    if not path.exists():
        path.mkdir()
    nlp.to_disk(path)


@plac.annotations(
    data_dir=('Training data directory', 'option', 't', Path),
    output_dir=('Optional output directory', 'option', 'o', Path),
    lang=('Model language', 'option', 'l'),
    blank_model=('Train a blank model or base training on existing model', 'flag', 'b'),
    verbose=('Print detailed training progress', 'flag', 'v'),
    epochs=('Number of training epochs', 'option', 'e', int),
    init_batch_size=('Initial size of mini batches', 'option', 'm', int),
    init_dropout_rate=('Initial dropout rate', 'option', 'd', float),
    batch_comp_rate=('Batch compound rate', 'option', 'c', float),
)
def main(data_dir, output_dir=None, lang='de', blank_model=False, verbose=False, epochs=100, init_batch_size=1,
         init_dropout_rate=0.5, batch_comp_rate=1.001):
    if blank_model:
        nlp = spacy.blank(INSTALLED_MODELS[lang])
        add_pipe(nlp, 'ner')
    else:
        nlp = spacy.load(INSTALLED_MODELS[lang])

    data = load_data(data_dir)
    add_labels(nlp.get_pipe('ner'), get_ner_labels(data))

    # TODO split data
    train_data = data
    test_data = data

    train(train_data, 'ner', epochs, nlp, blank_model, verbose, init_batch_size, init_dropout_rate, batch_comp_rate)

    test(test_data, nlp, verbose)

    if output_dir:
        save_model(nlp, output_dir)


if __name__ == '__main__':
    plac.call(main)
