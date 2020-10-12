# https://github.com/summanlp/textrank
from summa.summarizer import summarize


texts = open('raw_summary.txt', encoding='UTF-8').read().split('\n&&&\n')

print('BEFORE SUMMARIZATION:', end='\n\n')
for text in texts[5550:5555]:
    print(text, end='\n\n')

summaries = []
for text in texts:
    summary = summarize(text, words=30, language='russian')
    if summary:
        summaries.append(summary)
    else:
        summaries.append(text)

print('AFTER SUMMARIZATION:', end='\n\n')
for summary in summaries[5550:5555]:
    print(summary, end='\n\n')


with open('summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n&&&\n'.join(summaries))
