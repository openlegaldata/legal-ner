import re
from pathlib import Path

import plac
import srsly

from legal_ner.preprocessing import HtmlConcealer


def split_paragraphs(string):
    paragraph_delimiter = re.compile(r'\n')
    paragraphs = []
    while True:
        m = re.search(paragraph_delimiter, string)
        if m is None:
            paragraphs += [string]
            break
        paragraphs += [string[:m.start(0)]]
        string = string[m.end(0):]
    return paragraphs


@plac.annotations(
    input=('Path to json dump of oldp cases', 'option', 'i', Path),
    output=('Path to jsonl file with raw texts', 'option', 'o', Path)
)
def main(input: Path, output: Path):
    if not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)

    with input.open(mode='r') as in_f:
        with output.open(mode='w') as out_f:
            print("Preparing training data...")
            for line in in_f:
                json = srsly.json_loads(line)
                concealer = HtmlConcealer(json['content'])
                # the order is crucial
                concealer.replace_html_special_ents()
                concealer.remove_pattern(r'<br.*>', replace_with='\n')  # html linebreaks
                concealer.remove_pattern(r'<[^>]+>')  # html tags
                concealer.remove_pattern(r'\xa0+|\t| {2,}', replace_with=' ')  # white space
                concealer.remove_enumeration_numbers()
                concealer.remove_pattern(r'(^ +)|( +$)', flags=re.MULTILINE)  # leading or trailing whitespace
                concealer.remove_pattern(r'^[A-ZÄÜÖ]( [a-zäüö]){4,}( :)?$', flags=re.MULTILINE)  # whitespace
                # separated letters for headlines, e.g. T e n o r
                concealer.remove_pattern(r'\n{2,}', replace_with='\n')  # duplicate newlines
                concealer.remove_pattern(r'(^\n)|(\n$)')  # newline at start or end
                paragraphs = split_paragraphs(concealer.get_content())
                out_f.writelines(['{"text": "' + p + '"}\n' for p in paragraphs if len(p) > 10])
    print("...finished!")


if __name__ == '__main__':
    plac.call(main)
