"""
Useful for when you want to create a google docs table.
"""

import pandas as pd

df = pd.read_csv("decks/week005_deck.csv")
df = df.drop(columns=["Image"])
with open("deck.html", "w") as f:
    f.write(df.style.to_html(index=False))
