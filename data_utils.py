import json
from pathlib import Path


def load_data(data_dir: Path):
    if not data_dir.exists():
        raise ValueError("Invalid path given: {}".format(data_dir))

    data = []
    with data_dir.open('r') as file:
        for line in file:
            json_dict = json.loads(line)
            sent = json_dict['text']
            ents = [(item[0], item[1], item[2]) for item in json_dict['entities']]
            data += [(sent, {'entities': ents})]
    return data
