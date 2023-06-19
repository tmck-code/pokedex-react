#!/usr/bin/env python3

import os, sys
import asyncio

import aiohttp
import requests

async def adownload_image(url, odirname, ofname, i):
    print(i, ofname, url)
    await asyncio.sleep(0)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(url) as resp:
                response = await resp.read()
                with open(os.path.join(odirname, ofname), 'wb') as f:
                    f.write(response)
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print('error, retrying', url, e)
            await asyncio.sleep(2)

async def adownload_all_images(urls, chunk=10):
    tasks = []
    for i, url in enumerate(urls):
        name, set_name, number_in_set, _id, _ext = url.split('/')[-1].split('.')
        ofname = f'{number_in_set}_{name}.png'
        odirname = set_name
        os.makedirs(odirname, exist_ok=True)

        tasks.append(adownload_image(url, odirname, ofname, i))


        if i % chunk == 0:
            print('downloading 10 images')
            await asyncio.gather(*tasks)
            tasks = []

    await asyncio.gather(*tasks)


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
    print(f'found {len(urls)} images')

    asyncio.run(adownload_all_images(urls))


if __name__ == '__main__':
    url = sys.argv[1]
    run(url)
