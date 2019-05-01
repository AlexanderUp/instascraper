# encoding:utf-8
# scraper to grab images from instagram


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import re
import os
import json

from instascraper_config import URL
from instascraper_config import IMAGE_URL
from instascraper_config import OUTPUT_DIRECTORY

# ['entry_data']['ProfilePage'][0]['graphql']['user']['username']
# ['entry_data']['ProfilePage'][0]['graphql']['user']['id']
# ['entry_data']['ProfilePage'][0]['graphql']['user']['connected_fb_page']
# print(json.dumps(file['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]["edges"][0]['node']['display_url'], indent=4))


def parse_page(url=URL):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, features="lxml")
    script_text_list = bsObj.findAll('script', {'type':'text/javascript'}) # intermediate variable
    script_text_list = [x.get_text() for x in script_text_list]
    for candidate in script_text_list:
        if candidate.startswith('window._sharedData = '):
            json_file = candidate[21:-1] # to ignore 'window._sharedData = ' (len is 21) and last one
    image_urls = []
    file = json.loads(json_file)
    for i in range(len(file['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]["edges"])):
        image_urls.append(file['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]["edges"][i]['node']['display_url'])
    return image_urls

def download_images(image_urls):
    for url in image_urls:
        get_image(url)
    print('{} images downloaded!'.format(len(image_urls)))
    return None

def get_image(url=IMAGE_URL):
    source = urlopen(url).read()
    output_file_name = get_image_name(url)
    destination = OUTPUT_DIRECTORY + '/' + output_file_name
    if os.path.exists(destination):
        print('File {} already exists! Skipping...'.format(output_file_name))
    else:
        with open(destination, 'wb') as f:
            f.write(source)
        print('File {} written!'.format(output_file_name))
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
    download_images(parse_page())
