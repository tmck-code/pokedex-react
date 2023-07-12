#!/usr/bin/env python3

import os, sys
import asyncio

import aiohttp
import requests

async def adownload_image(url, odirname, ofname, i, total):
    print(f'{i}/{total} {ofname:<40s} {url}')
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

async def adownload_all_images(urls, odir, total, chunk=10):
    tasks = []
    for i, url in enumerate(urls):
        name, set_name, number_in_set, _id, _ext = url.split('/')[-1].split('.')
        ofname = f'{number_in_set}_{name}.png'
        odirpath = os.path.join(odir, set_name)
        os.makedirs(odirpath, exist_ok=True)

        tasks.append(adownload_image(url, odirpath, ofname, i, total))

        if i % chunk == 0:
            await asyncio.gather(*tasks)
            tasks = []

    await asyncio.gather(*tasks)

def find_image_urls(html):
    for i, line in enumerate(html.split('\n')):
        if 'thumb.png' in line:
            yield line.split('"')[3].removesuffix('thumb.png') + 'png'

def run(url, odir):
    response = requests.get(url)
    urls = list(find_image_urls(response.text))
    print(f'found {len(urls)} images')

    asyncio.run(adownload_all_images(urls, odir=odir, total=len(urls)))

if __name__ == '__main__':
    url, odir = sys.argv[1:]
    run(url, odir)
