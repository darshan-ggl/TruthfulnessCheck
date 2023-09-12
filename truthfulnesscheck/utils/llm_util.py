from truthfulnesscheck.config import config

initial_query_prompt = config["LLM"]["initial_query_prompt"]


def llm_place_check(place, city, model, output_tokens=100, temp=0.0, top_k=8, top_p=0.91):
    current_prompt = '''
    input_text: Does {place} present in the city {city} ?
    output :
    '''
    input_query = initial_query_prompt + "\n" + current_prompt.format(place=place, city=city)

    response = model.predict(prompt=input_query, max_output_tokens=output_tokens,
                             temperature=temp, top_k=top_k, top_p=top_p)

    return response.text
