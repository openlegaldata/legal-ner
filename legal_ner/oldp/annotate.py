import oldp_client
import plac
from oldp_client.rest import ApiException

from legal_ner.entity_extractors import HtmlEntityExtractor
from legal_ner.pipeline import RuleBasedPipeline, Entity


@plac.annotations(
    api_key=('Key for the Open Legal Data API', 'option', 'k', str),
    slug=('Annotate the case for the given slug', 'option', 'u', str),
    file_number=('Annotate the case for the given file number', 'option', 'f', int),
    court=('Annotate all cases for the given court id', 'option', 'c', int),
    state=('Annotate all cases for the given state id', 'option', 's', int),
    publish=('Push the results visible to the Open Legal Data Site', 'flag', 'p'),
    trusted=('Make the results visible to every site user', 'flag', 't'),
    model=('Path to the spacy language model', 'option', 'm', str),
    entities=('Comma separated list of entity names to extract', 'option', 'e', str)
)
def main(api_key, slug=None, file_number=None, court=None, state=None, trusted=False, publish=False,
         model='models/legal-de', entities=''):
    entity_types = entities.split(',')
    if len(entity_types) == 0:
        entity_types = [prop for prop in vars(Entity) if not prop.startswith('__')]

    kwargs = {'slug': slug, 'file_number': file_number, 'court': court, 'court__state': state, 'page_size': 100}
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    configuration = oldp_client.Configuration()
    configuration.api_key['Authorization'] = api_key

    api_instance = oldp_client.ApiClient(configuration)
    cases_api = oldp_client.CasesApi(api_instance)

    ent_count = 0
    page = 1
    print('Querying API...')
    while True:  # batch processing on per-page level
        try:
            cases_response = cases_api.cases_list(**kwargs, page=page)
            if page == 1:
                print("...There were {} cases found for your parameters.\nBusy extracting entities...".format(
                    cases_response.count))
            cases = cases_response.results
            page += 1
        except ApiException as e:
            if e.status == 404:
                break
            print("Error when querying CasesApi: {}".format(e))
            return

        if len(cases) == 0:
            print("No cases found for given parameters!")
            return

        entities = []
        for case in cases:
            entities = annotate(case, entities, entity_types, RuleBasedPipeline(model=model))
            # entities = annotate(case, entities, entity_types, StatisticalPipeline(model=model))
            break
        for (value, start, end, entity_type, case_id) in entities:
            ent_count += 1
            if publish:
                case_annotations_api = oldp_client.CaseAnnotationsApi(api_instance)
                push_to_oldp(case_annotations_api, case_id, value, start, end, entity_type, trusted)
            else:
                print("{}: {} [{}:{}]".format(entity_type, value, start, end))

    print("...finished!\n{} entities found for labels {}!".format(ent_count))


def annotate(case, entities, entity_types, pipeline):
    extractor = HtmlEntityExtractor(pipeline)
    extractor.run(case.content)
    for entity_type in entity_types:
        entities += list(map(lambda ent: ent + (entity_type, case.id), extractor.get_entities(entity_type)))
    return entities


def push_to_oldp(case_annotations_api, case_id, value, start, end, entity_type, trusted):
    data = oldp_client.CaseAnnotation()
    data.belongs_to = case_id
    data.label = entity_type
    data.value_str = str(value)
    # TODO param trusted = True, start_char, end_char
    try:
        case_annotations_api.case_annotations_create(data)
    except ApiException as e:
        print("Error when sending data to CaseAnnotationsApi: {}".format(e))


if __name__ == '__main__':
    plac.call(main)
