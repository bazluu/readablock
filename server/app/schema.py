import enum
from ninja import Schema


class LoginSchema(Schema):
    email: str
    password: str


class SignupSchema(Schema):
    email: str
    password: str


class BookSchema(Schema):
    book_id: int
    # character_limit: int
    sentence_last_read: int = 0
    sentences_per_page: int = 6
    page_turn: str | None = None  # "next" or "previous"


class BookUploadSchema(Schema):
    title: str
    author: str
    language: str
    is_public: bool = False


class TranslationSchema(Schema):
    text: str
    source: str
    target: str = "EN-GB"
    context: str | None = None


class TTSSchema(Schema):
    text: str
    language: str
    speed: float = 0.9


class FeedbackSchema(Schema):
    type: str
    body: str
