"""
Useful for when you want to create a google docs table.
"""

import pandas as pd

df = pd.read_csv("decks/week006_deck.csv")

css = """
<style>
table {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    border: 1px solid black;
    padding: 5px;
}
th:nth-child(1) {
    width: 34%;
}
th:nth-child(2) {
    width: 66%;
}
</style>
"""
html = css + "<table><tr><th>Word / 단어</th><th>Sentence/Usage Notes</th></tr>"

for row in df.iterrows():
    row = row[1]
    html += f'<tr><td>{row["한국어 단어"]}<br/>{row["English Word"]}</td><td></td></tr>'

html += "</table>"

with open("deck.html", "w") as f:
    f.write(html)
