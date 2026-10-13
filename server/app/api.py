from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.http import FileResponse

from ninja import NinjaAPI, File, Form
from ninja.files import UploadedFile
from ninja.responses import Response
import deepl
import secrets
import os
import magic
import requests
from datetime import date

from app import schema, services, selectors, models, constants
from app.constants import DEEPL_TO_GOOGLE
from core import models as core_models

api = NinjaAPI()

ALLOWED_EXTENSIONS = {".epub", ".kepub", ".txt"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# epub and kepub are ZIP-based; python-magic reports them as application/zip or
# application/epub+zip depending on the version and file structure.
ALLOWED_MIME_TYPES = {
    ".epub": {"application/epub+zip", "application/zip"},
    ".kepub": {"application/epub+zip", "application/zip"},
    ".txt": {"text/plain"}
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


@api.post("/logout/")
def logout(request):
    request.session.flush()
    return Response({"message": "Logged out"}, status=200)


@api.get("/user")
def user(request):
    try:
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser,
            },
            status=200,
        )

    except (KeyError, User.DoesNotExist):
        return Response({"error": "Authentication required"}, status=401)


@api.post("/update-word-goal")
def update_word_goal(request, data: schema.WordGoalSchema):
    try:
        user = User.objects.get(id=request.session["user_id"])
    except (KeyError, User.DoesNotExist):
        return Response({"error": "Authentication required"}, status=401)

    if data.word_goal not in core_models.UserMeta.DailyWordGoal.values:
        return Response(
            {"error": f"Invalid word goal. Allowed values: {list(core_models.UserMeta.DailyWordGoal.values)}"},
            status=400,
        )

    meta, _ = core_models.UserMeta.objects.get_or_create(user=user)
    meta.daily_word_goal = data.word_goal
    meta.save()

    # Keep today's stats snapshot in sync with the new goal
    models.ReadingLog.objects.filter(user_id=user.id, date=date.today()).update(
        word_goal=data.word_goal
    )

    return Response({"message": "Word goal updated", "word_goal": data.word_goal}, status=200)


