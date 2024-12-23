# here is a script to 'bump' a word if I have seen it recently and I want to remember it.
import json
import os
import sys
import time

import pandas as pd


os.chdir(os.path.dirname(__file__) + "/..")


def bump_word(word):
    deck_csvs = []
    for deck_csv_filename in os.listdir("decks"):
        if deck_csv_filename.endswith(".csv"):
            deck_csvs.append(
                (deck_csv_filename, pd.read_csv("decks/" + deck_csv_filename))
            )

    # load the bank of words
    df_src = pd.read_csv("wordlists/korean_wordlist_queue.csv", index_col=0)

    # find the word in the bank.
    # it should be a Korean word.
    word_row = df_src[df_src["korean_word"] == word]
    if word_row.empty:
        print(f"Word '{word}' not found in the bank. It may already be in a deck.")
        return

    index_val = word_row.index

    print("Found word with index", index_val)
    print("OK to remove this word from the queue? (y/n)")
    response = input()
    if response != "y":
        print("Exiting.")
        return

    # append the word to the deck.
    target_filename, target_df = deck_csvs[-1]
    target_df: pd.DataFrame
    target_df.loc[len(target_df)] = [
        word_row["korean_word"].values[0],
        word_row["english_translation"].values[0],
        word_row["mandarin_translation"].values[0],
        word_row["mandarin_pinyin"].values[0],
        "",  # 'image'
    ]

    with open("queue_write_log.json") as f:
        log = json.load(f)

    log.append(
        {
            "timestamp": time.time(),
            "action": "bump",
            "target": target_filename,
            "index": int(index_val),
        }
    )

    with open("queue_write_log.json", "w") as f:
        json.dump(log, f)

    target_df.to_csv("decks/" + target_filename, index=False)

    # remove the word from the queue.
    df_src.drop(index_val, inplace=True)
    df_src.to_csv("wordlists/korean_wordlist_queue.csv")


if __name__ == "__main__":
    bump_word(sys.argv[1])
