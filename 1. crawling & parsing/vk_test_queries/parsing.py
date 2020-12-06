from copy import deepcopy
import json
import pandas as pd
from pprint import pprint
import re
import vk

def parse_topic():
    key = '77b8ffc377b8ffc377b8ffc3dc77cc4ab8777b877b8ffc32818f6219a691916e88298b3'
    session = vk.Session(access_token=key)  # Авторизация
    vk_api = vk.API(session)
    comments = vk_api.board.getComments(v=5.95,
                                        group_id='108468',
                                        topic_id='24654269',
                                        count=1)
    number = int(comments['count'])
    for _ in range(1, number, 99):
        last_comment_id = int(comments['items'][-1]['id'])
        comments['items'].extend(
            vk_api.board.getComments(v=5.95,
                                     group_id='108468',
                                     topic_id='24654269',
                                     start_comment_id=last_comment_id,
                                     count=100)['items'][1:])

    with open('comments.json', 'w', encoding='utf-8') as outfile:
        json.dump(comments, outfile, ensure_ascii=False)

def parse_json_file(path):
    '''
    INPUT:
    com['id'] - идентификатор комментария.
    com['from_id'] - идентификатор автора комментария.
    com['date'] - дата создания (в формате Unixtime).
    com['text'] - текст комментария и если обращение, то:
    [idНОМЕРАДРЕСАТА:bp-НОМЕРГРУППЫ_НОМЕРКОММЕНТАРИЯОБРАЩЕНИЯ|ИМЯ]

    OUTPUT:
    словарь: идентификатор комментария - текст комментария
    '''
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    vocab = {com['id']: re.sub('\n', ' ', com['text']) for com in data['items']}

    vocab_str = ''
    for key, value in vocab.items():
        vocab_str += f'{key}: {value}\n'
    with open('texts_id.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(vocab_str)

def split_to_chunks():
    '''
    INPUT:
    словарь: идентификатор комментария - текст комментария

    OUTPUT:
    последовательность: идентификатор комментария - *идентификатор комментария обращения
    '''

    chunks = {}
    extract_all_addressee_id = lambda x: re.findall(r'\_(\d+)\|', x)

    with open('texts_id.txt', 'r', encoding='utf-8') as comments:
        for comment in comments:
            idx, text = comment.split(':', maxsplit=1)
            idx = int(idx)
            if addressees := extract_all_addressee_id(text):
                for addressee in addressees:
                    if idx not in chunks:
                        chunks[idx] = []
                    chunks[idx].append(int(addressee))

    for idx in chunks:
        for addressee in chunks[idx]:
            if addressee in chunks:
                chunks[idx].extend(chunks[addressee])
                break
    chunks = [sorted(set([*value, key])) for key, value in chunks.items()]
    chunks.sort(key=lambda x: len(x))

    print('step 3')
    for chunk in deepcopy(chunks):
        if chunk[:-1] in chunks:
            chunks.remove(chunk[:-1])

    with open('idx_chunks.txt', 'w') as outfile:
        pprint(chunks, stream=outfile)

def decoding_chunks():
    vocab = {}
    for comment in open('texts_id.txt', 'r', encoding='utf-8'):
        idx, text = comment.split(': ', maxsplit=1)
        vocab[int(idx)] = text
    
    extract_text = lambda x: re.sub(r'\[.+\],?', '', x, flags=re.DOTALL)
    comment_chunks = []
    with open('idx_chunks.txt', 'r') as chunks:
        for chunk in chunks:
            local_chunk = []
            for idx in chunk.split():
                try:
                    text = extract_text(vocab[int(idx)])
                    local_chunk.append(text)
                except KeyError:
                    continue
            comment_chunks.append('\t'.join(local_chunk))

    with open('text_chunks.txt', 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(comment_chunks))


if __name__ == "__main__": 
    #parse_topic()
    #parse_json_file('comments.json')
    #split_to_chunks()
    decoding_chunks()