@api.get("/reading-log/today")
def reading_log_today(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    log = selectors.get_reading_log(user_id, date.today())
    word_count = log.word_count if log else 0
    word_goal = services.get_daily_word_goal(user_id)

    return Response(
        {"word_count": word_count, "word_goal": word_goal},
        status=200,
    )


@api.get("/languages")
def get_supported_languages(request):
    return Response({"languages": constants.SUPPORTED_LANGUAGES}, status=200)


@api.get("/supported-languages")
def supported_languages(request):
    languages = services.get_supported_languages()

    return Response({"languages": languages}, status=200)


@api.get("/dashboard/books")
def dashboard_books(request, language: str):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    response = {"continue_reading": [], "library": []}

    # Per-user reading progress keyed by book id, used to show read status on
    # library cards.
    progress_map = {
        progress["book_id"]: progress["sentence_last_read"]
        for progress in models.BookProgress.objects.filter(user_id=user_id).values(
            "book_id", "sentence_last_read"
        )
    }

    # Fetch user's own books
    for book in models.Book.objects.filter(uploaded_by_id=user_id, language=language).values(
        "id", "title", "title_en", "author", "sentence_count"
    ):
        response["library"].append(
            {"id": book["id"], "title": book["title"], "title_en": book["title_en"], "author": book["author"], "sentence_count": book["sentence_count"], "sentence_last_read": progress_map.get(book["id"], 0), "is_owner": True}
        )

    # Fetch public books from other users
    for book in (
        models.Book.objects.filter(is_public=True, language=language)
        .exclude(uploaded_by_id=user_id)
        .values("id", "title", "title_en", "author", "sentence_count")
    ):
        response["library"].append(
            {"id": book["id"], "title": book["title"], "title_en": book["title_en"], "author": book["author"], "sentence_count": book["sentence_count"], "sentence_last_read": progress_map.get(book["id"], 0), "is_owner": False}
        )

    # Display library books alphabetically regardless of read state, using the
    # title the card shows (title_en falls back to title).
    response["library"].sort(key=lambda book: (book["title_en"] or book["title"]).lower())

    # Fully read books stay in the library and must not show up as
    # continue reading.
    books_in_progress = models.BookProgress.objects.filter(
        user_id=user_id, book__language=language
    ).exclude(sentence_last_read__gte=F("book__sentence_count")).order_by("-updated_at").values(
        "book_id", "book__title", "book__title_en", "book__author", "sentence_last_read", "book__sentence_count", "book__uploaded_by_id"
    )

    for book_progress in books_in_progress:
        if book_progress["sentence_last_read"] > 0:
            response["continue_reading"].append(
                {
                    "id": book_progress["book_id"],
                    "title": book_progress["book__title"],
                    "title_en": book_progress["book__title_en"],
                    "author": book_progress["book__author"],
                    "sentence_last_read": book_progress["sentence_last_read"],
                    "sentence_count": book_progress["book__sentence_count"],
                    "is_owner": book_progress["book__uploaded_by_id"] == user_id,
                }
            )

    return Response(response, status=200)


@api.post("/read/")
def read(request, data: schema.BookSchema):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    access = services.verify_book_access_and_existence(data.book_id, user_id)
    if not access:
        return Response({"error": "Book not found"}, status=404)

    # Save book sentences to cache if not already loaded
    if cache.get(f"{user_id}:{data.book_id}") is None:
        all_sentences = services.cache_book_sentences(data.book_id, user_id)

    all_sentences = cache.get(f"{user_id}:{data.book_id}")

    progress = models.BookProgress.objects.filter(
        book_id=data.book_id, user_id=user_id
    ).first()
    sentence_last_read = progress.sentence_last_read if progress else 0
    sentence_furthest_read = progress.sentence_furthest_read if progress else 0

    if data.page_turn == "next":
        sentence_current = sentence_last_read + 1
    elif data.page_turn == "previous":
        # A fully read book stores sentence_last_read == sentence_count, one past
        # the last index; treat it as standing on the last sentence.
        sentence_current = max(0, min(sentence_last_read, len(all_sentences) - 1) - 1)
    else:
        sentence_current = sentence_last_read

    # Return only one sentence at a time
    if sentence_current >= len(all_sentences):
        sentence_current = len(all_sentences) - 1

    sentence = all_sentences[sentence_current]

    # Log words read only when the reader moves past the furthest sentence they
    # have read before. Re-reading earlier sentences (e.g. toggling next/previous
    # back and forth over the same two sentences) must not inflate the daily total.
    is_new_progress = sentence_current > sentence_furthest_read
    if is_new_progress:
        book_language = models.Book.objects.get(id=data.book_id).language
        words = services.extract_words(sentence)
        services.record_words_read(user_id, words, book_language)
        services.update_reading_log(user_id, len(words))
        sentence_furthest_read = sentence_current

    # Reaching the last sentence marks the book as fully read: progress is saved
    # as sentence_count so completed books show 100% instead of stopping at 99%.
    sentence_progress = sentence_current
    if sentence_current == len(all_sentences) - 1:
        sentence_progress = len(all_sentences)
        sentence_furthest_read = max(sentence_furthest_read, sentence_progress)

    models.BookProgress.objects.update_or_create(
        book_id=data.book_id,
        user_id=user_id,
        defaults={
            "sentence_last_read": sentence_progress,
            "sentence_furthest_read": sentence_furthest_read,
        },
    )

    todays_log = selectors.get_reading_log(user_id, date.today())

    return Response(
        {
            "sentence": sentence,
            "sentence_count": len(all_sentences),
            "sentence_last_read": sentence_current,
            "sentence_first": sentence_current,
            "has_previous": sentence_current > 0,
            "words_read_today": todays_log.word_count if todays_log else 0,
            "word_goal_today": services.get_daily_word_goal(user_id),
        },
        status=200
    )


@api.post("/books/mark-unread")
def mark_unread(request, data: schema.MarkUnreadSchema):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    access = services.verify_book_access_and_existence(data.book_id, user_id)
    if not access:
        return Response({"error": "Book not found"}, status=404)

    deleted, _ = models.BookProgress.objects.filter(
        book_id=data.book_id, user_id=user_id
    ).delete()

    if deleted:
        return Response({"message": "Book marked as unread"}, status=200)

    return Response({"error": "Book not in library"}, status=404)


@api.post("/translate/")
def translate(request, data: schema.TranslationSchema):
    try:
        translated = services.translate(data.text, data.source, data.target, data.context)

        return Response({"translated": translated.text}, status=200)

    except deepl.DeepLException as error:
        return Response({"error": f"DeepL API error: {str(error)}"}, status=400)

    except Exception as error:
        return Response({"error": f"Translation error: {str(error)}"}, status=500)


@api.post("/books/upload-file")
def upload_book(request, data: Form[schema.BookUploadSchema], file: UploadedFile = File(...)):
    try:
        user = User.objects.get(id=request.session["user_id"])
    except (KeyError, User.DoesNotExist):
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

    random_suffix = secrets.token_hex(8)
    base_name = os.path.splitext(file.name)[0]
    file.name = f"{base_name}_{random_suffix}{ext}"

    is_public = data.is_public if user.is_superuser else False
    reading_ease_score = data.reading_ease_score if user.is_superuser else None

    book = models.Book(
        title=data.title,
        author=data.author,
        language=data.language,
        description=data.description,
        reading_ease_score=reading_ease_score,
        file=file,
        file_type=file_type,
        uploaded_by_id=user.id,
        is_public=is_public
    )
    book.save()

    # Save book sentences to cache and store sentence count on the book
    try:
        services.cache_book_sentences(book.id, user.id)
        services.update_sentence_count(book, cache.get(f"{user.id}:{book.id}"))
    except models.Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    return Response({"id": book.id, "message": "Book uploaded successfully"}, status=201)


@api.post("/books/upload-content")
def upload_book_content(request, data: schema.BookUploadContentSchema):
    try:
        user = User.objects.get(id=request.session["user_id"])
    except (KeyError, User.DoesNotExist):
        return Response({"error": "Authentication required"}, status=401)

    if data.language not in constants.SUPPORTED_LANGUAGES:
        return Response(
            {
                "error": f"Invalid language. Supported languages: {', '.join(constants.SUPPORTED_LANGUAGES)}"
            },
            status=400
        )

    if not data.content.strip():
        return Response({"error": "Content cannot be empty"}, status=400)

    is_public = data.is_public if user.is_superuser else False
    reading_ease_score = data.reading_ease_score if user.is_superuser else None

    random_suffix = secrets.token_hex(8)
    file_name = f"{data.title}_{random_suffix}.txt"
    content_file = ContentFile(data.content.encode("utf-8"), name=file_name)

    book = models.Book(
        title=data.title,
        author=data.author,
        language=data.language,
        description=data.description,
        reading_ease_score=reading_ease_score,
        file=content_file,
        file_type="txt",
        uploaded_by_id=user.id,
        is_public=is_public
    )
    book.save()

    # Save book sentences to cache and store sentence count on the book
    try:
        services.cache_book_sentences(book.id, user.id)
        services.update_sentence_count(book, cache.get(f"{user.id}:{book.id}"))
    except models.Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    return Response({"id": book.id, "message": "Book uploaded successfully"}, status=201)


@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    try:
        book = models.Book.objects.get(id=book_id)
    except models.Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    # Only the owner can delete their own book.
    if book.uploaded_by_id != user_id:
        return Response({"error": "Access denied"}, status=403)

    services.delete_book_by_id(book_id)

    return Response({"message": "Book deleted successfully"}, status=200)


@api.get("/books/{book_id}/download")
def download_book(request, book_id: int):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    # Only the uploader can download their own book.
    try:
        book = models.Book.objects.get(id=book_id, uploaded_by_id=user_id)
    except models.Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    return FileResponse(
        book.file.open("rb"),
        as_attachment=True,
        filename=f"{book.title}.{book.file_type}"
    )


@api.post("/feedback/")
def create_feedback(request, data: schema.FeedbackSchema):
    try:
        request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    allowed_types = {choice[0] for choice in models.Feedback._meta.get_field("type").choices}

    if data.type not in allowed_types:
        return Response({"error": "Invalid feedback type"}, status=400)

    if not data.body.strip():
        return Response({"error": "Feedback message is required"}, status=400)

    models.Feedback.objects.create(type=data.type, body=data.body.strip())

    return Response({"message": "Feedback submitted successfully"}, status=201)


@api.post("/tts/")
def tts(request, data: schema.TTSSchema):
    language_code = DEEPL_TO_GOOGLE.get(data.language.upper())

    if language_code is None:
        return Response({"error": f"TTS not supported for language: {data.language}"}, status=400)

    try:
        audio_content = services.text_to_speech(data.text, language_code, data.speed)
        return Response({"audio": audio_content}, status=200)
    except ValueError as error:
        return Response({"error": str(error)}, status=400)
    except requests.RequestException as error:
        return Response({"error": f"TTS error: {str(error)}"}, status=500)
