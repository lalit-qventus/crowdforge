from ninja import Router

from .schemas import SearchResponseOut
from . import services

router = Router()


@router.get("/search", response=SearchResponseOut)
def search_all(request, query: str, limit: int = 20, offset: int = 0):
    return services.search(query, index=None, limit=limit, offset=offset)


@router.get("/search/{index}", response=SearchResponseOut)
def search_index(request, index: str, query: str, limit: int = 20, offset: int = 0):
    return services.search(query, index=index, limit=limit, offset=offset)
