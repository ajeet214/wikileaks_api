import requests
from bs4 import BeautifulSoup
import json
import time


class Style:
    BOLD = '\033[1m'
    END = '\033[0m'


class Wikileaks:

    def __init__(self):
        self.proxy = self._get_proxy()

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '103.59.95.71',
                    "proxy_port": '23344'}

    def wikileaks(self, domain):

        req = requests.get('https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date' % (
            domain), proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']})
        soup = BeautifulSoup(req.content, "lxml")
        # print(soup)
        count = soup.findAll('div', {"class": "total-count"})
        print("Total " + count[0].text)

        list1 = []

        for a in soup.find_all('div', class_="result"):
            links = {}
            con = a.find('div', class_='excerpt')
            # print(con.text)
            links['content'] = con.text
            if not links['content']:
                links['content'] = None

            source = a.find('div', class_='leak-label')
            # print(source.text.replace('\n', ''))
            links['author_name'] = source.text.replace('\n', '')
            if not links['author_name']:
                links['author_name'] = None

            thumbnail = a.find('div', class_='thumbnail')
            # print("https://search.wikileaks.org/"+thumbnail.img['src'])
            links['author_image'] = "https://search.wikileaks.org/"+thumbnail.img['src']
            if not links['author_image']:
                links['author_image'] = None

            dict1 = {}
            for i in a.find_all('div', class_='date'):
                m1 = i.text.replace(' ', '').replace('\n', '').replace('Created', 'Created:').replace('Released', 'Released:').lower()
                m2 = m1.split(':')
                if m2[0] == 'released':
                    dict1[m2[0]] = m2[1]
                else:
                    pass
            # print(dict1)

            #conversion of human readable time to unixtime
            try:
                links['datetime'] = int(time.mktime(time.strptime(dict1['released'], '%Y-%m-%d'))) - time.timezone
            except ValueError:
                links['datetime'] = None

            links['title'] = a.a.text
            if not links['title']:
                links['title'] = None

            links['url'] = a.a['href']

            if links['url'].endswith('.PDF'):
                links['type'] = 'document'
            elif links['url'].endswith('.pdf'):
                links['type'] = 'document'
            elif links['url'].endswith('.docx'):
                links['type'] = 'document'
            elif links['url'].endswith('.DOCX'):
                links['type'] = 'document'
            elif links['url'].endswith('.txt'):
                links['type'] = 'document'
            elif links['url'].endswith('.TXT'):
                links['type'] = 'document'
            elif links['url'].endswith('.xlsx'):
                links['type'] = 'document'
            elif links['url'].endswith('.xls'):
                links['type'] = 'document'
            elif links['url'].endswith('.csv'):
                links['type'] = 'document'
            elif links['url'].endswith('.CSV'):
                links['type'] = 'document'
            else:
                links['type'] = 'link'

            if not links['url']:
                links['url'] = None

            list1.append(links)

        # return {'data':
        #             {'results': list1
        #              }
        #         }
        return {'data': list1}


if __name__ == '__main__':
    obj = Wikileaks()
    print(obj.wikileaks("daniel"))
