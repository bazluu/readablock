from django.core.cache import cache
from django.shortcuts import get_object_or_404

from ninja import NinjaAPI
from ninja.responses import Response
import deepl

from app import schema, services, models

api = NinjaAPI()


@api.post("/login/")
def login(request, data: schema.LoginSchema):
    try:
        user = models.User.objects.get(email=data.email)
    except models.User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    if user.check_password(data.password):
        request.session["user_id"] = user.id
        return Response({"message": "Login successful"}, status=200)

    else:
        return Response({"message": "Invalid password"}, status=401)


@api.post("/signup/")
def signup(request, data: schema.SignupSchema):
    if models.User.objects.filter(email=data.email).exists():
        return Response({"message": "Unable to create account"}, status=500)

    try:
        user = models.User(email=data.email)
        user.set_password(data.password)
        user.save()

    except Exception as error:
        print(error)
        return Response({"message": "Unable to create account"}, status=500)

    request.session["user_id"] = user.id

    return Response({"message": "Login successful"}, status=200)


@api.get("/dashboard/books")
def dashboard_books(request):
    # user_id = models.User.objects.get(id=request.session["user_id"]).id
    user_id = 1

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
    sentence_last_read = cache.get("sentence_last_read") or 0
    epub = services.convert_epub_to_str()
    epub_cleaned = services.remove_html(epub)

    # Pagination
    if data.page_turn == "next":
        sentence_first = sentence_last_read + 1
    elif data.page_turn == "previous":
        # Go back by 5 sentences (or adjust based on your needs)
        sentence_first = max(0, sentence_last_read - 9)  # -4 for current page, -5 for previous
    else:
        sentence_first = sentence_last_read if sentence_last_read > 0 else 0

    # TODO calculate this based on character limit
    sentence_last = sentence_first + 4

    sentences = services.convert_text_to_sentences(epub_cleaned, sentence_first, sentence_last)
    cache.set("sentence_last_read", sentence_last, 300)

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
