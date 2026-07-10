import pkgutil
from typing import Any, TypeVar

from pydantic import BaseModel, Field
from pydantic_extra_types.semantic_version import SemanticVersion

T = TypeVar("T")


class ItemSummary(BaseModel):
    itemId: int = Field(-1)
    itemName: str = Field("")
    itemClassification: int = Field(1)


class EventSummary(BaseModel):
    eventId: int = Field(-1)
    eventLocationName: str = Field("")
    eventItemName: str = Field("")


class LocationSummary(BaseModel):
    locationId: int = Field(-1)
    locationName: str = Field("")


class TransitionSummary(BaseModel):
    transitionId: int = Field(-1)
    transitionName: str = Field("")
    linkedRoomId: int = Field(-1)
    linkedRoomName: str = Field("")


class RuleNode(BaseModel):
    """
    Mirrors Archipelago's rule_builder `to_dict()` / `from_dict()` schema
    (docs/rule builder.md, "Serialization"), so it can be handed directly to
    `world.rule_from_dict(...)`. Leaf nodes (`Has`) carry `args`; `And`/`Or`
    nodes carry `children` instead.
    """

    rule: str = Field("")
    options: list[Any] = Field([])
    args: dict[str, Any] | None = Field(None)
    children: list["RuleNode"] | None = Field(None)


RuleNode.model_rebuild()


class PreWorldDataTransition(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    fromId: int = Field(-1)
    fromName: str = Field("")
    toId: int = Field(-1)
    toName: str = Field("")
    requirements: RuleNode | None = Field(None)


class PreWorldDataRoom(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    transitions: list[TransitionSummary] = Field([])
    locations: list[LocationSummary] = Field([])
    events: list[EventSummary] = Field([])


class PreWorldDataLocation(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    roomId: int = Field(-1)
    roomName: str = Field("")
    vanillaItem: ItemSummary = Field(default_factory=ItemSummary)
    requirements: RuleNode | None = Field(None)


class PreWorldDataEvent(BaseModel):
    id: int = Field(-1)
    roomId: int = Field(-1)
    roomName: str = Field("")
    locationName: str = Field("")
    itemName: str = Field("")
    requirements: RuleNode | None = Field(None)


class PreWorldDataItem(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    classification: int = Field(1)
    saveEntry: str = Field("")
    count: int = Field(0)
    vanillaLocations: list[LocationSummary] = Field([])


class PreWorldData(BaseModel):
    version: SemanticVersion = Field("0.0.1")  # ty:ignore[invalid-assignment]
    rooms: list[PreWorldDataRoom] = Field([])
    transitions: list[PreWorldDataTransition] = Field([])
    locations: list[PreWorldDataLocation] = Field([])
    events: list[PreWorldDataEvent] = Field([])
    items: list[PreWorldDataItem] = Field([])


class WorldDataItem(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    classification: int = Field(1)
    saveEntry: str = Field("")
    count: int = Field(0)
    vanillaLocations: list["WorldDataLocation"] = Field([])


class WorldDataLocation(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    roomId: int = Field(-1)
    roomName: str = Field("")
    requirements: RuleNode | None = Field(None)
    vanillaItem: WorldDataItem = Field(default_factory=WorldDataItem)


class WorldDataEvent(BaseModel):
    id: int = Field(-1)
    roomId: int = Field(-1)
    roomName: str = Field("")
    locationName: str = Field("")
    itemName: str = Field("")
    requirements: RuleNode | None = Field(None)


class WorldDataTransition(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    fromId: int = Field(-1)
    fromName: str = Field("")
    toId: int = Field(-1)
    toName: str = Field("")
    requirements: RuleNode | None = Field(None)


class WorldDataRoom(BaseModel):
    id: int = Field(-1)
    name: str = Field("")
    transitions: list[WorldDataTransition] = Field([])
    locations: list[WorldDataLocation] = Field([])
    events: list[WorldDataEvent] = Field([])


WorldDataItem.model_rebuild()


class WorldData(BaseModel):
    version: SemanticVersion = Field("0.0.1")  # ty:ignore[invalid-assignment]
    rooms: list[WorldDataRoom] = Field([])
    transitions: list[WorldDataTransition] = Field([])
    locations: list[WorldDataLocation] = Field([])
    events: list[WorldDataEvent] = Field([])
    items: list[WorldDataItem] = Field([])


class DataProvider:
    def __init__(self) -> None:
        self.raw_data: PreWorldData = self.load_json()

        self.data: WorldData = WorldData()
        self.process_data()

    def load_json(self, filename: str = "world.json") -> PreWorldData:
        fname: str = "/".join(["data", filename])
        data: bytes = pkgutil.get_data(__name__, fname) or b"{}"
        return PreWorldData.model_validate_json(data.decode())

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
