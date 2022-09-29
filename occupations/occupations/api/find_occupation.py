import os
import pandas as pd
import unidecode
from .utils import API_BASE_URL, PUNCTUATION, INEXISTENT_SALARY_MESSAGE
from .api_request import make_request

OCCUPATION = {}

# add requirements.txt
# grupos

def find(data):
    # TODO: handle occupation not found
    global OCCUPATION
    generate_occupation_dict()
    cbo_code = get_cbo_code(data["occupation"])
    occupation_salary = get_occupation_info(data["occupation"], cbo_code)
    occupation_response = {
        "cbo_code": cbo_code,
        "salary": occupation_salary,
    }
    
    return occupation_response

def get_cbo_code(occupation):
    global OCCUPATION
    key_to_find = assemble_key_for_maping(occupation)
    cbo_code = ""
    try:
        cbo_code = OCCUPATION[key_to_find]
    except KeyError:
        cbo_code = None

    return cbo_code

def get_occupation_info(occupation, cbo_code):
    if cbo_code == None:
        return INEXISTENT_SALARY_MESSAGE
    # remove accent and other special characters
    decoded_occupation = unidecode.unidecode(occupation)
    # generate api string
    api_string = assemble_api_string(decoded_occupation, cbo_code)
    # api request
    occupation_salary = make_request(api_string)

    return occupation_salary

def generate_occupation_dict():
    global OCCUPATION
    if OCCUPATION == {}:
        df = pd.read_csv(os.path.join(os.getcwd(), 'occupations/api/data/CBO2002 - Sinonimo.csv'), delimiter=';', encoding='ISO-8859-9')
        OCCUPATION = generate_hash_map(df["TITULO"], df["CODIGO"])

def generate_hash_map(keys, values):
    global PUNCTUATION
    # remove blank spaces and turn lower case
    keys_without_blank_space = [key.replace(" ", "").lower() for key in keys]
    # remove punctuation
    keys_without_punctuation = []
    temp_key = ""
    for key in keys_without_blank_space:
        temp_key = key
        for c in PUNCTUATION:
            temp_key = temp_key.replace(c, "")
        keys_without_punctuation.append(temp_key)

    hash_map = dict(zip(keys_without_punctuation, values))

    del keys_without_blank_space[:]
    del keys_without_punctuation[:]

    return hash_map

def assemble_key_for_maping(key):
    # remove blank spaces and turn lower case
    temp_key = key.replace(" ", "").lower()
    # remove punctuation
    for c in PUNCTUATION:
        temp_key = temp_key.replace(c, "")

    return temp_key

def assemble_api_string(string, cbo_code):
    # trim string
    temp_string = string.strip()
    # remove punctuation
    for c in PUNCTUATION:
        temp_string = temp_string.replace(c, "")
    # change blank spaces for "-" and turn lower case
    temp_string = temp_string.replace(" ", "-").lower()
    # add cbo code
    temp_string = temp_string + "-cbo-" + str(cbo_code)
    # add url
    api_string = API_BASE_URL + temp_string

    return api_string
