from spacy.matcher import Matcher
from spacy.tokens import Span


class PatternBasedMatcher(object):

    def __init__(self, nlp, patterns, label):
        string_store = nlp.vocab.strings
        if label not in string_store:
            string_store.add(label)
        self.label = string_store[label]

        self.matcher = Matcher(nlp.vocab)
        for pattern in patterns:
            self.matcher.add(self.label, None, pattern)

    def __call__(self, doc):
        new_ents = []
        old_ents = list(doc.ents)

        for _, start, end in self.matcher(doc):
            span = Span(doc, start, end, label=self.label)
            new_ents += [span]

        doc.ents = list(set(old_ents + new_ents))
        return doc
