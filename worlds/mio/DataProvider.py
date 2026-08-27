import json
import pkgutil
import re
from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")

# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
_SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def _validate_semver(version: str) -> str:
    if not _SEMVER_RE.match(version):
        raise ValueError(f"'{version}' is not a valid semantic version")
    return version


@dataclass
class ItemSummary:
    itemId: int = -1
    itemName: str = ""
    itemClassification: int = 1

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ItemSummary":
        return cls(
            itemId=d.get("itemId", -1),
            itemName=d.get("itemName", ""),
            itemClassification=d.get("itemClassification", 1),
        )


@dataclass
class EventSummary:
    eventId: int = -1
    eventLocationName: str = ""
    eventItemName: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "EventSummary":
        return cls(
            eventId=d.get("eventId", -1),
            eventLocationName=d.get("eventLocationName", ""),
            eventItemName=d.get("eventItemName", ""),
        )


@dataclass
class LocationSummary:
    locationId: int = -1
    locationName: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "LocationSummary":
        return cls(
            locationId=d.get("locationId", -1),
            locationName=d.get("locationName", ""),
        )


@dataclass
class TransitionSummary:
    transitionId: int = -1
    transitionName: str = ""
    linkedRoomId: int = -1
    linkedRoomName: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TransitionSummary":
        return cls(
            transitionId=d.get("transitionId", -1),
            transitionName=d.get("transitionName", ""),
            linkedRoomId=d.get("linkedRoomId", -1),
            linkedRoomName=d.get("linkedRoomName", ""),
        )


@dataclass
class RuleNode:
    """
    Mirrors Archipelago's rule_builder `to_dict()` / `from_dict()` schema
    (docs/rule builder.md, "Serialization"), so it can be handed directly to
    `world.rule_from_dict(...)`. Leaf nodes (`Has`) carry `args`; `And`/`Or`
    nodes carry `children` instead.
    """

    rule: str = ""
    options: list[Any] = field(default_factory=list)
    args: dict[str, Any] | None = None
    children: list["RuleNode"] | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "RuleNode | None":
        if d is None:
            return None
        children_data = d.get("children")
        return cls(
            rule=d.get("rule", ""),
            options=d.get("options", []),
            args=d.get("args"),
            children=[cls.from_dict(c) for c in children_data] if children_data is not None else None,
        )


@dataclass
class PreWorldDataTransition:
    id: int = -1
    name: str = ""
    fromId: int = -1
    fromName: str = ""
    toId: int = -1
    toName: str = ""
    requirements: RuleNode | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldDataTransition":
        return cls(
            id=d.get("id", -1),
            name=d.get("name", ""),
            fromId=d.get("fromId", -1),
            fromName=d.get("fromName", ""),
            toId=d.get("toId", -1),
            toName=d.get("toName", ""),
            requirements=RuleNode.from_dict(d.get("requirements")),
        )


@dataclass
class PreWorldDataRoom:
    id: int = -1
    name: str = ""
    transitions: list[TransitionSummary] = field(default_factory=list)
    locations: list[LocationSummary] = field(default_factory=list)
    events: list[EventSummary] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldDataRoom":
        return cls(
            id=d.get("id", -1),
            name=d.get("name", ""),
            transitions=[TransitionSummary.from_dict(t) for t in d.get("transitions", [])],
            locations=[LocationSummary.from_dict(l) for l in d.get("locations", [])],
            events=[EventSummary.from_dict(e) for e in d.get("events", [])],
        )


@dataclass
class PreWorldDataLocation:
    id: int = -1
    name: str = ""
    roomId: int = -1
    roomName: str = ""
    vanillaItem: ItemSummary = field(default_factory=ItemSummary)
    requirements: RuleNode | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldDataLocation":
        return cls(
            id=d.get("id", -1),
            name=d.get("name", ""),
            roomId=d.get("roomId", -1),
            roomName=d.get("roomName", ""),
            vanillaItem=ItemSummary.from_dict(d.get("vanillaItem", {})),
            requirements=RuleNode.from_dict(d.get("requirements")),
        )


@dataclass
class PreWorldDataEvent:
    id: int = -1
    roomId: int = -1
    roomName: str = ""
    locationName: str = ""
    itemName: str = ""
    requirements: RuleNode | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldDataEvent":
        return cls(
            id=d.get("id", -1),
            roomId=d.get("roomId", -1),
            roomName=d.get("roomName", ""),
            locationName=d.get("locationName", ""),
            itemName=d.get("itemName", ""),
            requirements=RuleNode.from_dict(d.get("requirements")),
        )


@dataclass
class PreWorldDataItem:
    id: int = -1
    name: str = ""
    classification: int = 1
    saveEntry: str = ""
    count: int = 0
    vanillaLocations: list[LocationSummary] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldDataItem":
        return cls(
            id=d.get("id", -1),
            name=d.get("name", ""),
            classification=d.get("classification", 1),
            saveEntry=d.get("saveEntry", ""),
            count=d.get("count", 0),
            vanillaLocations=[LocationSummary.from_dict(l) for l in d.get("vanillaLocations", [])],
        )


