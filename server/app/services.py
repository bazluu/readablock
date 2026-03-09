import os
import random
import string

from django.conf import settings

from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from textblob import TextBlob
import deepl


def convert_email_to_username(email: str, length: int = 6) -> str:
    seed = email
    chars = string.ascii_lowercase + string.digits

    rng = random.Random(seed)
    random_string = "".join(rng.choices(chars, k=length))

    username = email.split("@")[0] + "#" + random_string

    return username


def get_total_sentence_count(text: str) -> int:
    blob = TextBlob(text)
    total = len(blob.sentences)

    return total


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
    epub_path = os.path.join(os.path.dirname(__file__), "../Gatto e topo in società.epub")

    book = epub.read_epub(epub_path)

    text = []
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            content = item.get_content().decode("utf-8")
            text.append(content)

    full_text = "\n".join(text)

    return full_text


def translate(text: str, source: str | None, target: str, context: str | None):
    """
    Translation using DeepL API

    Parameters:
    - text: The text to translate
    - source: Source language code (optional, auto-detect if not provided)
    - target: Target language code (default: EN-GB)
    - context: Text related to the word to be translated, in the same language (optional)

    Returns translated text with language information
    """
    translator = deepl.Translator(settings.DEEPL_API_KEY)

    translated = translator.translate_text(
        text, source_lang=source, target_lang=target, context=context
    )

    return translated
