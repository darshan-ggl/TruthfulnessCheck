import spacy
from truthfulnesscheck.config import config

spacy_target_labels = config['Spacy']['spacy_target_labels']


def places_extraction(inpt_text, spacy_model):
    # Model load
    spacy_nlp = spacy.load(spacy_model)

    # Extraction
    places_lst = []
    places_details = {}
    spcy_obj = spacy_nlp(inpt_text)
    for word in spcy_obj.ents:
        if word.label_ in spacy_target_labels:
            if word.label_ not in places_details.keys():
                places_details[word.label_] = []
            places_details[word.label_].extend([word.text])
            places_lst.extend([word.text])

    places_lst = list(set(places_lst))
    return places_lst, places_details
