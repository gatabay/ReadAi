from jpype import JClass, java
from nltk import pos_tag, word_tokenize


def is_stop_word(w):
    with open("turkce-stop-words") as file:
        return w in file.read()


def find_word(w, l):
    for i in l:
        if w.lower() in i.lower():
            return i
    return False


def pos_tag_tr(sentences: list):
    words = list()
    markups = {"ADJ": list(), "NOUN": list(), "NUM": list(), "PRON": list(), "VERB": list()}

    TurkishMorphology: JClass = JClass("zemberek.morphology.TurkishMorphology")
    morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

    for sentence in sentences:
        _words = [word.strip().replace("\n", "").replace("\r", "").replace("\t", "") for word in sentence.split(" ")]

        words += _words

        analysis: java.util.ArrayList = (
            morphology.analyzeAndDisambiguate(sentence).bestAnalysis()
        )

        for i, analysis in enumerate(analysis):
            str_analysis = str(analysis)
            short, long = str_analysis.split(" ")
            _word = short.split(":")[0][1:]
            tag = short.split(":")[1][:-1].upper().strip()

            lem = str(analysis.getLemmas())[1:-1].split(",")[0].strip()
            word1 = find_word(lem, _words)
            word2 = find_word(_word, _words)

            word = word1 or word2

            print(f'LEM: {lem} | WORD: {word} | TAG: {tag}')

            if word is not False and not is_stop_word(word):
                if "NOUN" in tag:
                    markups["NOUN"].append(word)
                elif "NOUN" in tag and "TIME" in tag:
                    markups["NUM"].append(word)
                elif "VERB" in tag:
                    print(f'VERB: {word}')
                    markups["VERB"].append(word)
                elif "NUM" in tag:
                    markups["NUM"].append(word)
                elif "ADJ" in tag:
                    markups["ADJ"].append(word)
                elif "PRON" in tag:
                    markups["PRON"].append(word)

    for key, val in markups.items():
        markups[key] = " ".join(val)

    for key, val in markups.items():
        print(f'{key}: {markups[key]}')

    return words, markups


def pos_tag_en(sentences: list) -> [list, dict]:
    words = list()
    markups = {"ADJ": list(), "NOUN": list(), "NUM": list(), "PRON": list(), "VERB": list()}

    for sentence in sentences:
        words += [word.strip().replace("\n", "").replace("\r", "").replace("\t", "") for word in sentence.split(" ")]
        pos_tags = pos_tag(word_tokenize(sentence), tagset="universal")

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
                    if tag not in ["am",  "is", "are", "will", "won't", "has", "have"]:
                        markups[tag].append(word)

    for key, val in markups.items():
        markups[key] = " ".join(val)

    return words, markups


pos_taggers = {
    "en": pos_tag_en,
    "tr": pos_tag_tr
}