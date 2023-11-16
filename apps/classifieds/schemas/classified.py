from enum import Enum
from typing import List
from datetime import datetime

from ninja import Schema, Field

from ..models import (
    DRAFT,
    PENDING,
    REJECTED,
    APPROVED,
    DELETED
)


class ClassifiedStatus(str, Enum):
    DRAFT = DRAFT
    PENDING = PENDING
    APPROVED = APPROVED
    REJECTED = REJECTED
    DELETED = DELETED


class CurrencyType(str, Enum):
    USD = "usd"
    UZS = "uzs"


class DynamicFieldBase(Schema):
    key: str
    value: str


class DynamicFieldOut(DynamicFieldBase):
    id: int


class ClassifiedImageBase(Schema):
    classified: int


class ClassifiedImageOut(Schema):
    id: int | None
    image_url: str = Field(None, alias="image_url")


class ClassifiedDetailBase(Schema):
    id: int | None


class CreateClassifiedDetail(ClassifiedDetailBase):
    currency_type: CurrencyType
    price: float
    is_negotiable: bool = False
    description: str


class ClassifiedDetailOut(ClassifiedDetailBase):
    currency_type: CurrencyType
    price: float
    is_negotiable: bool = False
    description: str
    dynamic_fields: List[DynamicFieldOut] = Field(
        None, alias="dynamicfield_set")


class ClassifiedBase(Schema):
    id: int = None


class CreateClassified(Schema):
    category: int | None
    title: str | None


class ReturnCreatedClassified(ClassifiedBase):
    category: int = Field(None, alias="category_id")
    title: str | None


class ClassifiedOut(ClassifiedBase):
    category: int = Field(None, alias="category_id")
    title: str | None
    is_liked: bool = False
    detail: ClassifiedDetailOut = None
    created_at: datetime
    images: List[ClassifiedImageOut] = Field(
        None, alias="classifiedimage_set")
