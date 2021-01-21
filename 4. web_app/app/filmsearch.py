from numpy.linalg import norm
import os
from pandas import read_csv
from pickle import load
from pymorphy2 import MorphAnalyzer
import re

morph = MorphAnalyzer()
stops = open(os.path.join('app', 'russian.txt')).read().split()

with open(os.path.join('app', 'tfidf.pickle'), 'rb') as fid:
    vectorizer = load(fid)
with open(os.path.join('app', 'tfidf_matrix.pickle'), 'rb') as fid:
    X = load(fid)

#query = 'Обычное корейское семейство Кимов жизнь не балует. Приходится жить в сыром грязном полуподвале, воровать интернет у соседей и перебиваться случайными подработками. Однажды друг сына семейства, уезжая на стажировку за границу, предлагает тому заменить его и поработать репетитором у старшеклассницы в богатой семье Пак. Подделав диплом о высшем образовании, парень отправляется в шикарный дизайнерский особняк и производит на хозяйку дома хорошее впечатление. Тут же ему в голову приходит необычный план по трудоустройству сестры.'
def predict(query, n=10):
    query = ' '.join(list(morph.parse(word)[0].normal_form for word in re.findall("[\w]+", query)))
    query = ' '.join([word for word in query.split() if word not in stops])
    vec = vectorizer.transform([query]).toarray().reshape(1000, 1)
    data = read_csv(os.path.join('app', 'data.csv'), sep=';')
    simil = []
    for vector, film in zip(X, data['film']):
        simil.append((vector@vec/norm(vector)*norm(vec), film))
    simil.sort(reverse=True)
    prediction = ''
    for similarity, film in simil[:n]:
        prediction += 'similarity = ' + str(round(similarity[0], 5)) + ' film is ' + film + '\n'
    return prediction
