from truthfulnesscheck.config import config
from vertexai.language_models import TextGenerationModel

from truthfulnesscheck.utils.NER_util import places_extraction
from truthfulnesscheck.utils.maps_util import places_existence
from truthfulnesscheck.utils.string_matcher_util import fuzzy_wuzzy_check
from truthfulnesscheck.utils.llm_util import llm_place_check

spacy_model_name = config['Spacy']['spacy_model']
simple_ratio_threshold = config["FuzzyWuzzy"]["simple_ratio_threshold"]


def validate_place(plc_resp, current_place):
    for i in plc_resp['predictions']:
        recom_place = i["description"].split(",")[0]
        if fuzzy_wuzzy_check(place1=current_place, place2=recom_place, simple_ratio_threshold=simple_ratio_threshold)[0]:
            return {"place_exist": True, 'description': "place exist"}
    return {"place_exist": False, 'description': "place does not exist"}


def places_check(input_text, city, radius, filter_place_type='establishment'):
    # LLM initialization
    llm = TextGenerationModel.from_pretrained("text-bison@001")

    places_validation = {}

    # Places captured
    places, place_dict = places_extraction(input_text, spacy_model=spacy_model_name)

    for place in places:
        print(f"For: {place} check in {city}")
        # Maps api and radius check
        plc_resp = places_existence(place=place, centric_city=city, radius=radius, strictbounds=True,
                                    types=filter_place_type)

        # Validate place with fuzzywuzzy
        validation_resp = validate_place(plc_resp, place)

        # Maps validation
        if validation_resp['place_exist']:
            places_validation[place] = validation_resp
        else:
            # LLM validation
            llm_resp = llm_place_check(place=place, city=city, model=llm)
            print("llm_resp: ", llm_resp)
            llm_validation = eval(llm_resp)
            places_validation[place] = llm_validation

    return places_validation
