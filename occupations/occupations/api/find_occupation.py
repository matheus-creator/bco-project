import pandas as pd
import os

def find(data):
    df = pd.read_csv(os.path.join(os.getcwd(), 'occupations/api/data/CBO2002 - Grande Grupo.csv'), delimiter=';')
    data['name'] = df["TITULO"][0].strip()
    return data