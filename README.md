## Usage

```python 
import json
from truthfulnesscheck.validate_places import places_check

city_name = "Mumbai,MH,India"
text_content = """
    Mumbai, the city of dreams, is a bustling metropolis on India's western coast. It's a place where tradition and 
    modernity coexist in harmony. As you step into this vibrant city, you'll be immersed in a world of contrasts.
    The Gateway of India, a historic monument on the Arabian Sea, welcomes you with its grandeur. 
    Nearby, Marine Drive stretches along the coastline, offering stunning views of the sea, especially during the 
    evening when the "Queen's Necklace" of lights illuminates the promenade.
    """

result = places_check(input_text=text_content,
                      city=city_name)
                      
print("result: \n", json.dumps(result, indent=2))
```

