import enum
from ninja import Schema


class LoginSchema(Schema):
    email: str
    password: str


class SignupSchema(Schema):
    email: str
    password: str


class PageTurn(enum.Enum):
    NEXT = "next"
    PREVIOUS = "previous"


class BookSchema(Schema):
    book_id: int
    # character_limit: int
    sentence_last_read: int = 0
    sentences_per_page: int
    page_turn: PageTurn | None = None


class BookUploadSchema(Schema):
    title: str
    author: str


class TranslationSchema(Schema):
    text: str
    source: str = "IT"
    target: str = "EN-GB"
    context: str | None = None
