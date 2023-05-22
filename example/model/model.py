from config import PATH
from catboost import CatBoostClassifier, Pool
import requests
import pandas as pd 
import re 
import string

class SalaryPrediciton:

    TAG_RE = re.compile(r'<[^>]+>')
    table = str.maketrans(dict.fromkeys(string.punctuation)) # delete punctuation

    def __init__(self) -> None:
        self.model = CatBoostClassifier().load_model(PATH)

    def predict(self, url: str) -> float:
        data = self.get_features(url)
        return self.model.predict(self.pool(data))

    def get_features(self, url: str) -> pd.DataFrame:

        features = {}

        id = re.findall('[0-9]+', url)[0]
        r = requests.get(f'https://api.hh.ru/vacancies/{id}')

        if r.status_code == 404:
            print('Кажется, такой ссылки не существует')
            raise
        if r.status_code == 403:
            print('Сервис отдыхает, приходите через 30 минут')
            raise

        answer = r.json()
        features['description_clear'] = [self.remove_tags(answer['description'])]

        return pd.DataFrame(features)

    def remove_tags(self, text:str) -> str:
        text = self.TAG_RE.sub('', text)
        text = text.translate(self.table).lower()
        return ' '.join(text.split()) # delete extra spaces
    
    def pool(self, data: pd.DataFrame) -> Pool:
        return Pool(
            data=data,
            text_features=['description_clear']
        )