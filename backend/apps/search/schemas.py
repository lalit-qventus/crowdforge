from ninja import Schema


class SearchIn(Schema):
    query: str
    index: str | None = None
    limit: int = 20
    offset: int = 0


class SearchResultOut(Schema):
    id: str
    index: str
    title: str
    snippet: str
    score: float


class SearchResponseOut(Schema):
    hits: list[SearchResultOut]
    total: int
    query: str
