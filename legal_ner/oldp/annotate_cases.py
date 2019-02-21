import oldp_client
import plac
from oldp_client.rest import ApiException

from legal_ner.entity_extractors import HtmlEntityExtractor


@plac.annotations(
    api_key=('Key for the Open Legal Data API', 'option', 'k', str),
    case_id=('Id of the case to annotate', 'option', 'i', int),
    slug=('Annotate the case for the given slug', 'option', 'u', str),
    file_number=('Annotate the case for the given file number', 'option', 'f', int),
    court=('Annotate all cases for the given court id', 'option', 'c', int),
    state=('Annotate all cases for the given state id', 'option', 's', int),
    trusted=('Make the results visible to every site user', 'flag', 't')
)
def main(api_key, case_id=None, slug=None, file_number=None, court=None, state=None,
         entities=('EURO', 'LOCATION', 'PERSON', 'ORGANIZATION', 'STAKEHOLDER', 'CAUSE', 'PERCENT', 'DATE'),
         model='../../models/legal-de',
         trusted=False):
    if len(entities) == 0:
        print('No entities given!')
        return

    kwargs = {'slug': slug, 'file_number': file_number, 'court': court, 'state': state, 'page_size': 1000}
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    configuration = oldp_client.Configuration()
    configuration.api_key['Authorization'] = api_key

    api_instance = oldp_client.ApiClient(configuration)
    cases_api = oldp_client.CasesApi(api_instance)
    case_annotations_api = oldp_client.CaseAnnotationsApi(api_instance)

    ent_count = 0

    if case_id:
        try:
            case = cases_api.cases_read(case_id)
            print("Busy extracting entities for case {}...".format(case_id))
        except ApiException as e:
            print("Error when querying CasesApi: {}".format(e))
            return
        extract(case, case_annotations_api, ent_count, entities, model)
    else:
        page = 1
        while True:
            try:
                cases_response = cases_api.cases_list(**kwargs, page=page)
                if page == 1:
                    print("There were {} cases found for your parameters. Busy extracting entities...".format(
                        cases_response.count))
                cases = cases_response.results
            except ApiException as e:
                if e.status == 404:
                    break
                print("Error when querying CasesApi: {}".format(e))
                return

            if len(cases) == 0:
                print("No cases found for given parameters!")
                return

            for case in cases:
                extract(case, case_annotations_api, ent_count, entities, model)

    print("...finished!\n{} entities extracted and sent to the Open Legal Data Platform!")


def extract(case, case_annotations_api, ent_count, entities, model):
    extractor = HtmlEntityExtractor(model=model)
    extractor.run(case.content)
    for entity_type in entities:
        entities = extractor.get_entities(entity_type)
        for (value, start, end) in entities:
            data = oldp_client.CaseAnnotation()
            data.belongs_to = case.id
            data.label = entity_type
            data.value_str = str(value)
            # TODO param trusted = True, start_char, end_char
            try:
                case_annotations_api.case_annotations_create(data)
                ent_count += 1
            except ApiException as e:
                print("Error when sending data to CaseAnnotationsApi: {}".format(e))


if __name__ == '__main__':
    plac.call(main)
