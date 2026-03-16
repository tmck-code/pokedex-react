#!/usr/bin/env python3
'''
to run in regular mode:
./scripts/scraper.py

or, to resume after all the image urls have been collected:
./scripts/scraper.py urls.ndjson
'''

import asyncio
import os
import json
import sys
import time

import aiohttp
import requests
from bs4 import BeautifulSoup
from laser_prynter import pp, pbar

from collections import namedtuple

SetInfo = namedtuple("Set", "code url name")
CardInfo = namedtuple("Card", "img_url")


async def adownload_image(url, odirname, ofname, i, pb: pbar.PBar, retries: int = 5, wait_time: int = 10):
    ofpath = os.path.join(odirname, ofname)

    if os.path.exists(ofpath):
        pp.ppd(
            {"i": i, "total": pb.t, "ofpath": ofpath, "url": url, "status": "skipping"},
            style="fruity", indent=None
        )
        pb.update(1)
        return

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        for attempt in range(retries):
            try:
                pp.ppd({"i": i, "total": pb.t, "url": url, "status": "requesting"}, indent=None)

                async with session.get(url) as resp:
                    response = await resp.read()
                    resp.raise_for_status()

                    with open(os.path.join(odirname, ofname), "wb") as f:
                        f.write(response)

                pp.ppd({"i": i, "total": pb.t, "ofpath": ofpath, "url": url, "status": "written"}, style="material", indent=None)
                pb.update(1)
                return

            except Exception as e:
                print("error, retrying", url, e)
                await asyncio.sleep(wait_time)
        else:
            raise Exception(f"failed to download {url} after {retries} attempts")


from itertools import batched

async def adownload_all_images(urls, odir, pb: pbar.PBar, chunk: int = 10):
    for batch in batched(urls, chunk):
        tasks = []
        for i, url in enumerate(batch):
            try:
                name, set_name, number_in_set, *_extra = url.split("/")[-1].split(".")

            except ValueError as e:
                pp.ppd({"url": url, "error": str(e)}, style="fruity", indent=None)
                pb.update(1)
                continue

            ofname = f"{number_in_set}_{name}.png"
            odirpath = os.path.join(odir, set_name)
            os.makedirs(odirpath, exist_ok=True)

            tasks.append(adownload_image(url, odirpath, ofname, i, pb))

        await asyncio.gather(*tasks)

def request_with_retries(method: str, url: str, retries: int = 5, wait_time: int = 10):
    for attempt in range(1, retries+1):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return resp
        except Exception as e:
            pp.ppd({'attempt': attempt, 'error': {'class': e.__class__.__name__, 'msg': str(e)}}, indent=None, style='fruity')
            time.sleep(wait_time)
    else:
        raise Exception(f'failed to request {url} after {retries} attempts')


def find_all_cards(url):
    soup = BeautifulSoup(request_with_retries('get', url).text, "lxml")

    for i, card in enumerate(soup.find_all("div", {"class": "card"})):
        img_url = card.find("img", {"class": "card lazyload"}).attrs["data-src"]

        card_info = CardInfo(**{"img_url": img_url.replace("thumb.png", "png")})
        pp.ppd(card_info._asdict(), indent=None)

        yield card_info


def find_all_sets(url):
    print("finding sets for url", url, "lxml")
    soup = BeautifulSoup(requests.get(url).text, "lxml")

    for btn in soup.find_all("a", {"class": "button"}):
        info = SetInfo(
            **{
                "code": btn.attrs["name"],
                "name": btn.attrs["title"],
                "url": f"https://jp.pokellector.com{btn.attrs['href']}",
            }
        )
        pp.ppd(info._asdict(), indent=None)
        yield info


def run(url, odir="cards", ifpath: str = None):
    print("finding all sets, cards & images from", url)
    urls = []
    sets = list(find_all_sets(url))

    if ifpath is not None:
        urls = []
        with open(ifpath) as istream:
            for line in istream:
                urls.append(CardInfo(**json.loads(line)).img_url)

        with pbar.PBar(total=len(urls)) as pb:
            asyncio.run(adownload_all_images(urls, odir=odir, pb=pb))
        return

    with pbar.PBar(total=len(sets)) as pb, open('urls.ndjson', 'w') as ostream:
        for i, card_set in enumerate(sets):
            pp.ppd(card_set._asdict(), indent=None)

            for card in find_all_cards(card_set.url):
                urls.append(card.img_url)
                print(json.dumps(card._asdict()), file=ostream)

            pb.update(1)

    with pbar.PBar(total=total) as pb:
        asyncio.run(adownload_all_images(urls, odir=odir, pb=pb))


if __name__ == "__main__":
    run("https://jp.pokellector.com/sets/", ifpath=sys.argv[1] if len(sys.argv) > 1 else None)

