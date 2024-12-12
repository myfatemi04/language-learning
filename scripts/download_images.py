"""
This file is used to automatically download images to go with a deck.
First, get the Google Programmatic Search Engine API.

https://programmablesearchengine.google.com/controlpanel/create

Then, take the API key and use it to make requests.

https://developers.google.com/custom-search/v1/using_rest

"""

import json
import requests
import os
import urllib.parse
import matplotlib.pyplot as plt

cx = os.getenv("GOOGLE_CUSTOM_SEARCH_ID")
key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")


def select_image(query: str):
    request_url = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}:omuauf_lfve&q={query}&searchType=image&num=10".format(
        key=urllib.parse.quote_plus(key),  # type: ignore
        cx=urllib.parse.quote_plus(cx),  # type: ignore
        query=urllib.parse.quote_plus(query),  # type: ignore
    )
    response = requests.get(request_url)

    print(request_url)

    if response.status_code != 200:
        print("Response gave an error!")
        print(response.text)
        return

    search_result = response.json()
    items = search_result["items"]

    for item in items:
        # Display the first 4 images.
        thumbnail_link = item["thumbnailLink"]

        if len(thumbnail_link) > 1000:
            print(thumbnail_link[:10])
        else:
            print(thumbnail_link)

        # plt.imshow()

    with open("search_result.json", "w") as f:
        json.dump(search_result, f)


select_image("heel")
