import logging
import random
import time

import requests

from Header import header






class Crawler:
    
    def __init__(self):
        self.session = requests.session()
        self._header = header
        self.random_sleep_min = 2
        self.random_sleep_max = 6

    @property
    def header(self):
        return self._header

    def add_header(self, _key, _value):
        self._header[_key] = _value
            
    def get_html(self, url):
        html = self.session.get(url, headers=self._header)
        return html

    def sleep_random_secends(self):
        time.sleep(random.uniform(self.random_sleep_min, self.random_sleep_max))