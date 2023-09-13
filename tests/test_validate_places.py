import json
from truthfulnesscheck.validate_places import places_check

city_name = "Mumbai,MH,India"
place = "Marine Drive"

result = places_check(city=city_name,
                      place=place,
                      radius=300)
print("result: \n", json.dumps(result, indent=2))
