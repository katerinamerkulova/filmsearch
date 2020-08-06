import pandas as pd
import numpy as np
import pickle
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stops = stopwords.words("russian")
stops.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на'])

with open('tfidf.pickle', 'rb') as fid:
    vectorizer = pickle.load(fid)
with open('tfidf_matrix.pickle', 'rb') as fid:
    X = pickle.load(fid)    # https://yadi.sk/d/tbhfd_gJY41ofg

#query = 'Обычное корейское семейство Кимов жизнь не балует. Приходится жить в сыром грязном полуподвале, воровать интернет у соседей и перебиваться случайными подработками. Однажды друг сына семейства, уезжая на стажировку за границу, предлагает тому заменить его и поработать репетитором у старшеклассницы в богатой семье Пак. Подделав диплом о высшем образовании, парень отправляется в шикарный дизайнерский особняк и производит на хозяйку дома хорошее впечатление. Тут же ему в голову приходит необычный план по трудоустройству сестры.'
def predict(query, n=10):
    query = ' '.join(list(morph.parse(word)[0].normal_form for word in re.findall("[\w]+", query)))
    query = ' '.join([word for word in query.split() if word not in stops])
    vec = vectorizer.transform([query]).toarray().reshape(25000, 1)
    data = pd.read_csv('data.csv', sep=';')
    simil = []
    for vector, film in zip(X, data['film']):
        simil.append((np.dot(vector, vec)/np.linalg.norm(vector)*np.linalg.norm(vec), film))
    simil.sort(reverse=True)
    prediction = ''
    for similarity, film in simil[:n]:
        prediction += 'similarity = ' + str(round(similarity[0], 5)) + ' film is ' + film + '\n'
    return prediction
