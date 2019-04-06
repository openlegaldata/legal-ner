# German Legal-Domain Language Model

This model is based on [de_core_news_sm](https://spacy.io/models/de#de_core_news_sm) (License [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)) and has been 
additionally trained on NER data from the legal domain.

Training parameters:
- epochs = 4
- initial dropout rate = 0.5, linear decay
- intial batch size = 1, batch compound rate = 1.001
