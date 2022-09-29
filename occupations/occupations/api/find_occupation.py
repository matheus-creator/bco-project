import os
import pandas as pd
import unidecode
from .utils import PUNCTUATION, INEXISTENT_SALARY_MESSAGE
from .api_request import make_request
from .assemble_strings import assemble_key_for_maping, assemble_api_string

OCCUPATIONS = {}
BIG_GROUPS = {}
MAIN_SUB_GROUPS = {}
SUB_GROUPS = {}
FAMILIES = {}

def find(data):
    global OCCUPATIONS
    generate_occupation_groups_dicts()
    cbo_code = get_cbo_code(data["occupation"])
    occupation_salary = get_occupation_info(data["occupation"], cbo_code)
    occupation_groups = get_occupation_groups(cbo_code)
    occupation_response = {
        "cbo_code": cbo_code, 
        "salary": occupation_salary,
        "big_group": occupation_groups[0],
        "main_sub_group": occupation_groups[1],
        "sub_group": occupation_groups[2],
        "family": occupation_groups[3],
    }

    return occupation_response

def read_data(path):
    return pd.read_csv(os.path.join(os.getcwd(), path), delimiter=';', encoding='ISO-8859-9')

def generate_occupation_groups_dicts():
    global OCCUPATIONS
    global BIG_GROUPS
    global MAIN_SUB_GROUPS
    global SUB_GROUPS
    global FAMILIES
    if OCCUPATIONS == {}:
        df = read_data('occupations/api/data/CBO2002 - Sinonimo.csv')
        OCCUPATIONS = generate_occupations_hash_table(df["TITULO"], df["CODIGO"])

        df = read_data('occupations/api/data/CBO2002 - Grande Grupo.csv')
        BIG_GROUPS = generate_group_hash_table(df["CODIGO"], df["TITULO"])

        df = read_data('occupations/api/data/CBO2002 - SubGrupo Principal.csv')
        MAIN_SUB_GROUPS = generate_group_hash_table(df["CODIGO"], df["TITULO"])

        df = read_data('occupations/api/data/CBO2002 - SubGrupo.csv')
        SUB_GROUPS = generate_group_hash_table(df["CODIGO"], df["TITULO"])

        df = read_data('occupations/api/data/CBO2002 - Familia.csv')
        FAMILIES = generate_group_hash_table(df["CODIGO"], df["TITULO"])

def get_cbo_code(occupation):
    global OCCUPATIONS
    key_to_find = assemble_key_for_maping(occupation)
    cbo_code = ""
    try:
        cbo_code = OCCUPATIONS[key_to_find]
    except KeyError:
        cbo_code = None

    return cbo_code

def get_occupation_info(occupation, cbo_code):
    if cbo_code == None:
        return INEXISTENT_SALARY_MESSAGE
    # generate api string
    api_string = assemble_api_string(occupation, cbo_code)
    # api request
    occupation_salary = make_request(api_string)

    return occupation_salary

def get_occupation_groups(cbo_code):
    cbo = str(cbo_code)

    big_group = BIG_GROUPS[int(cbo[:1])]
    main_sub_group = MAIN_SUB_GROUPS[int(cbo[:2])]
    sub_group = SUB_GROUPS[int(cbo[:3])]
    family = FAMILIES[int(cbo[:4])]

    return [big_group, main_sub_group, sub_group, family]

def generate_occupations_hash_table(keys, values):
    global PUNCTUATION
    # remove blank spaces and turn lower case
    keys_without_blank_space = [key.replace(" ", "").lower() for key in keys]
    # remove punctuation, accent and other special characters
    keys_without_punctuation = []
    temp_key = ""
    for key in keys_without_blank_space:
        temp_key = unidecode.unidecode(key)
        for c in PUNCTUATION:
            temp_key = temp_key.replace(c, "")
        keys_without_punctuation.append(temp_key)

    hash_table = dict(zip(keys_without_punctuation, values))

    del keys_without_blank_space[:]
    del keys_without_punctuation[:]

    return hash_table

def generate_group_hash_table(keys, values):
    # trim values
    temp_values = [value.strip() for value in values]
    return dict(zip(keys, temp_values))
