from typing import Generator

from spacy.tokens import Span

from nlp.ner.regexps.base import Regexp


class RegexpEntityMatcher(object):

    def __init__(self, nlp, label, regexp: Regexp):
        self.regexp = regexp
        self.label = nlp.vocab.strings[label]

        if not Span.has_extension('regexp_match'):
            Span.set_extension('regexp_match', default='')

    def __call__(self, doc):
        new_ents = []
        for value, start, end in self.extract(doc.text):
            span = doc.char_span(start, end, label=self.label)
            span._.set('regexp_match', value)
            new_ents += [span]
        doc.ents = list(doc.ents) + new_ents
        return doc

    def extract(self, text) -> Generator:
        for match in self.regexp.regexp_obj().finditer(text):
            yield (self.regexp.normalize(match.groupdict(), match.group(0)), match.start(), match.end())

