import requests
import bs4
import re
import wikipediaapi as wapi
wiki = wapi.Wikipedia('ru')


def crawl_linkspage(url, common, length, film_titles=[]):
    page = requests.get(url)
    parser = bs4.BeautifulSoup(page.text, 'lxml')
    links = parser.find_all('li')[2:205]

    for link in links[:-3]:
        title = link.a.get('title')
        if not re.match('Категория:', title):
            film_titles.append(title)

    if len(film_titles) < length:
        url = common + re.search('pagefrom.+pages', str(parser)).group(0)    # next page
        try:
            crawl_linkspage(url, common, length, film_titles)
        except AttributeError:
            return film_titles 
    return film_titles


def parsing(titles):
    correct_titles = []
    for title in titles:
        page = wiki.page(title)
        
        for sect in page.sections:
            if sect.title in ('Сюжет', 'Синопсис'):
                plot = sect.text # plot
                plot = re.sub('\n', ' ', text)
                correct_titles.append(title)

                with open('film_plots.txt', 'a', encoding='utf-8') as f:
                    f.write(plot + '&&&\n')
                break
    with open('wiki_titles.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(correct_titles))


def tokenization(texts):
    tokenized_texts = [' '.join(re.findall('\w+', text.lower())) for text in texts]
    with open('tokenized_film_plots.txt', 'w', encoding='utf-8') as f:
        f.write('\n&&&\n'.join(tokenized_texts))

