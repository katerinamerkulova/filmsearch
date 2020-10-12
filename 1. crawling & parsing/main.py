import requests
import bs4
import re
import wikipediaapi as wapi
wiki = wapi.Wikipedia('ru')


def crawl_linkspage(url, common, length):
    page = requests.get(url)
    parser = bs4.BeautifulSoup(page.text, 'lxml')
    links = parser.find_all('li')[5:205]
    for link in links[:-2]:
        film_titles.append(link.a.get('title'))
    if len(film_titles) < length:
        url = common + re.search('pagefrom.+pages', str(parser)).group(0)    # next page
        try:
            parse_linkspage(url, common, length)
        except AttributeError:
            return film_titles
    return film_titles


def parsing(titles):
    for title in titles:
        page = wiki.page(title)
        try:
            if page.sections[0].title == 'Сюжет':
                plot = page.sections[0].text    # plot
                summary = page.summary
                with open('film_plots.txt', 'a', encoding='utf-8') as f:
                    f.write(plot + '\n&&&\n' )
                with open('summary.txt', 'a', encoding='utf-8') as f:
                    f.write(summary + '\n&&&\n' )
        except IndexError:
            None


def tokenization(texts):
    tokenized_texts = [' '.join(re.findall('\w+', text.lower())) for text in texts]
    with open('tokenized_film_plots.txt', 'w', encoding='utf-8') as f:
        f.write(tokenized_texts)

