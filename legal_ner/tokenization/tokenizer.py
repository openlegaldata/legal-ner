from spacy.tokenizer import Tokenizer
from spacy.util import compile_suffix_regex, compile_infix_regex, compile_prefix_regex

custom_suffixes = [
    r'^[A-Z]\d.$',  # Ehefrau W1.
    r'^\w+\.?-\w+\.$',  # Schl.-Holst.
    r'^\d{1,2}\.$',  # 20. Februar
]


def create_custom_tokenizer(nlp):
    prefixes = compile_prefix_regex(nlp.Defaults.prefixes)
    infixes = compile_infix_regex(nlp.Defaults.infixes)
    suffixes = compile_suffix_regex(tuple(list(nlp.Defaults.suffixes) + custom_suffixes))

    return Tokenizer(nlp.vocab,
                     rules=nlp.Defaults.tokenizer_exceptions,
                     prefix_search=prefixes.search,
                     infix_finditer=infixes.finditer,
                     suffix_search=suffixes.search,
                     token_match=None)
