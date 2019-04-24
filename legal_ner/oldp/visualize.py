import oldp_client
import plac
from oldp_client.rest import ApiException
from spacy import displacy

from legal_ner.entity_extractors import HtmlEntityExtractor
from legal_ner.pipelines import RuleBasedPipeline, StatisticalPipeline, Entity, JoinedPipeline


@plac.annotations(
    api_key=('Key for the Open Legal Data API', 'option', 'k', str),
    case_id=('Id of the case to annotate', 'option', 'i', int),
    model=('Path to the spacy language model', 'option', 'm', str),
    pipe=('The pipeline to use. Either "statistical", "rulebased" or "joined"', 'option', 'p', str)
)
def main(case_id, api_key, pipe, model='models/legal-de'):
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

    if pipe == 'statistical':
        pipeline = StatisticalPipeline(model)
    elif pipe == 'rulebased':
        pipeline = RuleBasedPipeline(model)
    elif pipe == 'joined':
        pipeline = JoinedPipeline(model)
    else:
        raise ValueError('Unknown pipeline {}!'.format(pipe))

    extractor = HtmlEntityExtractor(pipeline)
    extractor.run(case.content)
    print("...finished!\n{} Entities found. Inspect results at: http://localhost:5000\n\nStop the server with "
          "CTRL+C".format(len(extractor.doc)))
    displacy.serve(extractor.doc, 'ent', options={'colors': {Entity.PER: '#BF3F3F',
                                                             Entity.LOC: '#3FBF3F',
                                                             Entity.ORG: '#BF3FBF',
                                                             Entity.PARTY: '#3FBF7F',
                                                             Entity.REASONING: '#7F3FBF',
                                                             Entity.ACTION: '#BF3F7F',
                                                             Entity.FORBEARANCE: '#3F3FBF',
                                                             Entity.BGB_AT: '#3FBFBF',
                                                             Entity.DATE: '#7FBF3F',
                                                             Entity.EURO: '#BF7F3F',
                                                             Entity.PERCENT: '#BF3F3F'}})


if __name__ == '__main__':
    plac.call(main)
