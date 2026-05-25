import io
import os
import random
import string
import uuid

from django.conf import settings

from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from textblob import TextBlob
import deepl
import requests

from app import models
from app.constants import LANGUAGES


def get_supported_languages():
    supported = [{"name": "Latin", "deepl": "LA", "google_tts": None, "marc": "lat"}]
    for lang in LANGUAGES:
        if lang["deepl"] and lang["google_tts"]:
            supported.append(lang)

    return supported


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


def convert_epub_to_str(file):
    with file.open("rb") as f:
        data = f.read()

    book = epub.read_epub(io.BytesIO(data))

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


def get_book_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()

    return f"books/{uuid.uuid4()}{ext}"


def verify_book_access(book_id: int, user_id: int) -> bool:
    book = models.Book.objects.get(id=book_id)

    if book.is_public:
        return True

    if book.uploaded_by_id == user_id:
        return True

    return False


def text_to_speech(text, language_code, speed=0.9, tier="Standard", variant="A"):
    if not settings.GOOGLE_TTS_API_KEY:
        raise ValueError("TTS not configured")

    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": language_code,
            "name": f"{language_code}-{tier}-{variant}",
            "ssmlGender": "NEUTRAL",
        },
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": speed},
    }

    response = requests.post(
        f"https://texttospeech.googleapis.com/v1/text:synthesize?key={settings.GOOGLE_TTS_API_KEY}",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()

    return response.json().get("audioContent", "")
