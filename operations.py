from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from newspaper import Article




def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    if not article.is_parsed:
        raise ValueError("Unexpected Article")

    return article.text




def parse_article(url):
    result = list()
    text = get_article(url)
    pos_tags = pos_tag(word_tokenize(text), tagset="universal")

    for word, tag in pos_tags:
        if tag == "ADJ":
            result.append((word, "red"))
        elif tag == "NOUN":
            result.append((word, "green"))
        elif tag == "NUM":
            result.append((word, "blue"))
        elif tag == "PRON":
            result.append((word, "purple"))
        elif tag == "VERB":
            result.append((word, "orange"))
        else:
            result.append((word, "black"))

    return result
