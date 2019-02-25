from pathlib import Path

import oldp_client
import plac
from oldp_client.rest import ApiException
from spacy import displacy

from legal_ner.pipeline import Pipeline
from legal_ner.entity_extractors import HtmlEntityExtractor


@plac.annotations(
    api_key=('Key for the Open Legal Data API', 'option', 'k', str),
    case_id=('Id of the case to annotate', 'option', 'i', int),
    model=('Path to the spacy language model', 'option', 'm', Path),
)
def main(case_id, api_key, model=Path('models/legal-de')):
    configuration = oldp_client.Configuration()
    configuration.api_key['Authorization'] = api_key

    api_instance = oldp_client.ApiClient(configuration)
    cases_api = oldp_client.CasesApi(api_instance)

    try:
        case = cases_api.cases_read(case_id)
        print("Busy extracting entities for case {}...".format(case_id))
    except ApiException as e:
        print("Error when querying CasesApi: {}".format(e))
        return
    extractor = HtmlEntityExtractor(Pipeline(model))
    extractor.run(case.content)
    print("...finished!\n{} Entities found. Inspect results at: http://localhost:5000\n\nStop the server with "
          "CTRL+C".format(len(extractor.doc)))
    displacy.serve(extractor.doc, 'ent')  # TODO add colors colors={'per':'blue'}


if __name__ == '__main__':
    plac.call(main)
