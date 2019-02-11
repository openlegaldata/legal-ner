import html
import re
from pathlib import Path

import oldp_client
import plac


@plac.annotations(
    output_dir=('Directory to store the files in', 'option', 'o', Path),
    api_key=('Key for the Open Legal Data API', 'option', 'k', str),
    cases=('Case ids to scrape', 'option', 'c', str)
)
def main(output_dir: Path, api_key: str, cases: str):
    if not output_dir.exists():
        output_dir.mkdir()

    case_ids = cases.split(',')

    conf = oldp_client.Configuration()
    conf.api_key['api_key'] = api_key
    api_client = oldp_client.ApiClient(conf)
    cases_api = oldp_client.CasesApi(api_client)

    for case_id in case_ids:
        case = cases_api.cases_read(case_id)

        filepath = output_dir / "case_{}.txt".format(case_id)
        with filepath.open("w", encoding="utf-8") as f:
            content = case.content
            content = remove_pattern(content, r'<br.*>', replace_with='\n')
            content = remove_pattern(content, r'<[^>]+>')
            content = replace_html_special_ents(content)
            content = remove_whitespace(content)
            f.write(content)


def remove_whitespace(content):
    content = re.sub(r'( |\xa0)+', ' ', content)
    return '\n'.join([s for s in content.splitlines() if s.strip()])


def remove_pattern(content, regex, replace_with=''):
    pattern = re.compile(regex)
    while True:
        m = re.search(pattern, content)
        if m is None:
            break
        content = content[:m.start(0)] + replace_with + content[m.end(0):]
    return content


def replace_html_special_ents(content):
    pattern = re.compile(r'&#\d{1,4};|&\w{1,6};')
    while True:
        m = re.search(pattern, content)
        if m is None:
            break
        unicode = html.unescape(m.group(0))
        content = content[:m.start(0)] + unicode + content[m.end(0):]
    return content


if __name__ == '__main__':
    plac.call(main)
