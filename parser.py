import os
import re
from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import word_tokenize


def get_token_vector(text, language="german"):
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

        print(Counter(nltk_tokens))
    except LookupError:
        raise ValueError("Please supply a valid text language")


if __name__ == "__main__":
    html_dir = "htmls"

    for fname in os.listdir(html_dir):
        print(fname[-4:])
        if fname[-4:] != "html":
            continue

        fpath = os.path.join(html_dir, fname)
        print(fpath)
        with open(fpath) as f:
            html = f.read()
            soup = BeautifulSoup(html, features="html.parser")
            text = soup.find(id="readspeaker-content").text
            get_token_vector(text)
