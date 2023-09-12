## Usage

```python 
import json
from truthfulnesscheck.validate_places import places_check

city_name = "Mumbai,MH,India"
text_content = "The seven

result = places_check(input_text=text_content,
                      city=city_name)
                      
print("result: \n", json.dumps(result, indent=2))
```

