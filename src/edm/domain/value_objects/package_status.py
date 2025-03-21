import enum


class PackageStatus(enum.StrEnum):
    DRAFT = "draft"
    CREATED = "created"
    QUEUED = "queued"
    SENT = "sent"
    SIGNED = "signed"
    SIGNED_DOWNLOADED = "downloaded_signed"
