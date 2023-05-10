#!/usr/bin/env python3

import os, sys
import requests

def find_image_urls(html):
    for i, line in enumerate(html.split('\n')):
        if 'thumb.png' in line:
            yield line.split('"')[3].removesuffix('thumb.png') + 'png'

def download_image(url, odirname, ofname):
    os.makedirs(odirname, exist_ok=True)
    with open(os.path.join(odirname, ofname), 'wb') as f:
        f.write(requests.get(url).content)

def run(url):
    response = requests.get(url)
    urls = list(find_image_urls(response.text))
    print(f'found {len(urls)} images', urls)

    for i, url in enumerate(urls):
        name, set_name, number_in_set, _id, _ext = url.split('/')[-1].split('.')
        ofname = f'{number_in_set}_{name}.png'
        print(f'{i}/{len(urls)}', set_name, ofname, url)

        download_image(url, set_name, ofname)

if __name__ == '__main__':
    url = sys.argv[1]
    run(url)
