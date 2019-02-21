from spacy.matcher import Matcher
from spacy.tokens import Span


class EntityMatcher(object):

    def __init__(self, nlp, patterns, label, mark_whole_sent=False):
        self.mark_sent = mark_whole_sent
        self.label = nlp.vocab.strings[label]
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add(self.label, None, patterns)

    def __call__(self, doc):
        new_ents = []
        for _, start, end in self.matcher(doc):
            span = Span(doc, start, end, label=self.label)

            if self.mark_sent:
                span = span.sent
            new_ents += [span]
        doc.ents = list(doc.ents) + new_ents
        return doc
