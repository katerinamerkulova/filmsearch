import random
import re

from summa.summarizer import summarize
import wikipediaapi as wapi
wiki = wapi.Wikipedia('ru')


def parsing(title):
    page = wiki.page(title)
    text = page.summary
    if len(text.split()) < 300:
        summary = text
    else:
        summary = summarize(text, words=50, language='russian')

    summary = re.sub(r'\(.+?\)', '', summary)
    summary = re.sub(r'«.+?»', '', summary)
    summary = re.sub(r'[^\s\dА-Яа-я\-]', '', summary)
    summary = re.sub(r'\s+', ' ', summary)

    if len(summary.split()) > 30:
        with open('summary.txt', 'a', encoding='utf-8') as f:
            f.write(summary.lower().strip() + '\n')
        
        summary_titles.append(title)
        

titles = open('titles.txt', 'r', encoding='utf-8').read().split('\n')
wiki_titles = open('wiki_titles.txt', 'r', encoding='utf-8').read().split('\n')
summary_titles = []

titles_to_parse = random.sample(titles, 1000)
for title in titles_to_parse:
    if title in wiki_titles:
        parsing(title)

while len(summary_titles) < 1000:
    title = random.choice(titles)
    if title in wiki_titles and title not in summary_titles:
        parsing(title)

with open('summary_titles.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary_titles))
