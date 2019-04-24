from spacy.pipeline import EntityRuler


def prepare_patterns(patterns, label):
    entity_ruler_patterns = []
    for pattern in patterns:
        entity_ruler_patterns += [{"label": label, "pattern": pattern}]
    return entity_ruler_patterns


def init_entity_ruler(nlp, patterns, label):
    string_store = nlp.vocab.strings
    if label not in string_store:
        string_store.add(label)

    ruler = EntityRuler(nlp)
    ruler.add_patterns(prepare_patterns(patterns, label))
    return ruler
