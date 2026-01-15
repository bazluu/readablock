from ninja import Schema
from typing import Optional


class LoginSchema(Schema):
    email: str
    password: str


class SignupSchema(Schema):
    email: str
    password: str


class BookSchema(Schema):
    #book_id: int
    #character_limit: int
    #sentence_last_read: int = 0
    sentences_per_page: int
    page_turn: str | None = None # "next" | "previous"


class TranslationSchema(Schema):
    text: str
    source: str = "IT"
    target: str = "EN-GB"
    context: str | None = None
