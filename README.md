# Named Entity Recognition for the Legal Domain

### Dependencies

Get a copy of the repository:
```
$ git clone git@github.com:openlegaldata/legal-ner.git
```

Before getting started you have to install the Python dependencies, which will also install the required language 
models.
```
$ cd legal-ner
$ pipenv --python 3.7
$ pipenv install
```

To be able to run python scripts the project root needs to be added to the python module search path.
```
$ export PYTHONPATH=$PWD
```

All python statements below should be run in the shell provided by pipenv.
```
$ pipenv shell
```

## Extract Entities

To extract entities for the [Open Legal Data Platform (OLDP)](https://openlegaldata.io) run:
```
$ python legal_ner/oldp/annotate.py -k=your_api_key -p
```
To get more information about the usage run:
```
$ python legal_ner/oldp/annotate.py --help
```

You can also extract and locally visualize entities for a single case using:
```
$ python legal_ner/oldp/visualize.py -k=your-your_api_key-key -i=case_id
```


## Training your Model

### Obtaining Data

You can download cases from the OLDP website using:
```
$ python legal_ner/utils/oldp_scraper.py -o=data -k=your_api_key -c=case_id_1,case_id2,...
```

The data has to be annotated in the following format:
```json
{
  "text": "Denn das FG hat --wie oben dargelegt-- bindend festgestellt, dass die Klägerin das Motorrad gerade nicht zur Ausfuhr, sondern zur Nutzung in den USA erworben hat.",
  "entities": [[9, 11, "ORG"], [145, 148, "LOC"]],
}
```

Each line contains one json object. Store the labeled sentences in `data/annotations.txt` and split them into a 
training and testing dataset with:
```
$ python legal_ner/utils/split_data.py --data=data/annotations.txt --train=data/train.txt --test=data/test.txt
```

### Training
Currently only the NER module can be trained. The following command loads the training and test datasets from `data/` 
and 
saves the trained model to `models/legal-de`.
```
$ python legal_ner/training/train_ner.py -t=data/train.txt -l=data/test.txt --epochs=4 -o=models/legal-de -v
```


### Evaluation

You can evaluate the performance on a given model (e.g. `models/legal-de`) by providing an evaluation dataset (e.g. 
`data/test.txt`) and 
running:
```
$ python eval.py -l=data/test.txt -m=models/legal-de
```


## Pretrained Language Models
This repository hosts its own pretrained language models, specific for the German legal domain:
- [German Legal-Domain Language Model](https://github.com/openlegaldata/legal-ner/tree/master/models/legal-de)

Usage:
```
import spacy
nlp = spacy.load(path_to_model)
```
