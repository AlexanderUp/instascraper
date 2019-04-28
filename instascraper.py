# encoding:utf-8
# scraper to grab images from instagram


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from io import StringIO

import re
import os

from instascraper_config import URL
from instascraper_config import IMAGE_URL
from instascraper_config import OUTPUT_DIRECTORY


def get_html(url=URL):
    html = urlopen(url)
    # print('html:')
    # print(html.read())
    bsObj = BeautifulSoup(html, features="lxml")
    return None

def get_image(url=IMAGE_URL):
    source = urlopen(url).read()
    output_file_name = get_image_name(url)
    destination = OUTPUT_DIRECTORY + '/' + output_file_name
    with open(destination, 'wb') as f:
        f.write(source)
    print('File written!')
    print('File name: {}'.format(output_file_name))
    return None

def get_image_name(url=IMAGE_URL):
    url_splitted = [x for x in url.split('/') if x]
    pattern = r'(?P<image_name>^[a-z0-9_]*\.jpg)\?'
    p = re.compile(pattern, re.I)
    for part in url_splitted:
        temp = p.search(part)
        if temp is not None:
            return temp['image_name']
    return None


if __name__ == '__main__':
    print('*' * 125)
    # get_html()
    get_image()
    # print(get_image_name())
