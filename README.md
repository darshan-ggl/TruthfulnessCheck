## Usage

### Config
```yaml
- PROJECT_ID: 
- location:
- API_KEY:
- radius:
- simple_ratio threshold:

  
# secondary
- spacy_model: 

# API endpoints
- geocode_url: "https://maps.googleapis.com/maps/api/geocode/json"
- autocomplete_url: 'https://maps.googleapis.com/maps/api/place/autocomplete/json'  ## or places url

```

```python 
from truthfulnesscheck import valdate_places

validate_places(
    city="city_name_along_with_state_and_country_name",
    text="plain_text_content"
) 
```

