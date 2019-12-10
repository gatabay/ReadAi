from newspaper import Article
from langdetect import detect
from find_pos import pos_taggers, is_stop_word
from summa import summarizer, keywords
from sentence_splitter import split_text_into_sentences


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()

    if not article.is_parsed:
        raise ValueError("Unexpected Article")

    return article.text


def parse_article(url):
    text = get_article(url)

    summary = summarizer.summarize(text)

    lang = detect(text)

    print(f'LANG: {lang}')

    sentences = split_text_into_sentences(text=text, language=lang)
    sentences = [s for s in sentences if s.strip()]

    tagger = pos_taggers[lang]

    words, markups = tagger(sentences)

    _keywords = keywords.keywords(text).split("\n")

    _keywords = [k for k in _keywords if not is_stop_word(k)]

    markups["KEYWORD"] = _keywords

    return words, markups, summary
