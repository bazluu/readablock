from ninja import NinjaAPI
from ninja.responses import Response

from app import schema, services


api = NinjaAPI()

@api.post("/read/")
def read(request, data: schema.BookSchema):
    sentence_first = data.sentence_first
    sentence_last = data.sentence_last

    epub = services.convert_epub_to_str()
    epub_cleaned = services.remove_html(epub)
 
    sentences = services.convert_text_to_sentences(epub_cleaned, sentence_first, sentence_last)

    return Response({"sentences": sentences}, status=200)
