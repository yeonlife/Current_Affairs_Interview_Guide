from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys

def ex_tag(sid, page):
    '''
    뉴스 분야(sid)와 페이지(page)를 입력하면, 그에 대한 링크들을 리스트로 추출하는 함수\n
    Given a news category (sid) and a page number (page), 
    this function extracts a list of links according to that category.

    Args:
    - sid (int): The news category identifier.
    - page (int): The page number to retrieve links from.

    Returns:
    - tag_list (list): A list of links found on the specified news category page.
    '''

    # 뉴스 카테고리 페이지에 해당하는 url
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}#&date=%2000:00:00&page={page}"
    
    # 웹 크롤링 시 로봇이 아님을 인지시키기 위해 사용, 에러 방지
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
              AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
    
    html = requests.get(url, headers=header)   # 지정된 url에 GET 요청을 보냄.
    soup = BeautifulSoup(html.text, 'lxml')    # html.text에는 HTML 코드가 담겨 있음. lxml 모듈의 해석에 의해 HTML 문서로 변환
    a_tag = soup.find_all("a")   # html에서 하이퍼링크를 정의하는 모든 <a> 태그 가져옴

    tag_list = []
    for a in a_tag:
        if 'href' in a.attrs:   # <a> tag에 하이퍼링크 걸려 있어야 함
            #print(a['href'])
            if (f'sid={sid}' in a['href']) and ('article' in a['href']):   
                # 하이퍼링크 주소에 sid 넘버와 article 포함되어 있는 링크만 수집
                tag_list.append(a['href'])
    
    return tag_list

def re_tag(sid, pg_start = 1, pg_end = 100):
    '''
    특정 분야의 1~100페이지 까지의 뉴스 링크 중복되지 않게 리스트로 반환\n
    Retrieve a list of non-duplicate news links for a specific category from pages 1 to 100.

    Args:
    - sid (int): The news category identifier.
    - pg_start (int, optional): The starting page number (default is 1).
    - pg_end (int, optional): The ending page number (default is 100).

    Returns:
    - re_list (list): A list of unique news links from the specified category and pages.
    '''
    
    re_list = []
    num_pages = pg_end - pg_start + 1

    for i in tqdm(range(num_pages)):
        temp_tag = ex_tag(sid, i+1)
        re_list.extend(temp_tag)
    
    # 중복 제거
    re_set = set(re_list)
    re_list = list(re_set)

    return re_list
