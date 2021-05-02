import os
import re
import random
import json

from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import word_tokenize


def get_token_counter(text, language="german"):
    """Simple text preparation

    Args:
        token_vector ([type]): [description]
        language (str, optional): [description]. Defaults to "german".

    Raises:
        ValueError: [description]
    """
    try:
        # remove numbers
        text = re.sub(r"\d+", "", text)

        # Tokenize
        nltk_tokens = word_tokenize(text)

        # Remove stopwords
        special_chars = [".", "!", ",", "?", "#", ":", "(", ")", "-"]
        german_stop_words = set(stopwords.words("german") + special_chars)
        nltk_tokens = [token for token in nltk_tokens if token not in german_stop_words]
        return Counter(nltk_tokens)
    except LookupError:
        raise ValueError("Please supply a valid text language")


def random_select(token_counter: Counter, size=15):
    """Select k token randomly weighted by their frequency

    Args:
        token_counter (Counter): [description]
        size (int, optional): [description]. Defaults to 15.
    """
    # Return all if input size is smaller than target
    if len(token_counter) < size:
        return token_counter.keys()

    selection = set()
    while len(selection) < size:
        rnd_token = random.choices(
            population=list(token_counter.keys()),
            weights=token_counter.values(),
            cum_weights=None,
            k=1,
        )[0]
        selection.add(rnd_token)

        del token_counter[rnd_token]
    return selection


# TODO
# 3) Build trainings json according to requirements
# 4) Build OpenAI API utility

if __name__ == "__main__":
    html_dir = "htmls"
    lines = []
    with open("train.json") as train_file:
        validation_content = json.load(train_file)

        for row in validation_content:
            file_name = row["file"]
            selector = row["contentSelector"]
            label = row["label"]

            fpath = os.path.join(html_dir, row["file"])

            with open(fpath) as html_file:
                html = html_file.read()
                soup = BeautifulSoup(html, features="html.parser")
                text = soup.select(selector)[0].text
                token_counter = get_token_counter(text)
                token_vector_sample = random_select(token_counter)

                line = json.dumps(
                    {"text": " ".join(token_vector_sample), "label": label}
                )
                lines.append(line + "\n")

    with open("train_parsed.json", "w") as out_file:
        out_file.writelines(lines)
