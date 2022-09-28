import pandas as pd
import os

# add requirements.txt

def find(data):
    df = pd.read_csv(os.path.join(os.getcwd(), 'occupations/api/data/CBO2002 - Grande Grupo.csv'), delimiter=';', encoding='ISO-8859-9')
    data['name'] = df["TITULO"][0].strip()
    return data