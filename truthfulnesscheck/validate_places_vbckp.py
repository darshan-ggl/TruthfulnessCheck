import yaml
import logging
import requests

# Spacy
import spacy

# FuzzyWuzzy
from fuzzywuzzy import fuzz

# VertexAI
from google.cloud import aiplatform as vertexai
from vertexai.language_models import TextGenerationModel

# TODO: fix the config yaml file path
# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Access configuration parameters
PROJECT_ID = config.get('PROJECT_ID')
region = config.get('location')
API_KEY = config.get('MAPS_API_KEY')
radius = config.get('radius')
simple_ratio_threshold = config.get('simple_ratio_threshold')
spacy_model_name = config.get('spacy_model')
geocode_url = config.get('geocode_url')
autocomplete_url = config.get('autocomplete_url')

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=region)


def places_extraction(inpt_text, spacy_model=spacy_model_name):  # en_core_web_lg

    # Model load
    spacy_nlp = spacy.load(spacy_model)

    # Extraction
    places_lst = []
    places_details = {}
    spcy_obj = spacy_nlp(inpt_text)
    for word in spcy_obj.ents:
        if word.label_ in ["GPE", "FAC", "LOC"]:  # "ORG"
            if word.label_ not in places_details.keys():
                places_details[word.label_] = []
            places_details[word.label_].extend([word.text])
            places_lst.extend([word.text])

    places_lst = list(set(places_lst))
    return places_lst, places_details


def get_lat_lng(city_name, api_key=API_KEY):
    params = {
        "address": city_name,
        "key": api_key
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return f"{lat}, {lng}"
    else:
        return None


def fuzzy_wuzzy_check(place1, place2, simple_ratio_threshold=simple_ratio_threshold):
    print(f"Checking FuzzyWuzzy ratio: P1-{place1}, P2-{place2}")
    fuzzy_res = False

    simple_ratio = fuzz.ratio(place1, place2)
    meta = {"simple_ratio": simple_ratio}

    # Check if the ratio is within the threshold
    if simple_ratio > simple_ratio_threshold:
        fuzzy_res = True

    print(f"FuzzyWuzzy res: {fuzzy_res} for {place1}")
    return fuzzy_res, simple_ratio


def places_existence(place, centric_city, radius, strictbounds, types='establishment', api_key=API_KEY):
    # Getting location lat long
    lat_long = get_lat_lng(centric_city)

    params = {
        'input': place,
        # 'location': lat_long,
        # 'radius':radius,
        'locationrestriction': f'circle:{radius}@{lat_long}',
        'strictbounds': strictbounds,
        'types': types,
        'rankby': radius,
        'key': api_key,
    }
    response = requests.get(autocomplete_url, params=params)
    return response.json()


def validate_place(plc_resp, current_place):
    for i in plc_resp['predictions']:
        recom_place = i["description"].split(",")[0]
        if fuzzy_wuzzy_check(place1=current_place, place2=recom_place)[0]:
            return {"place_exist": True, 'description': "place exist"}
    return {"place_exist": False, 'description': "place does not exist"}


def llm_place_check(place, city, model, output_tokens=100, temp=0.0, top_k=8, top_p=0.91):
    initial_query_prompt = '''
  You are an expert cartographer and you know all places which exists on Earth.
  You have been assigned task to validate if the place actually exist and strictly within the near vicinity of the city mentioned.
  Also provide description of place if it exist near city.
  Please strictly mention in description that place does not exist if it is not near to city.
  Please do not makeup places and only give answer based a existing place.
  The description should short descrition of 1-2 lines and should be stricly only be of 20-30 words only.
  You must strictly follow the below input and output format-
  input_text: Does Winnipeg Art Gallery present in the city WINNIPEG,MANITOBA,CANADA ?
  output: {"place_exist": True,"description": "The Winnipeg Art Gallery is an art museum in Winnipeg, Manitoba, Canada."}
  input_text: Does paris golf course present in the city PARIS, ILLINOIS,UNITED STATES OF AMERICA ?
  output : {"place_exist": False,"descritpion" : "No such place exist in the city Paris, ILLINOIS,UNITED STATES OF AMERICA."}
  input_text: Does Kohlapur present in the city Pune,India ?
  output : {"place_exist": False,"descritpion" : "kohlapur is not near to pune."}
  input_text: Does The Carolina Panthers Stadium present in the city CHARLOTTE,NORTH CAROLINA,UNITED STATES OF AMERICA ?
  output : {"place_exist: True,"description": "It is the home facility and headquarters of the Carolina Panthers of the National Football League."}
  '''

    current_prompt = '''
  input_text: Does {place} present in the city {city} ?
  output :
  '''
    input_query = initial_query_prompt + "\n" + current_prompt.format(place=place, city=city)

    response = model.predict(prompt=input_query, max_output_tokens=output_tokens, temperature=temp, top_k=top_k,
                             top_p=top_p)

    return response.text


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
            llm_validation = eval(llm_resp)
            places_validation[place] = llm_validation

    return places_validation
