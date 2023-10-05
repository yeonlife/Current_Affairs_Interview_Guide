from crawling_functions import *

# 모든 네이버 뉴스 카테고리의 뉴스 기사 링크 모음
all_hrefs = {}
sids = [i for i in range(100,106)]

for sid in sids:
    sid_data = re_tag(sid)
    all_hrefs[sid] = sid_data

print(all_hrefs)