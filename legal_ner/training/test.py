def fscore(ents, true_ents):
    if len(ents) == 0 or len(true_ents) == 0:
        return 0.0

    true_positives = sum(1 for ent in ents if ent in true_ents)
    false_negatives = sum(1 for ent in true_ents if ent not in ents)
    false_positives = sum(1 for ent in ents if ent not in true_ents)
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    if (precision + recall) == 0:
        return 0.0

    return (2 * precision * recall) / (precision + recall)


def test(test_data, nlp, verbose):
    avg_score = 0.0
    for sent, ents in test_data:
        doc = nlp(sent)
        score = fscore([(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents], ents['entities'])
        avg_score += score
        if verbose:
            print("Sentence: {}".format(sent))
            print("  Entities: {}".format([(ent.text, ent.label_) for ent in doc.ents]))
            print("  Tokens: {}".format([t.text for t in doc]))
            print("  F-Score: {}\n".format(score))

    avg_score /= len(test_data)
    print("F-Score: {}".format(avg_score))
    return avg_score
