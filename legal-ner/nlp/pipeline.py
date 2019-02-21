import spacy

from nlp.ner.matcher import EntityMatcher
from nlp.ner.regexp_matcher import RegexpEntityMatcher
from nlp.ner.regexps.dates import GermanDates
from nlp.ner.regexps.money import GermanEuros
from nlp.ner.regexps.percents import GermanPercentages
from nlp.ner.patterns import *


def run(model, text):
    nlp = spacy.load(model)

    # TODO add custom tokenization and sentence segmentation
    # https://spacy.io/usage/linguistic-features#special-cases
    # https://spacy.io/usage/linguistic-features#sbd

    stakeholder_matcher = EntityMatcher(nlp, stakeholder, 'STAKEHOLDER')
    nlp.add_pipe(stakeholder_matcher, name='stakeholder_matcher', before='ner')

    cause_matcher = EntityMatcher(nlp, cause, 'CAUSE', mark_whole_sent=True)
    nlp.add_pipe(cause_matcher, name='cause_matcher', before='ner')

    date_matcher = RegexpEntityMatcher(nlp, 'DATE', GermanDates())
    nlp.add_pipe(date_matcher, name='regexp_dates_extractor', before='ner')

    percents_matcher = RegexpEntityMatcher(nlp, 'EURO', GermanEuros())
    nlp.add_pipe(percents_matcher, name='regexp_euro_extractor', before='ner')

    percents_matcher = RegexpEntityMatcher(nlp, 'PERCENT', GermanPercentages())
    nlp.add_pipe(percents_matcher, name='regexp_percent_extractor', before='ner')

    doc = nlp(text)

    return doc
