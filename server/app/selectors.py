from app import models


def get_sentence_last_read(user_id: int, book_id: int) -> int | None:
    try:
        return models.BookProgress.objects.get(user_id=user_id, book_id=book_id).sentence_last_read
    except models.BookProgress.DoesNotExist:
        return None
