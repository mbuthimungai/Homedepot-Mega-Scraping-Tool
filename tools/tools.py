from requests_html import AsyncHTMLSession
import random
import secrets
import asyncio
from tools.cookie_handler import CookieHandler

cookie_handler = CookieHandler()

def random_values(d_lists):
    idx = secrets.randbelow(len(d_lists))
    return d_lists[idx]

def user_agents():
    try:
        with open('tools/user-agents.txt') as f:
            agents = f.read().split("\n")
            return random_values(agents).strip()
    except FileNotFoundError:
        with open('tools/user-agents.txt', 'w') as f:
            pass

class Response:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = AsyncHTMLSession()
        self.proxies = {
            'http': 'http://brd-customer-hl_907e9430-zone-homedepot_search2:rb9km2u03m64@brd.superproxy.io:22225',
            # 'https': 'http://brd-customer-hl_907e9430-zone-homedepot_search2:rb9km2u03m64@brd.superproxy.io:22225'
        }
        self.use_proxy = True
        self.headers = {
            'User-Agent': user_agents() or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': '*/*',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.homedepot.com/s/jkhkh?NCNI-5',
            'content-type': 'application/json',
            'X-Experience-Name': 'general-merchandise',
            'apollographql-client-name': 'general-merchandise',
            'apollographql-client-version': '0.0.0',
            'X-current-url': '/s/jkhkh',
            'x-hd-dc': 'origin',
            'X-Api-Cookies': '{"x-user-id":""}',
            'x-debug': 'false',
            'Origin': 'https://www.homedepot.com',
            'Connection': 'keep-alive',
            'Cookie': f'_abck=dhgkjdfghkdfjghaposdh{random.randint(100,999)}kjahf-235',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

    async def content_graph(self, graph_payload=None):
        max_retry = 10
        additional_retry = 10  # New retry count with a new cookie

        for attempt in range(max_retry + additional_retry):
            self.headers['User-Agent'] = user_agents()
            if attempt >= max_retry:                
                self.headers['Cookie'] = await cookie_handler.read_cookie()                
            else:                
                self.headers['Cookie'] = f'_abck=dhgkjdfghkdfjghaposdh{random.randint(100,999)}kjahf-235'
               
            try:
                if self.use_proxy:
                    response = await asyncio.wait_for(
                        self.session.post(self.base_url, headers=self.headers, json=graph_payload, proxies=self.proxies, ), 5
                    )
                else:
                    response = await asyncio.wait_for(
                        self.session.post(self.base_url, headers=self.headers, json=graph_payload, ), 5
                    )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retry + additional_retry} failed: {e}")                
                if attempt >= max_retry:
                    await cookie_handler.farm_cookies()
                
                if "proxy" in str(e).lower() and self.use_proxy:
                    print("Proxy failed. Trying without proxy...")
                    self.use_proxy = False
                    continue  # Retry without proxy
                if attempt == max_retry + additional_retry - 1:
                    return None

    async def content_html(self):
        max_retry = 10
        additional_retry = 10

        for attempt in range(max_retry + additional_retry):
            
            if attempt >= max_retry:                
                self.headers['Cookie'] = await cookie_handler.read_cookie()
            else:
                self.headers['Cookie'] = f'_abck=dhgkjdfghkdfjghaposdh{random.randint(100,999)}kjahf-235'
                                
            try:
                if self.use_proxy:
                    if self.base_url.startswith('https://www.homedepot.com/'):
                        self.headers['User-Agent'] = user_agents()
                        response = await asyncio.wait_for(
                            self.session.get(self.base_url, headers=self.headers, proxies=self.proxies, ), 5
                        )
                    else:                        
                        response = await asyncio.wait_for(
                            self.session.get(self.base_url, proxies=self.proxies, ), 5
                        )                        
                else:
                    if self.base_url.startswith('https://www.homedepot.com/'):
                        self.headers['User-Agent'] = user_agents()
                        response = await asyncio.wait_for(
                            self.session.get(self.base_url, headers=self.headers, ), 5
                        )
                    else:
                        response = await asyncio.wait_for(
                            self.session.get(self.base_url, ), 5
                        )
                response.raise_for_status()
                return response.text
            except Exception as e: 
                            
                print(f"Attempt {attempt + 1}/{max_retry + additional_retry} failed: {e}")
                if attempt >= max_retry:
                    await cookie_handler.farm_cookies()
                
                if "proxy" in str(e).lower() and self.use_proxy:
                    print("Proxy failed. Trying without proxy...")
                    self.use_proxy = False
                    continue  # Retry without proxy
                if attempt == max_retry + additional_retry - 1:
                    return None