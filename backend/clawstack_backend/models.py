from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LinkItem(BaseModel):
    label: str
    href: str


class OfferItem(BaseModel):
    slug: str
    title: str
    price_label: str
    summary: str
    cta_label: str
    cta_href: str
    kind: Literal["open-source", "service", "managed"]


class SiteConfigResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_name: str
    tagline: str
    public_site_url: str
    public_api_base: str
    public_api_url: str
    canonical_url: str
    og_image_url: str
    repo_url: str
    contact_email: str | None
    docs: list[LinkItem]
    offers: list[OfferItem]


class HealthResponse(BaseModel):
    status: Literal["ok"]
    environment: str
    timestamp_utc: datetime


class IntakeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_tier: Literal["pro-setup", "managed", "custom"] = Field(
        description="Requested service tier."
    )
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    company: str | None = Field(default=None, max_length=120)
    source: str | None = Field(default=None, max_length=1024)
    website: str | None = Field(default=None, max_length=120)
    message: str = Field(min_length=10, max_length=4000)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("email must look like a real address")
        return value


class IntakeResponse(BaseModel):
    status: Literal["accepted"]
    lead_id: str
    delivery_channels: list[str] = Field(default_factory=list)


class LeadRecord(BaseModel):
    lead_id: str
    created_at_utc: datetime
    service_tier: Literal["pro-setup", "managed", "custom"]
    name: str
    email: str
    company: str | None = None
    source: str | None = None
    website: str | None = None
    message: str
    client_id: str | None = None


class LeadListResponse(BaseModel):
    leads: list[LeadRecord]
