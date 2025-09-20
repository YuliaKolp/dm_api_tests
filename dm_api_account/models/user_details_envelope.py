from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class ParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class Info(BaseModel):
    value: str
    parseMode: ParseMode


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSICPALE = "ClassicPale"
    NIGHT = "Night"


class Pading(BaseModel):
    commentsPerPage: int
    entitiesPerPage: int
    messagesPerPage: int
    postsPerPage: int
    topicsPerPage: int


class UserSettings(BaseModel):
    colorSchema: ColorSchema
    paging: Pading


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    mediumPictureUrl: str = Field(None, alias="mediumPictureUrl")
    smallPictureUrl: str = Field(None, alias="smallPictureUrl")
    status: str = Field(None, alias="status")
    rating: Rating
    online: datetime = Field(None, alias="online")
    name: str = Field(None, alias="name")
    location: str = Field(None, alias="location")
    registration: datetime = Field(None, alias="registration")
    icq: str = Field(None)
    skype: str = Field(None)
    originalPictureUrl: str = Field(None)
    #info: Info = Field(None) # It seems there is an error in Swagger
    info: str = Field(None)
    settings: UserSettings = Field(None)



class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
