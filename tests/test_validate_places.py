import json
from truthfulnesscheck.validate_places import places_check

city_name = "Mumbai,MH,India"
text_content = "The seven islands that constitute Mumbai were earlier home to communities of Marathi language-speaking " \
               "Koli people.[22][23][24] For centuries, the seven islands of Bombay were under the control of successive " \
               "indigenous rulers before being ceded to the Portuguese Empire, and subsequently to the East India Company in 1661," \
               " through the dowry of Catherine Braganza when she was married off to Charles II of England.[25] Beginning in 1782," \
               " Mumbai was reshaped by the Hornby Vellard project,[26] which undertook reclamation of the area between the seven " \
               "islands from the sea.[27] Along with construction of major roads and railways, the reclamation project, " \
               "completed in 1845, transformed Mumbai into a major seaport on the Arabian Sea. Mumbai in the 19th century was " \
               "characterized by economic and educational development. During the early 20th century it became a strong base for " \
               "the Indian independence movement. Upon India's independence in 1947 the city was incorporated into Bombay State. " \
               "In 1960, following the Samyukta Maharashtra Movement, a new state of Maharashtra was created with Mumbai as " \
               "the capital.[28]"

result = places_check(input_text=text_content,
                      city=city_name,
                      radius=300)
print("result: \n", json.dumps(result, indent=2))
