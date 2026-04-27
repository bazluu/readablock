from app import models


def get_sentence_last_read(user_id: int, book_id: int) -> int:
    sentence_last_read = models.BookProgress.objects.get(
        user_id=user_id, book_id=book_id
    ).sentence_last_read

    return sentence_last_read
