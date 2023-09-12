from fuzzywuzzy import fuzz


def fuzzy_wuzzy_check(place1, place2, simple_ratio_threshold):
    print(f"Checking FuzzyWuzzy ratio: P1-{place1}, P2-{place2}")
    fuzzy_res = False

    simple_ratio = fuzz.ratio(place1, place2)
    meta = {"simple_ratio": simple_ratio}

    # Check if the ratio is within the threshold
    if simple_ratio > simple_ratio_threshold:
        fuzzy_res = True

    print(f"FuzzyWuzzy res: {fuzzy_res} for {place1}")
    return fuzzy_res, simple_ratio
