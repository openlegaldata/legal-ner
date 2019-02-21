from oldp.apps.nlp.base import SpacyNLP


def lemmatize(noun: str, lang='de'):  # TODO
    nlp = SpacyNLP(lang=lang)
    container = nlp.process(noun)
    return next(container.lemmas())


def lemmas(word_tuple, lang='de'):
    if word_tuple is None:
        return None

    lemmatized_words = ()
    for word in word_tuple:
        lemmatized_words += (lemmatize(word, lang=lang),)
    return lemmatized_words
