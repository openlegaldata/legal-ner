from pathlib import Path

import numpy as np
import plac


@plac.annotations(
    data=('Path for file containing all available training/test data', 'option', 'd', Path),
    train=('Path to store training data in', 'option', 't', Path),
    test=('Path to store test data in', 'option', 'l', Path),
    split=('Amount of data to use for testing purposes', 'option', 's', float)
)
def main(data: Path, train: Path, test: Path, split=0.1):
    if not data.exists():
        raise ValueError('Given data path does not exist! {}'.format(data))

    train_data = ''
    test_data = ''
    np.random.seed(0)
    with data.open("r") as file:
        for line in file:
            if np.random.random() > split:
                train_data += line
            else:
                test_data += line
    write_to_file(train, train_data)
    write_to_file(test, test_data)


def write_to_file(path: Path, string):
    with path.open('w+', encoding='utf-8') as file:
        file.write(string)


if __name__ == '__main__':
    plac.call(main)
