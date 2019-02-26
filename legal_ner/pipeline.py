from abc import abstractmethod

import spacy

from legal_ner.ner.pattern_based import PatternBasedMatcher
from legal_ner.ner.regexp_based import RegexpBasedMatcher
from legal_ner.ner.regexps.dates import GermanDates
from legal_ner.ner.regexps.money import GermanEuros
from legal_ner.ner.regexps.percents import GermanPercentages
from legal_ner.ner.matcher_patterns import party, reasoning, action, forbearance, bgb_at
from legal_ner.tokenization.special_cases import special_cases
from legal_ner.tokenization.tokenizer import create_custom_tokenizer


class Entity:
    # statistical
    PER = 'PER'
    LOC = 'LOC'
    ORG = 'ORG'
    MISC = 'MISC'

    # pattern based
    PARTY = 'PARTY'
    REASONING = 'REASONING'
    ACTION = 'ACTION'
    FORBEARANCE = 'FORBEARANCE'
    BGB_AT = 'BGB_AT'

    # regexp based
    DATE = 'DATE'
    EURO = 'EURO'
    PERCENT = 'PERCENT'


class Pipeline:

    def __init__(self, model):
        self.model = model

    @abstractmethod
    def run(self, text):
        pass


class RuleBasedPipeline(Pipeline):

    def run(self, text):
        nlp = spacy.load(self.model)

        nlp.tokenizer = create_custom_tokenizer(nlp)
        for word, special_case in special_cases.items():
            nlp.tokenizer.add_special_case(word, special_case)

        nlp.remove_pipe('parser')
        nlp.remove_pipe('ner')

        party_matcher = PatternBasedMatcher(nlp, party, Entity.PARTY)
        nlp.add_pipe(party_matcher, name='party_matcher')

        reasoning_matcher = PatternBasedMatcher(nlp, reasoning, Entity.REASONING)
        nlp.add_pipe(reasoning_matcher, name='reasoning_matcher')

        action_matcher = PatternBasedMatcher(nlp, action, Entity.ACTION)
        nlp.add_pipe(action_matcher, name='action_matcher')

        forbearance_matcher = PatternBasedMatcher(nlp, forbearance, Entity.FORBEARANCE)
        nlp.add_pipe(forbearance_matcher, name='forbearance_matcher')

        bgb_at_matcher = PatternBasedMatcher(nlp, bgb_at, Entity.BGB_AT)
        nlp.add_pipe(bgb_at_matcher, name='bgb_at_matcher')

        date_matcher = RegexpBasedMatcher(nlp, Entity.DATE, GermanDates())
        nlp.add_pipe(date_matcher, name='regexp_dates_extractor')

        percents_matcher = RegexpBasedMatcher(nlp, Entity.EURO, GermanEuros())
        nlp.add_pipe(percents_matcher, name='regexp_euro_extractor')

        percents_matcher = RegexpBasedMatcher(nlp, Entity.PERCENT, GermanPercentages())
        nlp.add_pipe(percents_matcher, name='regexp_percent_extractor')

        doc = nlp(text)

        return doc


class StatisticalPipeline(Pipeline):

    def run(self, text):
        nlp = spacy.load(self.model)

        nlp.tokenizer = create_custom_tokenizer(nlp)
        for word, special_case in special_cases.items():
            nlp.tokenizer.add_special_case(word, special_case)

        doc = nlp(text)

        return doc
