import spacy

from legal_ner.ner.rule_based import RuleBasedMatcher
from legal_ner.ner.regexp_based import RegexpBasedMatcher
from legal_ner.ner.regexps.dates import GermanDates
from legal_ner.ner.regexps.money import GermanEuros
from legal_ner.ner.regexps.percents import GermanPercentages
from legal_ner.ner.matcher_patterns import party, reasoning, action, forbearance, bgb_at
from legal_ner.tokenization.special_cases import special_cases
from legal_ner.tokenization.tokenizer import create_custom_tokenizer


ENTITIES = {
    # Language Model
    'PER':'',
    'LOC':'',
    'ORG':'',
    'MISC':'',
    # Regexps
    'PER':'',
    'PER':'',
    'PER':'',
    'PER':'',
    # Matcher Patterns
    'PER':'',
    'PER':'',
    'PER':'',
    'PER':'',
}

class Pipeline:

    def __init__(self, model):
        self.model = model

    def run(self, text):
        nlp = spacy.load(self.model)

        nlp.tokenizer = create_custom_tokenizer(nlp)
        for word, special_case in special_cases.items():
            nlp.tokenizer.add_special_case(word, special_case)

        party_matcher = RuleBasedMatcher(nlp, party, 'PARTY')
        nlp.add_pipe(party_matcher, name='party_matcher', after='ner')

        reasoning_matcher = RuleBasedMatcher(nlp, reasoning, 'REASONING')
        nlp.add_pipe(reasoning_matcher, name='reasoning_matcher', after='ner')

        action_matcher = RuleBasedMatcher(nlp, action, 'ACTION')
        nlp.add_pipe(action_matcher, name='action_matcher', after='ner')

        forbearance_matcher = RuleBasedMatcher(nlp, forbearance, 'FORBEARANCE')
        nlp.add_pipe(forbearance_matcher, name='forbearance_matcher', after='ner')

        bgb_at_matcher = RuleBasedMatcher(nlp, bgb_at, 'BGB_AT')
        nlp.add_pipe(bgb_at_matcher, name='bgb_at_matcher', after='ner')

        date_matcher = RegexpBasedMatcher(nlp, 'DATE', GermanDates())
        nlp.add_pipe(date_matcher, name='regexp_dates_extractor', after='ner')

        percents_matcher = RegexpBasedMatcher(nlp, 'EURO', GermanEuros())
        nlp.add_pipe(percents_matcher, name='regexp_euro_extractor', after='ner')

        percents_matcher = RegexpBasedMatcher(nlp, 'PERCENT', GermanPercentages())
        nlp.add_pipe(percents_matcher, name='regexp_percent_extractor', after='ner')

        doc = nlp(text)

        return doc
