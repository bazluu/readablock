from ninja import Schema


class BookSchema(Schema):
    #book_id: int
    #character_limit: int
    sentence_first: int = 0
    sentence_last: int
