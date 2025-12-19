import os

from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from textblob import TextBlob


def convert_text_to_sentences(text: str, start: int, end: int):
    blob = TextBlob(text)

    sentences = []
    for sentence in blob.sentences[start:end]:
        sentences.append(str(sentence))

    return sentences

def remove_html(text: str):
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)

    return clean_text

def convert_epub_to_str():
    epub_path = os.path.join(
        os.path.dirname(__file__),
        "../Gatto e topo in società.epub"
    )

    book = epub.read_epub(epub_path)

    text = []
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            content = item.get_content().decode("utf-8")
            text.append(content)

    full_text = "\n".join(text)

    return full_text
