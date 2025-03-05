import re 

def string_to_json(response):
    cleaned = re.sub(r"^```json\s*", "", response)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned