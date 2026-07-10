import unittest
from collections.abc import Iterator

from worlds.mio.DataProvider import DataProvider, RuleNode


def _iter_leaf_references(node: RuleNode | None) -> Iterator[tuple[str, str]]:
    """
    Yields (kind, name) for every leaf in a rule tree: kind is "name" for a
    Has/HasFromListUnique leaf (an item or event name), or "region" for a
    CanReachRegion leaf (a room name).
    """
    if node is None:
        return
    if node.rule == "Has":
        assert node.args is not None
        yield "name", node.args["item_name"]
    elif node.rule == "HasFromListUnique":
        assert node.args is not None
        for name in node.args["item_names"]:
            yield "name", name
    elif node.rule == "CanReachRegion":
        assert node.args is not None
        yield "region", node.args["region_name"]
    elif node.children:
        for child in node.children:
            yield from _iter_leaf_references(child)


def _is_satisfiable_with_progression_only(node: RuleNode, item_classifications: dict[str, int]) -> bool:
    """
    Evaluates whether `node` can be satisfied using only progression-classified
    items, treating event references as always-available (each event's own
    rule tree is checked independently) and CanReachRegion as structural
    (the transitions leading to that region are checked independently too).
    """
    if node.rule == "Has":
        assert node.args is not None
        classification = item_classifications.get(node.args["item_name"])
        return classification is None or bool(classification & 0b0001)
    if node.rule == "HasFromListUnique":
        assert node.args is not None
        available_count = sum(
            1
            for name in node.args["item_names"]
            if name not in item_classifications or (item_classifications[name] & 0b0001)
        )
        return available_count >= node.args["count"]
    if node.rule in ("CanReachRegion", "True_"):
        return True
    if node.rule == "False_":
        return False
    if node.rule in ("And", "Or"):
        assert node.children is not None
        if node.rule == "And":
            return all(_is_satisfiable_with_progression_only(child, item_classifications) for child in node.children)
        return any(_is_satisfiable_with_progression_only(child, item_classifications) for child in node.children)
    raise ValueError(f"Unhandled rule type in test: {node.rule}")


class TestRuleReferences(unittest.TestCase):
    """
    Static checks against the DataProvider's raw rule trees. These don't
    need a constructed multiworld, so they run fast and catch data-entry
    mistakes (an unwired event, a non-progression item gating logic)
    directly against world.json.
    """

    data_provider: DataProvider

    @classmethod
    def setUpClass(cls) -> None:
        cls.data_provider = DataProvider()

    def _all_requirements(self) -> Iterator[tuple[str, RuleNode | None]]:
        for transition in self.data_provider.data.transitions:
            yield transition.name, transition.requirements
        for location in self.data_provider.data.locations:
            yield location.name, location.requirements
        for event in self.data_provider.data.events:
            yield event.itemName, event.requirements

    def test_all_referenced_names_exist(self) -> None:
        known_names = {item.name for item in self.data_provider.data.items} | {
            event.itemName for event in self.data_provider.data.events
        }
        known_rooms = {room.name for room in self.data_provider.data.rooms}

        for context, node in self._all_requirements():
            for kind, name in _iter_leaf_references(node):
                with self.subTest(context=context, name=name):
                    if kind == "region":
                        self.assertIn(name, known_rooms, f"'{context}' requires unknown room '{name}'")
                    else:
                        self.assertIn(name, known_names, f"'{context}' requires unknown item/event '{name}'")

    def test_all_rules_satisfiable_with_progression_items_only(self) -> None:
        # A rule can reference non-progression items as long as at least one
        # satisfying path through the tree (e.g. one branch of an Or) is
        # reachable using only progression-classified items - that's the
        # actual Archipelago invariant (progression items alone must be able
        # to complete the game), not "every referenced item is progression".
        item_classifications = {item.name: item.classification for item in self.data_provider.data.items}

        for context, node in self._all_requirements():
            if node is None or node.rule == "False_":
                continue  # a bare False_ is a deliberate "not reachable yet" marker, not a bug
            with self.subTest(context=context):
                self.assertTrue(
                    _is_satisfiable_with_progression_only(node, item_classifications),
                    f"'{context}' cannot be satisfied using only progression-classified items",
                )
