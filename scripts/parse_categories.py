import json
import re

import bs4

for lang in ["en", "zh"]:
    column_names = ["Elementary", "Intermediate", "Advanced"]
    categories = []

    categories_html = bs4.BeautifulSoup(
        open(f"category_table_{lang}.html"), "html.parser"
    )

    trs = categories_html.select_one("tbody").select("tr")  # type: ignore
    for row in trs:
        for column, td in enumerate(row.select("td")):
            if td.text.strip():
                categories.append(
                    {
                        "category": re.sub("\\s+", " ", td.text.strip()),
                        "level": column_names[column],
                        "id": td.select_one("input").attrs["value"],
                    }
                )

    with open(f"categories_{lang}.json", "w") as f:
        json.dump(categories, f)
