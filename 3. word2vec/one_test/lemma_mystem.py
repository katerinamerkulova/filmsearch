#!/usr/bin/env python
# coding: utf-8


import re
import requests


'''
Этот скрипт принимает на вход обработанный русский текст после mystem с флашами -clid в виде {разводить=V=прош,вин,ед,прич,полн,муж,сов,страд,неод|разводить=V=прош,им,ед,прич,полн,муж,сов,страд}{карьерист=S,муж,од=им,ед}{и=CONJ=}
На выход подаётся последовательность разделенных пробелами лемм с частями речи 
("зеленый_NOUN трамвай_NOUN").
Их можно непосредственно использовать в моделях с RusVectōrēs (https://rusvectores.org).
'''


def tag_mystem(text='Текст нужно передать функции в виде строки!', mapping=None, postags=True):
    # если частеречные тэги не нужны (например, их нет в модели), выставьте postags=False
    # в этом случае на выход будут поданы только леммы

    tagged = []
    text = re.findall('{(.+?)}', text)
    
    for w in text:
        try:
            lemma, pos = w.split('=', maxsplit=1)
        except ValueError:
            continue

        lemma = re.sub('\?', '', lemma)
        pos = re.findall('(.+?)[=,]', pos)[0]
        if mapping:
            if pos in mapping:
                pos = mapping[pos]  # здесь мы конвертируем тэги
            else:
                pos = 'X'  # на случай, если попадется тэг, которого нет в маппинге
        tagged.append(lemma.lower() + '_' + pos)
    if not postags:
        tagged = [t.split('_')[0] for t in tagged]
    return tagged


# Таблица преобразования частеречных тэгов Mystem в тэги UPoS:
mapping_url = 'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

mystem2upos = {}
r = requests.get(mapping_url, stream=True)
for pair in r.text.split('\n'):
    pair = pair.split()
    if len(pair) > 1:
        mystem2upos[pair[0]] = pair[1]


file = open('test_lemma.txt', encoding='utf-8')
for text in file:
    res = ' '.join(tag_mystem(text=text, mapping=mystem2upos))
    with open('test_lemma_correct.txt',  'a', encoding='utf-8') as file:
        file.write(res + ' &&&\n')
