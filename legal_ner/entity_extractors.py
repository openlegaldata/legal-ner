from typing import Generator

from legal_ner import pipeline
from legal_ner.preprocessing import HtmlConcealer


class EntityExtractor:

    def __init__(self, model='de_core_news_sm'):
        self.model = model
        self.doc = None

    def run(self, text):
        self.doc = pipeline.run(self.model, text)

    def get_entities(self, entity_type) -> Generator:
        for ent in self.doc.ents:
            if entity_type == ent.label_:
                yield (ent.text, ent.start_char, ent.end_char)


class HtmlEntityExtractor(EntityExtractor):
    html_concealer = None

    def run(self, text):
        self.html_concealer = HtmlConcealer(text)
        self.html_concealer.conceal()
        super().run(self.html_concealer.get_content())

    def get_entities(self, entity_type) -> Generator:
        for (value, start, end) in super().get_entities(entity_type):
            start, end = self.html_concealer.concealed_to_html_pos(start, end)
            yield value, start, end
