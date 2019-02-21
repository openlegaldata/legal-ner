from spacy.tokens import Span


class EntityRelationExtractor(object):

    def __init__(self, entities, model, noun_phrases=False):
        self.entities = entities
        self.model = model
        self.noun_phrases = noun_phrases
        if not Span.has_extension('entity_relation_subj'):
            Span.set_extension('entity_relation_subj', default='')
        if not Span.has_extension('entity_relation_root'):
            Span.set_extension('entity_relation_root', default='')

    def __call__(self, doc):
        merge_spans(doc.ents)
        if self.noun_phrases:
            merge_spans(doc.noun_chunks)

        for span in filter(lambda t: t.label_ in self.entities, doc.ents):
            token = span[0]
            if 'de' in self.model:
                relation = extract_relations_de(token)
            elif 'en' in self.model:
                relation = extract_relations_en(token)
            else:
                raise ValueError('Unsupported model {}!'.format(self.model))

            if relation:
                span._.set('entity_relation_subj', relation[0])
                span._.set('entity_relation_root', relation[1])
        return doc


def merge_spans(spans):
    for span in spans:
        span.merge()


def extract_relations_en(token):
    """https://spacy.io/api/annotation#dependency-parsing CLEAR Style"""
    if token.dep_ == 'dobj':
        # entity is attribute or direct object
        verb = token.head.lemma_
        subject = None
        for t in token.head.lefts:
            if t.dep_ == 'nsubj':
                subject = t.lemma_
        return subject, verb

    elif token.dep_ == 'pobj' and token.head.dep_ == 'prep':
        # entity is object of preposition
        verb = token.head.head.lemma_
        subject = None
        for t in token.head.head.lefts:
            if t.dep_ == 'nsubj':
                subject = t.lemma_
        return subject, verb


def extract_relations_de(token):
    """https://spacy.io/api/annotation#dependency-parsing TIGER Treebank"""
    if token.dep_ == 'oa':
        # entity is accusative object
        head = token.head
        while head.dep_ != 'ROOT':
            head = head.head
        verb = head.lemma_
        subject = None
        for t in head.children:
            if t.dep_ == 'sb':
                subject = t.lemma_
        return subject, verb

    elif token.dep_ == 'nk':
        # entity is noun kernel
        if token.head.dep_ == 'oa':
            # without noun chunking the nk may be part of the oa
            token.dep_ = 'oa'
            return extract_relations_de(token)

        prep = token.head.lemma_

        subject = None
        head = token.head
        while head.dep_ != 'ROOT':
            head = head.head
        for t in head.children:
            if t.dep_ == 'sb':
                subject = t.lemma_
        return subject, prep