@dataclass
class PreWorldData:
    version: str = "0.0.1"
    rooms: list[PreWorldDataRoom] = field(default_factory=list)
    transitions: list[PreWorldDataTransition] = field(default_factory=list)
    locations: list[PreWorldDataLocation] = field(default_factory=list)
    events: list[PreWorldDataEvent] = field(default_factory=list)
    items: list[PreWorldDataItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PreWorldData":
        return cls(
            version=_validate_semver(d.get("version", "0.0.1")),
            rooms=[PreWorldDataRoom.from_dict(r) for r in d.get("rooms", [])],
            transitions=[PreWorldDataTransition.from_dict(t) for t in d.get("transitions", [])],
            locations=[PreWorldDataLocation.from_dict(l) for l in d.get("locations", [])],
            events=[PreWorldDataEvent.from_dict(e) for e in d.get("events", [])],
            items=[PreWorldDataItem.from_dict(i) for i in d.get("items", [])],
        )


@dataclass
class WorldDataItem:
    id: int = -1
    name: str = ""
    classification: int = 1
    saveEntry: str = ""
    count: int = 0
    vanillaLocations: list["WorldDataLocation"] = field(default_factory=list)


@dataclass
class WorldDataLocation:
    id: int = -1
    name: str = ""
    roomId: int = -1
    roomName: str = ""
    requirements: RuleNode | None = None
    vanillaItem: WorldDataItem = field(default_factory=WorldDataItem)


@dataclass
class WorldDataEvent:
    id: int = -1
    roomId: int = -1
    roomName: str = ""
    locationName: str = ""
    itemName: str = ""
    requirements: RuleNode | None = None


@dataclass
class WorldDataTransition:
    id: int = -1
    name: str = ""
    fromId: int = -1
    fromName: str = ""
    toId: int = -1
    toName: str = ""
    requirements: RuleNode | None = None


@dataclass
class WorldDataRoom:
    id: int = -1
    name: str = ""
    transitions: list[WorldDataTransition] = field(default_factory=list)
    locations: list[WorldDataLocation] = field(default_factory=list)
    events: list[WorldDataEvent] = field(default_factory=list)


@dataclass
class WorldData:
    version: str = "0.0.1"
    rooms: list[WorldDataRoom] = field(default_factory=list)
    transitions: list[WorldDataTransition] = field(default_factory=list)
    locations: list[WorldDataLocation] = field(default_factory=list)
    events: list[WorldDataEvent] = field(default_factory=list)
    items: list[WorldDataItem] = field(default_factory=list)


class DataProvider:
    def __init__(self) -> None:
        self.raw_data: PreWorldData = self.load_json()

        self.data: WorldData = WorldData()
        self.process_data()

    def load_json(self, filename: str = "world.json") -> PreWorldData:
        fname: str = "/".join(["data", filename])
        data: bytes = pkgutil.get_data(__name__, fname) or b"{}"
        return PreWorldData.from_dict(json.loads(data.decode()))

    def process_data(self) -> None:
        # ── Pass 1: create all objects (no links yet) ──────────────────────────

        rooms: dict[int, WorldDataRoom] = {r.id: WorldDataRoom(id=r.id, name=r.name) for r in self.raw_data.rooms}
        items: dict[int, WorldDataItem] = {
            i.id: WorldDataItem(
                id=i.id,
                name=i.name,
                classification=i.classification,
                saveEntry=i.saveEntry,
                count=i.count,
            )
            for i in self.raw_data.items
        }
        events: dict[int, WorldDataEvent] = {
            e.id: WorldDataEvent(
                id=e.id,
                roomId=e.roomId,
                roomName=e.roomName,
                locationName=e.locationName,
                itemName=e.itemName,
                requirements=e.requirements,
            )
            for e in self.raw_data.events
        }
        locations: dict[int, WorldDataLocation] = {
            l.id: WorldDataLocation(
                id=l.id,
                name=l.name,
                roomId=l.roomId,
                roomName=l.roomName,
                requirements=l.requirements,
            )
            for l in self.raw_data.locations
        }
        transitions: dict[int, WorldDataTransition] = {
            t.id: WorldDataTransition(
                id=t.id,
                name=t.name,
                fromId=t.fromId,
                fromName=t.fromName,
                toId=t.toId,
                toName=t.toName,
                requirements=t.requirements,
            )
            for t in self.raw_data.transitions
        }

        # ── Helpers ────────────────────────────────────────────────────────────

        def resolve(lookup: dict[int, T], id: int, context: str) -> T | None:
            if id not in lookup:
                print(f"[DataProvider] Warning: could not resolve {context} with id {id}")
                return None
            return lookup[id]

        # ── Pass 2: link everything together ───────────────────────────────────

        # Items: link vanilla locations
        for pre_item in self.raw_data.items:
            item = items[pre_item.id]
            for loc_summary in pre_item.vanillaLocations:
                location = resolve(locations, loc_summary.locationId, "vanilla location for item")
                if location is not None:
                    item.vanillaLocations.append(location)

        # Locations: link vanilla item
        for pre_loc in self.raw_data.locations:
            location = locations[pre_loc.id]
            vanilla_item = resolve(items, pre_loc.vanillaItem.itemId, "vanilla item for location")
            if vanilla_item is not None:
                location.vanillaItem = vanilla_item

        # Rooms: link transitions, locations, events
        for pre_room in self.raw_data.rooms:
            room = rooms[pre_room.id]
            for trans_summary in pre_room.transitions:
                transition = resolve(transitions, trans_summary.transitionId, "transition for room")
                if transition is not None:
                    room.transitions.append(transition)
            for loc_summary in pre_room.locations:
                location = resolve(locations, loc_summary.locationId, "location for room")
                if location is not None:
                    room.locations.append(location)
            for event_summary in pre_room.events:
                event = resolve(events, event_summary.eventId, "event for room")
                if event is not None:
                    room.events.append(event)

        # ── Populate self.data ─────────────────────────────────────────────────

        self.data.rooms = list(rooms.values())
        self.data.transitions = list(transitions.values())
        self.data.locations = list(locations.values())
        self.data.events = list(events.values())
        self.data.items = list(items.values())
