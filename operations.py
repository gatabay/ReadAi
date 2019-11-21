from nltk.tag import pos_tag
from newspaper import Article
from nltk.tokenize import word_tokenize


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    if not article.is_parsed:
        raise ValueError("Unexpected Article")

    return article.text


def parse_article(url):
    markups = {"ADJ": list(), "NOUN": list(), "NUM": list(), "PRON": list(), "VERB": list()}
    text = get_article(url)
    words = [word.strip().replace("\n", "").replace("\r", "").replace("\t", "") for word in text.split(" ")]
    pos_tags = pos_tag(word_tokenize(text), tagset="universal")

    for word, tag in pos_tags:
        if tag in markups.keys():
            if tag == "ADJ":
                markups[tag].append(word)
            elif tag == "NOUN":
                markups[tag].append(word)
            elif tag == "NUM":
                markups[tag].append(word)
            elif tag == "PRON":
                markups[tag].append(word)
            elif tag == "VERB":
                if tag not in ["am", "is", "are", "will", "won't", "has", "have"]:
                    markups[tag].append(word)

    for key, val in markups.items():
        markups[key] = " ".join(val)

    return words, markups
