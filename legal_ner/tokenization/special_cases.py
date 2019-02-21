from spacy.symbols import ORTH, LEMMA, POS, TAG, NORM

special_cases = {
    u'Art.': [{ORTH: u'Art.', LEMMA: u'Artikel', NORM: u'Artikel', POS: u'NOUN'}],
    u'Urt.': [{ORTH: u'Urt.', LEMMA: u'Urteil', NORM: u'Urteil', POS: u'NOUN'}],
    u'Rn.': [{ORTH: u'Rn.', LEMMA: u'Randnummer', NORM: u'Randnummer', POS: u'NOUN'}],
    u'Aufl.': [{ORTH: u'Aufl.', LEMMA: u'Auflage', NORM: u'Auflage', POS: u'NOUN'}],
    u'n.F.': [{ORTH: u'n.', LEMMA: u'neue', NORM: u'neue', POS: u'ADJ'},
              {ORTH: u'F.', LEMMA: u'Fassung', NORM: u'Fassung', POS: u'NOUN'}],
    u'St.': [{ORTH: u'St.', LEMMA: u'Ständige', NORM: u'Ständige', POS: u'ADJ'}],
    u'Rspr.': [{ORTH: u'Rspr.', LEMMA: u'Rechtsprechung', NORM: u'Rechtsprechung', POS: u'NOUN'}],
    u'i.V.m.': [{ORTH: u'i.', LEMMA: u'in', NORM: u'in', POS: u'ADP'},
                {ORTH: u'V.', LEMMA: u'Verbindung', NORM: u'Verbindung', POS: u'NOUN'},
                {ORTH: u'm.', LEMMA: u'mit', NORM: u'mit', POS: u'ADP'}],
    u'lfd.': [{ORTH: u'lfd.', LEMMA: u'laufende', NORM: u'laufende', POS: u'ADJ'}],
    u'ff.': [{ORTH: u'ff.', LEMMA: u'fortfolgende', NORM: u'fortfolgende', POS: u'ADJ'}],
}
