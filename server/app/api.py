from django.core.cache import cache

from ninja import NinjaAPI
from ninja.responses import Response

from app import schema, services


api = NinjaAPI()

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
            "has_previous": sentence_first > 0
        },
        status=200
    )
