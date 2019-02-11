# German Legal-Domain Language Model

This model is based on [de_core_news_sm](https://spacy.io/models/de#de_core_news_sm) (License [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)) and has been 
additionally 
trained on NER data from the legal domain `data/train.txt`.

Training parameters:
- epochs = 4
- initial dropout rate = 0.5, linear decay
- intial batch size = 1, batch compound rate = 1.001

Test performance on legal domain data `data/test.txt`:
| Model | F-Score |
| ----- | ------- |
| de_core_news_sm | 0.351 |
| de_core_news_sm + legal training | 0.817 |

_Note_: These metrics are based on a small test dataset and computed without cross-validation.
