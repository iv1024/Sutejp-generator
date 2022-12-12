import requests
from bs4 import BeautifulSoup
from ua_parser import user_agent_parser
from random_tools import random_ua

class Sutejp:
    def generate(self):
        session = requests.Session()
        mail_url_list = []
        ua = random_ua()
        parsed_ua = user_agent_parser.Parse(ua)
        headers =  {
            "authority": "sute.jp",
            "_method": "GET",
            "path": "/",
            "scheme": "https",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",      "if-none-match": 'W/"337b242b5973ad18882d5e9cae1ad489"',
            "referer": "https://sute.jp/inbox",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"{}"'.format(parsed_ua['os']['family']),
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="{0}", "Google Chrome";v="{0}"'.format(parsed_ua['user_agent']['major'])
        }
        response = session.get("https://sute.jp", headers=headers)
        soup = BeautifulSoup(response.content, features="html.parser")
        self.token = soup.find('input', {'name': 'authenticity_token'}).get('value')
        self.username = soup.find("input", {"name": "guest[login]"}).get("value")
        data = {
             "utf8": "✓",
             "authenticity_token": str(self.token),
             "guest[login]": str(self.username)
        }
        headers = {
            "authority": "sute.jp",
            "_method": "POST",
            "path": "/signup",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-length": "160",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://sute.jp",
            "referer": "https://sute.jp/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="{0}", "Google Chrome";v="{0}"'.format(parsed_ua['user_agent']['major']),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"{}"'.format(parsed_ua['os']['family']),
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        result = session.post("https://sute.jp/signup", data=data, headers=headers, cookies=response.cookies, allow_redirects=True)
        soup = BeautifulSoup(result.content, features="html.parser")
        for mails in soup.select("li.message"):
            data_id = mails.get("data-id")
            mail_url_list.append(f"https://sute.jp/inbox/{data_id}")
        self.status_code = result.status_code
        if self.status_code in (200, 201):
            return True
        elif self.status_code == 403:
            raise Exception("403 Forbidden")
        else:
            raise Exception(f"{self.status_code}")
