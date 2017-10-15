from requests.exceptions import RequestException
from multiprocessing import Pool
import requests
from lxml import etree
import json

def get_one_page(url,headers):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None



def parse_one_page(html):
    html = etree.HTML(html)
    img_href = html.xpath('//*[@id="app"]/div/div/div/dl/dd/a/img[2]/@data-src')
    ranking = html.xpath('//dd/i/text()')
    film_name = html.xpath('//dd/div/div/div[1]/p[1]/a/text()')
    to_star = html.xpath('//dd/div/div/div[1]/p[2]/text()')
    score_one = html.xpath('//dd/div/div/div[2]/p/i[1]/text()')
    score_two = html.xpath('//dd/div/div/div[2]/p/i[2]/text()')
    release_time = html.xpath('//dd/div/div/div[1]/p[3]/text()')
    for img,ran,film,start,one,two,release in zip(img_href,ranking,film_name,to_star,score_one,score_two,release_time):
        data = {
            'logo':img,
            '排名':ran,
            '电影':film,
            '主演': start.strip(),
            '评分': one+two,
            '上映时间': release
        }
        print(data)
        yield  {
            'logo': data['logo'],
            '排名':data['排名'],
            '电影':data['电影'],
            '评分': data['评分'],
            '主演': data['主演'][3:],
            '上映时间': data['上映时间'][5:],
        }

def main(offset):
    url = 'http://maoyan.com/board/4?offset={0}'.format(offset)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }
    html = get_one_page(url,headers)
    for items in parse_one_page(html):
        writefile(items)

def writefile(content):
    with open('maoyan_list.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])