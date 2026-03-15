#!/usr/bin/env python3

import os
import asyncio

import aiohttp
import requests
from bs4 import BeautifulSoup
from laser_prynter import pp, pbar

from collections import namedtuple

SetInfo = namedtuple("Set", "code url name")
CardInfo = namedtuple("Card", "img_url")


async def adownload_image(url, odirname, ofname, i, total, pb: pbar.PBar):
    ofpath = os.path.join(odirname, ofname)

    if os.path.exists(ofpath):
        pp.ppd(
            {
                "i": i,
                "total": total,
                "ofpath": ofpath,
                "url": url,
                "status": "skipping",
            },
            style="fruity",
            indent=None,
        )
        pb.update(1)
        return

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        try:
            async with session.get(url) as resp:
                response = await resp.read()
                with open(os.path.join(odirname, ofname), "wb") as f:
                    f.write(response)
            pp.ppd(
                {
                    "i": i,
                    "total": total,
                    "ofpath": ofpath,
                    "url": url,
                    "status": "written",
                },
                style="material",
                indent=None,
            )
            pb.update(1)
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print("error, retrying", url, e)
            await asyncio.sleep(2)


async def adownload_all_images(urls, odir, total, chunk=10):
    tasks = []
    with pbar.PBar(total=total) as pb:
        for i, url in enumerate(urls):
            try:
                name, set_name, number_in_set, *_extra = url.split("/")[-1].split(".")
            except ValueError as e:
                pp.ppd({"url": url, "error": str(e)}, style="fruity", indent=None)
                pb.update(1)
                continue
            ofname = f"{number_in_set}_{name}.png"
            odirpath = os.path.join(odir, set_name)
            os.makedirs(odirpath, exist_ok=True)

            tasks.append(adownload_image(url, odirpath, ofname, i, total, pb))

            if i % chunk == 0:
                await asyncio.gather(*tasks)
                tasks = []

        await asyncio.gather(*tasks)


def find_all_cards(url):
    print("finding images for url", url)
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    print("Received response for", url)
    for i, card in enumerate(soup.find_all("div", {"class": "card"})):
        img_url = card.find("img", {"class": "card lazyload"}).attrs["data-src"]
        card_info = CardInfo(**{"img_url": img_url.replace("thumb.png", "png")})
        pp.ppd(card_info._asdict(), indent=None)
        yield card_info


def find_all_sets(url):
    print("finding sets for url", url, "html.parser")
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for btn in soup.find_all("a", {"class": "button"}):
        info = SetInfo(
            **{
                "code": btn.attrs["name"],
                "url": f"https://jp.pokellector.com{btn.attrs['href']}",
                "name": btn.attrs["title"],
            }
        )
        pp.ppd(info._asdict(), indent=None)
        yield info


def run(url, odir="cards"):
    print("finding all sets, cards & images from", url)
    urls = []
    sets = list(find_all_sets(url))
    with pbar.PBar(total=len(sets)) as pb:
        for i, card_set in enumerate(sets):
            pp.ppd(card_set._asdict(), indent=None)

            for card in find_all_cards(card_set.url):
                urls.append(card.img_url)
            pb.update(1)

    asyncio.run(adownload_all_images(urls, odir=odir, total=len(urls)))


if __name__ == "__main__":
    run("https://jp.pokellector.com/sets/")
