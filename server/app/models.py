from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Book(models.Model):
    """
    Model for books with access control.
    Books can be either public (accessible to all) or private (only accessible to the uploader).
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    file = models.FileField(upload_to="books/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Access control
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_books"
    )
    is_public = models.BooleanField(default=False)


class BookProgress(models.Model):
    """
    Model for book progress tracking.
    The very existence of a row in this table means that the user has this book in their library.
    """
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence_last_read = models.IntegerField(default=0)
