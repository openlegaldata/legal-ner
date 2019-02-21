from spacy.symbols import ORTH, LEMMA, POS, TAG, NORM

special_cases = {
    u'Art.': [{ORTH: u'Art.', LEMMA: u'Artikel', NORM: u'Artikel', POS: u'NOUN'}],
    u'Urt.': [{ORTH: u'Urt.', LEMMA: u'Urteil', NORM: u'Urteil', POS: u'NOUN'}],
    u'Rn.': [{ORTH: u'Rn.', LEMMA: u'Randnummer', NORM: u'Randnummer', POS: u'NOUN'}],
    u'Aufl.': [{ORTH: u'Aufl.', LEMMA: u'Auflage', NORM: u'Auflage', POS: u'NOUN'}],
    u'n.F.': [{ORTH: u'n.F.', LEMMA: u'neue Fassung', NORM: u'neue Fassung', POS: u'NOUN'}],
    u'St.': [{ORTH: u'St.', LEMMA: u'Ständige', NORM: u'Ständige', POS: u'ADJ'}],
    u'Rspr.': [{ORTH: u'Rspr.', LEMMA: u'Rechtsprechung', NORM: u'Rechtsprechung', POS: u'NOUN'}],
    u'i.V.m.': [{ORTH: u'i.V.m.', LEMMA: u'in Verbindung mit', NORM: u'in Verbindung mit', POS: u'SCONJ'}],
    u'lfd.': [{ORTH: u'lfd.', LEMMA: u'laufende', NORM: u'laufende', POS: u'ADJ'}],
    u'ff.': [{ORTH: u'ff.', LEMMA: u'fortfolgende', NORM: u'fortfolgende', POS: u'ADJ'}],
}
