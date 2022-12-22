# %%
import configparser
import datetime
import json
import logging
import os
import random
import re
import time
from glob import glob

import requests
from bs4 import BeautifulSoup 

from Crawler import Crawler
from Header import header

# %%
config = configparser.ConfigParser()
config.read(r"D:\591\property\a.property")

# %%
log_dir = config['DEFAULT']['log_dir']
save_dir = config['DEFAULT']['save_dir']

# %%
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    # stream=sys.stdout
                    handlers=[logging.FileHandler(log_dir + '\\' + '{0}_crawler591.log'.format(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")), 'w', 'utf-8'), ]
                   )

# %%
class Crawler591:
    
    def __init__(self):
        self.crawler = Crawler()
        self.logger = logging.getLogger('Crawler591')
    
    def get_details(self, save_dir):
        # 先取得已經下載的清單
        all_files = glob(save_dir + '\\' + '*.json')
        downloaded_list = [int(os.path.splitext(x.split('\\')[-1])[0]) for x in all_files]

        # 首頁連線
        home_page_html = self.crawler.get_html('https://rent.591.com.tw/')
        if home_page_html.status_code != requests.codes.ok:
            self.logger.warning('https://rent.591.com.tw/ 連線失敗')
            raise Exception

        # 取得 csrf-token
        soup = BeautifulSoup(home_page_html.text, "lxml")
        token_element = soup.find('meta', {'name': 'csrf-token'})
        csrf_token = token_element['content']

        # 獲取資料總數
        self.crawler.add_header('X-CSRF-TOKEN', csrf_token)
        list_pages_html = self.crawler.get_html('https://rent.591.com.tw/home/search/rsList?kind=0&region=8')
        if list_pages_html.status_code != requests.codes.ok:
            self.logger.warning('https://rent.591.com.tw/home/search/rsList?kind=0&region=8 連線失敗')
            raise Exception
        total_records_num = int(re.sub(',', '', json.loads(list_pages_html.text)['records']))

        self.logger.info('搜尋總數 {0} 筆資料'.format(total_records_num))

        # 抓個別頁面時 header 需要多 2 個參數
        t591 = home_page_html.cookies.get_dict()['T591_TOKEN']
        self.crawler.add_header('deviceid', t591)
        self.crawler.add_header('device', 'pc')
        
        # 逐頁取得個別 post_id
        # 並存檔
        current_page_num = 0
        while True:
            url = 'https://rent.591.com.tw/home/search/rsList?kind=0&region=8&firstRow={0}'.format(current_page_num*30)

            self.logger.info('執行第 {0} 頁, url: {1}'.format(current_page_num, url))

            current_page_html = self.crawler.get_html(url)
            self.crawler.sleep_random_secends()
            if current_page_html.status_code != requests.codes.ok:
                self.logger.warning('{0} 連線失敗'.format(url))
                raise Exception
            current_page = json.loads(current_page_html.text)
            post_ids = [x['post_id'] for x in current_page['data']['data']]

            if not post_ids:
                self.logger.info('下載結束!')
                break

            # 取得個別租案資料並存檔
            for post_id in post_ids:
                if post_id in downloaded_list:
                    self.logger.info('{0} 已經存在~將跳過!'.format(post_id))
                    continue
                
                house_url = 'https://bff.591.com.tw/v1/house/rent/detail?id={0}'.format(post_id)
                self.logger.debug('執行url: {0}'.format(house_url))
                house_html = self.crawler.get_html(house_url)
                if house_html.status_code != requests.codes.ok:
                    self.logger.warning('{0} 連線失敗'.format(house_url))
                    continue
                
                house_content = json.loads(house_html.text)
                with open(save_dir + '\\' + '{0}.json'.format(post_id), 'w', encoding='utf8') as f:
                    json.dump(house_content, f, indent=4,ensure_ascii=False)
                self.crawler.sleep_random_secends()

            current_page_num += 1

# %%
crawler591 = Crawler591()
crawler591.get_details(save_dir)

# %%



