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
            span._.set('regexp_match', value)
            new_ents += [span]

            if span in old_ents:
                old_ents.remove(span)
        doc.ents = old_ents + new_ents
        return doc

    def extract(self, text) -> Generator:
        for match in self.regexp.regexp_obj().finditer(text):
            yield (self.regexp.normalize(match.groupdict(), match.group(0)), match.start(), match.end())
