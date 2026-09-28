from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

from app import constants

extensions_allowed = FileExtensionValidator(allowed_extensions=["epub", "pdf", "txt", "kepub"])


class Book(models.Model):
    """
    Model for books with access control.
    Books can be either public (accessible to all) or private (only accessible to the uploader).
    """

    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=100, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    language = models.CharField(
        max_length=7, choices=[(lang, lang) for lang in constants.SUPPORTED_LANGUAGES]
    )
    sentence_count = models.IntegerField(default=0)
    description = models.TextField(null=True)
    reading_ease_score = models.FloatField(null=True)
    tags = models.JSONField(default=list, blank=True)

    file = models.FileField(upload_to="books/")
    BOOK_FILE_TYPES = (("epub", "epub"), ("pdf", "pdf"), ("txt", "txt"), ("kepub", "kepub"))
    file_type = models.CharField(choices=BOOK_FILE_TYPES, max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Access control
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_books")
    is_public = models.BooleanField(default=False)


class BookProgress(models.Model):
    """
    Model for book progress tracking.
    The very existence of a row in this table means that the user has this book in their library.
    """

    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence_last_read = models.IntegerField(default=0)


class Word(models.Model):
    """
    Shared vocabulary table, deduped across all users and books.
    """

    text = models.CharField(max_length=255)
    language = models.CharField(
        max_length=7, choices=[(lang, lang) for lang in constants.SUPPORTED_LANGUAGES]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["text", "language"], name="uniq_word_language")
        ]
        indexes = [models.Index(fields=["text"])]


class ReadingLog(models.Model):
    """
    Materialized counter of how many words a user read on a given day.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_log")
    date = models.DateField()
    word_count = models.PositiveSmallIntegerField(default=0)
    word_goal = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="uniq_user_date")
        ]


class WordRead(models.Model):
    """
    Which words a user read, on what day, and how many times.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="word_reads")
    word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name="reads")
    date = models.DateField()
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "word", "date"], name="uniq_user_word_date")
        ]
        indexes = [models.Index(fields=["user", "word"])]


class BookUpload(models.Model):
    """
    Model for book uploads.
    This model is used to track the status of book uploads and to store the uploaded file before it is processed.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/", validators=[extensions_allowed])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    error_message = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Feedback(models.Model):
    type = models.CharField(
        max_length=20, choices=[(t, t) for t in ("bug", "feature_request", "general")]
    )
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
