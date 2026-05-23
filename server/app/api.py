from cmath import e
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from ninja import NinjaAPI, File, Form
from ninja.files import UploadedFile
from ninja.responses import Response
import deepl
import os
import magic
import requests

from app import schema, services, selectors, models, constants
from core import models as core_models

api = NinjaAPI()

ALLOWED_EXTENSIONS = {".epub", ".kepub"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# epub and kepub are ZIP-based; python-magic reports them as application/zip or
# application/epub+zip depending on the version and file structure.
ALLOWED_MIME_TYPES = {
    ".epub": {"application/epub+zip", "application/zip"},
    ".kepub": {"application/epub+zip", "application/zip"},
}


@api.post("/login/")
def login(request, data: schema.LoginSchema):
    try:
        auth_user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    if auth_user.check_password(data.password):
        request.session["user_id"] = auth_user.id
        return Response({"message": "Login successful"}, status=200)

    else:
        return Response({"message": "Invalid password"}, status=401)


# @api.post("/signup/")
# def signup(request, data: schema.SignupSchema):
#     if User.objects.filter(email=data.email).exists():
#         return Response({"message": "Unable to create account"}, status=500)

#     try:
#         username = services.convert_email_to_username(data.email)
#     except Exception as error:
#         print(error)
#         username = data.email

#     try:
#         auth_user = User(username=username, email=data.email)
#         auth_user.set_password(data.password)
#         auth_user.save()

#         core_models.UserMeta.objects.create(user=auth_user)
#     except Exception as error:
#         print(error)
#         return Response({"message": "Unable to create account"}, status=500)

#     request.session["user_id"] = auth_user.id

#     return Response({"message": "Login successful"}, status=200)


@api.get("/languages")
def get_supported_languages(request):
    return Response({"languages": constants.SUPPORTED_LANGUAGES}, status=200)


@api.get("/supported-languages/")
def supported_languages(request):
    cache_key = "supported_languages"
    # cached = cache.get(cache_key)
    # if cached is not None:
    #     return Response({"languages": cached}, status=200)

    try:
        translator = deepl.Translator(settings.DEEPL_API_KEY)

        source_langs = translator.get_source_languages()
        target_langs = translator.get_target_languages()

        deepl_eng_codes = set()
        for lang in source_langs:
            code = lang.code.upper()
            if code != "EN":
                deepl_eng_codes.add(code)

        for lang in target_langs:
            code = lang.code.upper()
            base = code.split("-")[0]
            if base != "EN":
                deepl_eng_codes.add(code)

        resp = requests.get(
            f"https://texttospeech.googleapis.com/v1/voices?key={settings.GOOGLE_TTS_API_KEY}",
            timeout=10,
        )
        resp.raise_for_status()
        voices = resp.json().get("voices", [])

        tts_standard_codes = set()
        for voice in voices:
            if "Standard" in voice.get("name", ""):
                tts_standard_codes.update(voice.get("languageCodes", []))

        available = [
            d
            for d, t in TTS_LANGUAGE_MAP.items()
            if d in deepl_eng_codes and t in tts_standard_codes
        ]

        cache.set(cache_key, available, 3600)

        return Response({"languages": available}, status=200)

    except deepl.DeepLException as error:
        return Response({"error": f"DeepL API error: {str(error)}"}, status=400)
    except requests.RequestException as error:
        return Response({"error": f"TTS API error: {str(error)}"}, status=400)
    except Exception as error:
        return Response({"error": str(error)}, status=500)


@api.get("/dashboard/books")
def dashboard_books(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    response = {"continue_reading": [], "library": []}

    for book in models.Book.objects.filter(uploaded_by_id=user_id).values("id", "title", "author"):
        response["library"].append(
            {"id": book["id"], "title": book["title"], "author": book["author"]}
        )

    books_in_progress = models.BookProgress.objects.filter(user_id=user_id).values(
        "book_id", "book__title", "book__author", "sentence_last_read", "book__is_public"
    )

    for book_progress in books_in_progress:
        if book_progress["sentence_last_read"] > 0:
            response["continue_reading"].append(
                {
                    "id": book_progress["book_id"],
                    "title": book_progress["book__title"],
                    "author": book_progress["book__author"],
                    "sentence_last_read": book_progress["sentence_last_read"],
                }
            )

        # A public book will show up in "library" but not in "continue_reading" if the user hasn't read it yet
        elif book_progress["sentence_last_read"] == 0 and book_progress["book__is_public"]:
            response["library"].append(
                {
                    "id": book_progress["book_id"],
                    "title": book_progress["book__title"],
                    "author": book_progress["book__author"],
                }
            )

    return Response(response, status=200)


@api.post("/read/")
def read(request, data: schema.BookSchema):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    if services.verify_book_access(data.book_id, user_id) is False:
        return Response({"error": "Access denied"}, status=403)

    try:
        book = models.Book.objects.get(id=data.book_id)
    except models.Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    epub_file = book.file

    epub = services.convert_epub_to_str(epub_file)
    epub_cleaned = services.remove_html(epub)

    sentence_last_read = selectors.get_sentence_last_read(user_id, data.book_id) or 0

    # Pagination
    # sentence_last_read stores sentence_first of the last viewed page
    if data.page_turn == "next":
        sentence_first = sentence_last_read + 5
    elif data.page_turn == "previous":
        sentence_first = max(0, sentence_last_read - 5)
    else:
        sentence_first = sentence_last_read

    # TODO calculate this based on character limit
    sentence_last = sentence_first + 4

    sentences = services.convert_text_to_sentences(epub_cleaned, sentence_first, sentence_last)

    models.BookProgress.objects.update_or_create(
        book_id=data.book_id, user_id=user_id, defaults={"sentence_last_read": sentence_first}
    )

    return Response(
        {
            "sentences": sentences,
            "sentence_count": services.get_total_sentence_count(epub_cleaned),
            "sentence_last_read": sentence_last,
            "sentence_first": sentence_first,
            "has_previous": sentence_first > 0,
        },
        status=200,
    )


@api.post("/translate/")
def translate(request, data: schema.TranslationSchema):
    try:
        translated = services.translate(data.text, data.source, data.target, data.context)

        return Response({"translated": translated.text}, status=200)

    except deepl.DeepLException as error:
        return Response({"error": f"DeepL API error: {str(error)}"}, status=400)

    except Exception as error:
        return Response({"error": f"Translation error: {str(error)}"}, status=500)


@api.post("/books/upload")
def upload_book(request, data: Form[schema.BookUploadSchema], file: UploadedFile = File(...)):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    if file.size > MAX_FILE_SIZE:
        return Response({"error": "File exceeds the 50 MB size limit"}, status=400)

    if data.language not in constants.SUPPORTED_LANGUAGES:
        return Response(
            {
                "error": f"Invalid language. Supported languages: {', '.join(constants.SUPPORTED_LANGUAGES)}"
            },
            status=400,
        )

    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return Response(
            {"error": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"},
            status=400,
        )

    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if mime not in ALLOWED_MIME_TYPES[ext]:
        return Response({"error": "File content does not match the expected type"}, status=400)

    file_type = ext.lstrip(".")

    book = models.Book(
        title=data.title,
        author=data.author,
        language=data.language,
        file=file,
        file_type=file_type,
        uploaded_by_id=user_id,
    )
    book.save()

    return Response({"id": book.id, "message": "Book uploaded successfully"}, status=201)


# Maps DeepL language codes to BCP-47 codes for Google TTS
TTS_LANGUAGE_MAP = {
    "IT": "it-IT",
    "EN-GB": "en-GB",
    "EN-US": "en-US",
    "DE": "de-DE",
    "FR": "fr-FR",
    "ES": "es-ES",
    "PT-PT": "pt-PT",
    "PT-BR": "pt-BR",
    "NL": "nl-NL",
    "PL": "pl-PL",
    "RU": "ru-RU",
    "JA": "ja-JP",
    "ZH": "zh-CN",
}


@api.post("/tts/")
def tts(request, data: schema.TTSSchema):
    language_code = TTS_LANGUAGE_MAP.get(data.language.upper())

    try:
        audio_content = services.text_to_speech(data.text, language_code, data.speed)
        return Response({"audio": audio_content}, status=200)
    except ValueError as error:
        return Response({"error": str(error)}, status=500)
    except requests.RequestException as error:
        return Response({"error": f"TTS error: {str(error)}"}, status=500)
