from typing import Generator

from spacy.tokens import Span

from legal_ner.ner.regexps.base import Regexp


class RegexpBasedMatcher(object):

    def __init__(self, nlp, label, regexp: Regexp):
        string_store = nlp.vocab.strings
        if label not in string_store:
            string_store.add(label)
        self.label = string_store[label]

        self.regexp = regexp

        if not Span.has_extension('regexp_match'):
            Span.set_extension('regexp_match', default='')

    def __call__(self, doc):
        new_ents = []
        old_ents = list(doc.ents)

        for value, start, end in self.extract(doc.text):
            span = doc.char_span(start, end, label=self.label)
            if span is None:
                # TODO why can some spans not be created?
                print('Span was none for value {}'.format(value))
                continue
            span._.set('regexp_match', value)
            new_ents += [span]

        doc.ents = old_ents + new_ents
        return doc

    def extract(self, text) -> Generator:
        for match in self.regexp.regexp_obj().finditer(text):
            try:
                value = self.regexp.normalize(match.groupdict(), match.group(0))
            except Exception as e:
                print(e)
                continue
            yield (value, match.start(), match.end())
