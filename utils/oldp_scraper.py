from pathlib import Path

import oldp_client
import plac

from nlp.preprocessing import remove_whitespace, remove_pattern, replace_html_special_ents


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


if __name__ == '__main__':
    plac.call(main)
