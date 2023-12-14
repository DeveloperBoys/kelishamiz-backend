from enum import Enum
from typing import List
from datetime import datetime

from ninja import Schema, Field

from apps.classifieds.models import (
    PENDING,
    REJECTED,
    APPROVED,
    DELETED
)


class ClassifiedStatus(str, Enum):
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
    image_url: str = Field(None, alias="imageUrl")


class ClassifiedDetailBase(Schema):
    id: int | None


class ClassifiedDetailOut(ClassifiedDetailBase):
    currency_type: CurrencyType = Field(alias="currencyType")
    price: float
    is_negotiable: bool = Field(default=False, alias="isNegotiable")
    description: str
    location: str
    dynamic_fields: List[DynamicFieldOut] = Field(
        None, alias="dynamicFields")


class ClassifiedBase(Schema):
    id: int = None


class CreateClassified(Schema):
    category: int = Field(default=None)
    title: str
    dynamic_fields: List[DynamicFieldBase] = Field(
        None, alias="dynamicFields")
    currency_type: CurrencyType = Field(alias="currencyType")
    is_negotiable: bool = Field(default=False, alias="isNegotiable")
    price: float
    description: str
    location: int


class ReturnCreatedClassified(ClassifiedBase):
    category: int = Field(None, alias="categoryId")
    title: str | None


class ClassifiedOut(ClassifiedBase):
    category: int = Field(None, alias="categoryId")
    title: str | None
    is_liked: bool = Field(default=False, alias="isLiked")
    detail: ClassifiedDetailOut = None
    created_at: datetime = Field(alias="createdAt")
    images: List[ClassifiedImageOut] = None
