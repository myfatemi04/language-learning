import json
import os
import sys
import time

import pandas as pd

os.chdir(os.path.dirname(__file__) + "/..")


def make_deck(num_words, week_number):
    # edit the 'korean_wordlist.csv' file.
    df_src = pd.read_csv(
        os.path.dirname(__file__) + "/korean_wordlist_queue.csv", index_col=0
    )
    # take the first 'num_words' rows
    df_remaining = df_src.iloc[num_words:]
    df_remaining.to_csv(
        os.path.dirname(__file__) + "/korean_wordlist_queue.csv", index=True
    )
    df = df_src.head(num_words)
    df.drop(columns=["category", "difficulty"], inplace=True)
    df.rename(
        {
            "korean_word": "한국어 단어",
            "english_translation": "English Word",
            "mandarin_translation": "汉语单词",
            "mandarin_pinyin": "汉语拼音",
        },
        axis=1,
        inplace=True,
    )
    df["Image"] = ["" for _ in range(num_words)]
    d = os.path.dirname(__file__) + "/../decks"
    df.to_csv(f"{d}/week{week_number:03d}_deck.csv", index=False)

    with open("wordlists/queue_write_log.json") as f:
        log = json.load(f)

    log.append(
        {
            "timestamp": time.time(),
            "action": "make_deck",
            "target": f"week{week_number:03d}_deck.csv",
            "start_index": int(df.index[0]),
            "end_index": int(df_remaining.index[0]),
        }
    )

    with open("wordlists/queue_write_log.json", "w") as f:
        json.dump(log, f)

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
        html += (
            f'<tr><td>{row["한국어 단어"]}<br/>{row["English Word"]}</td><td></td></tr>'
        )

    html += "</table>"

    with open("deck.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    make_deck(int(sys.argv[1]), int(sys.argv[2]))
