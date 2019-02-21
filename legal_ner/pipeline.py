import spacy

from legal_ner.ner.matcher import EntityMatcher
from legal_ner.ner.regexp_matcher import RegexpEntityMatcher
from legal_ner.ner.regexps.dates import GermanDates
from legal_ner.ner.regexps.money import GermanEuros
from legal_ner.ner.regexps.percents import GermanPercentages
from legal_ner.ner.patterns import stakeholder, cause
from legal_ner.tokenization.special_cases import special_cases
from legal_ner.tokenization.tokenizer import create_custom_tokenizer


def run(model, text):
    nlp = spacy.load(model)

    nlp.tokenizer = create_custom_tokenizer(nlp)
    for word, special_case in special_cases.items():
        nlp.tokenizer.add_special_case(word, special_case)

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
