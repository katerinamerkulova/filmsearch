import re

data = open('film_plots.txt').read().split('&&&\n')[:-1]
titles = open('wiki_titles.txt').read().split('\n')
stop_words = open('russian.txt').read().split('\n')

for idx, text in enumerate(data):
  text = re.findall('\w+', text.lower())
  text = ' '.join([word for word in text if word not in stop_words]) + '&&&\n'

  with open('film_plots_tokenized.txt', 'a') as file:
    file.write(text)