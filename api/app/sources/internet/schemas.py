# app/sources/internet/schemas.py

from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    description: str = ""
    domain: str = ""

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
