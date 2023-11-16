from typing import List

from ninja import Schema, Field


class CategoryIn(Schema):
    name: str | None
    parent: int | None


class ChildCategory(Schema):
    id: int
    name: str
    parent: int = Field(0, alias="parent_id")
    iconUrl: str = Field(None, alias="icon_url")


class CategoryOut(Schema):
    id: int
    name: str
    iconUrl: str = Field(None, alias="icon_url")
    childs: List[ChildCategory] = Field(None, alias="children")
