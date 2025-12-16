import os

from ebooklib import epub, ITEM_DOCUMENT
from ninja import NinjaAPI
from ninja.responses import Response


api = NinjaAPI()

@api.get("/hello/")
def hello(request):
    return {"message": "Hello, World!"}

@api.get("/read/")
def read(request):
    # Path to your local EPUB file (adjust as needed)
    epub_path = os.path.join(os.path.dirname(__file__), "../Gatto e topo in società.epub")

    # Read the EPUB file
    book = epub.read_epub(epub_path)
    text = []

    # Extract text from each document in the EPUB
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            text.append(item.get_content().decode("utf-8"))

    # Combine all text
    full_text = "\n".join(text)

    return Response({"text": full_text}, status=200)
