from dataclasses import dataclass
from typing import NamedTuple

from BaseClasses import Item, ItemClassification, Location


class ItemData(NamedTuple):
    code: int | None
    classification: ItemClassification
    language: str = ""


class LocData(NamedTuple):
    id: int = 0
    name: str = "New Location"
    title_slug: str = "new-location"
    difficulty: str = "EASY"
    lang_slugs: list[str] = []  # List of langSlugs
    required_features: dict[
        str, list[int]
    ] = {}  # {langSlug: [<Required lang feature 1 item id>, <Required lang feature 2 item id>]}


class ArchipelaCodeItem(Item):
    game = "ArchipelaCode"


class ArchipelaCodeLocation(Location):
    game = "ArchipelaCode"


@dataclass
class Language:
    lang: str
    langSlugs: list[str]


@dataclass
class VersionIdentifier:
    major: int
    minor: int
    patch: int
