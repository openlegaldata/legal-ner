from spacy.symbols import ORTH, LEMMA, POS, TAG

# https://spacy.io/usage/linguistic-features#adding-patterns-attributes

party = [[{LEMMA: 'Kläger'}],
         [{LEMMA: 'Beklagte'}]]

reasoning = [[{ORTH: 'weil'}],
             [{ORTH: 'denn'}],
             [{ORTH: 'da'}]]
