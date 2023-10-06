import pandas as pd
from crawling_functions import *

# 모든 네이버 뉴스 카테고리의 뉴스 기사 링크 모음
all_hrefs = {}
sids = [i for i in range(100,106)]

for sid in sids:
    sid_data = re_tag(sid)
    all_hrefs[sid] = sid_data

print(all_hrefs)


idx2word = {'100' : '정치', '101' : '경제', '102' : '사회', '103' : '생활/문화', '105' : 'IT/과학', '104':'세계'}
urllist= {'제목':[],'주소':[],'본문':[],'분야':[]}

for line in all_hrefs:
    category_list = all_hrefs[line]
    for url in category_list:
        response = requests.get(url)
        newsoup = BeautifulSoup(response.content, 'html.parser')
        title = newsoup.find('span', attrs={'class':'media_end_head_headline'})
        article = newsoup.find('article', attrs={'class': 'go_trans _article_content'})
        category = idx2word[str(url[-3:])]

        urllist['제목'].append(title.get_text())
        urllist['주소'].append(url)
        urllist['본문'].append(article.get_text())
        urllist['분야'].append(category)

pd.DataFrame(urllist)
