import subprocess
import re
import string
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find("corpus/stopwords/english")
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
    nltk.download('averaged_perceptron_tagger')

STOPWORDS = set(stopwords.words('english'))


def remove_urls(text):
    return re.sub(r'https?://\S+|www.\.\S+', '', text)


def remove_emojis(text):
    # Reference: https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


def remove_punctuation(text, punctuation=None):
    if punctuation is None:
        punctuation = string.punctuation
    return text.translate(str.maketrans(punctuation, ' ' * len(punctuation)))


def remove_stopwords(text, stopwords=None):
    if stopwords is None:
        stopwords = STOPWORDS
    return ' '.join([word for word in text.split() if word not in stopwords])


def remove_extra_whitespace(text):
    return " ".join(text.split())


def postagger(token_words):
    return nltk.pos_tag(token_words)


def load_president_speeches():
    # !wget -q "https://www.dropbox.com/s/kow9mxovx7k84r6/corpus.zip"
    # subprocess.run(["wget", "-q", "https://www.dropbox.com/s/kow9mxovx7k84r6/corpus.zip"])
    # !unzip -o -q corpus.zip
    subprocess.run(["unzip", "-o", "-q", "corpus.zip"])
    import pandas as pd
    import glob

    rows = []
    for txtfile in glob.glob("corpus/*.txt"):
        _, _, filename = txtfile.partition("/")
        filename = filename.replace(".txt", "")
        year, _, president = filename.partition("-")
        with open(txtfile, "r") as file_:
            text = file_.read()
        rows.append((year, president, text))
    data = pd.DataFrame(rows, columns=["year", "president", "text"])
    return data
