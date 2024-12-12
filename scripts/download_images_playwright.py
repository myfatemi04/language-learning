"""
Google APIs are too annoying to use. It is easier for me to just use Playwright.
"""

import playwright
from playwright.sync_api import Playwright, Browser, Page, sync_playwright, Locator
import matplotlib.pyplot as plt
from urllib.parse import quote_plus


def select_image(page: Page, query: str):
    page.goto("http://www.google.com/search?q=" + quote_plus(query))
    page.get_by_role("link", name="Images").first.click()

    input()

    # Lowkey this is all I need to be saving time. I can just screen cap the image I want and paste it into the desired folder.

    # Get the results.
    # links_to_click: list[Locator] = []
    # for link in page.locator("h3 > a").all():
    #     print(link)
    #     href = link.get_attribute("href")
    #     if href and href.startswith("/imgres"):
    #         links_to_click.append(link)

    # image_sources: list[str] = []

    # for link in links_to_click:
    #     link.click()

    #     possible_images = page.locator("dialog > img").all()
    #     for image in possible_images:
    #         src = image.get_attribute("src")
    #         if src and ".gstatic.com" not in src:
    #             image_sources.append(src)


import pandas as pd

words = pd.read_csv("../decks/week001_deck.csv")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context()
    page = ctx.new_page()

    for word in words["English word"]:
        select_image(page, word)
