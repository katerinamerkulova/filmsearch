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


##crawling
# the number of films in wikipedia is 29820 https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83

url='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
common = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&'
film_titles = crawl_linkspage(url, common, 29820)

with open('wiki_titles.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(film_titles))

#cartoons
# the number of cartoons in wikipedia is 3764 https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83

url='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
common = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&'

car_titles + = crawl_linkspage(url, common, 3764)

with open('wiki_titles.txt', 'a', encoding='utf-8') as f:
    f.write('\n'.join(car_titles))

#TVseries
# the number of tv-series in wikipedia is 3588 https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D0%BB%D0%B5%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83

url='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D0%BB%D0%B5%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
common = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D0%BB%D0%B5%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&'

tv_titles = crawl_linkspage(url, common, 3588)

with open('wiki_titles.txt', 'a', encoding='utf-8') as f:
    f.write('\n'.join(tv_titles))


## parsing
#titles = open('wiki_titles.txt', encoding='utf-8').read().split('\n')
titles = film_titles + car_titles + tv_titles
parsing(titles)

## tokenization
texts = open('film_plots.txt', encoding='UTF-8').read().split('\n&&&\n')
tokenization(texts)