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
    sentence_last_read: int = 0
    page_turn: str | None = None  # "next" or "previous"


class BookUploadSchema(Schema):
    title: str
    author: str
    language: str
    is_public: bool = False
    description: str | None = None
    reading_ease_score: float | None = None


class TranslationSchema(Schema):
    text: str
    source: str
    target: str = "EN-GB"
    context: str | None = None


class TTSSchema(Schema):
    text: str
    language: str
    speed: float = 0.9


class BookUploadContentSchema(Schema):
    title: str
    author: str
    language: str
    content: str
    is_public: bool = False
    description: str | None = None
    reading_ease_score: float | None = None


class FeedbackSchema(Schema):
    type: str
    body: str
