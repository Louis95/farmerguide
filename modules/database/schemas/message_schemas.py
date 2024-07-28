"""Schemas for the message objects, used as responses."""
# pylint: disable=too-few-public-methods

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Message schema for the response types."""

    detail: str = Field(
        ...,
        example="String type - this will contain more details about the problem encountered",
        description="Details about the problem encountered",
    )
