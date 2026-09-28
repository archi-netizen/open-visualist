"""Shared request/response models for the OpenVisualist API."""
from pydantic import BaseModel


class EssayRequest(BaseModel):
    content: str


class ImageResult(BaseModel):
    url: str
    thumbnail: str
    title: str
    creator: str
    source: str
    license_code: str
    license_url: str
    requires_attribution: bool
    attribution: str
    foreign_landing_url: str
    matched_keyword: str
    confidence: int
