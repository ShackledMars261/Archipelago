from BaseClasses import CollectionState, Location

from .bases import MIOTestBase


class TestBasicLogic(MIOTestBase):
    options = {  # noqa: RUF012
        "logic_difficulty": 0,
        "boss_kill_checks": False,
    }

    def test_basic_access(self) -> None:
        with self.subTest("Test starting checks accessible with nothing"):
            slash_loc: Location = self.world.get_location("ST_security_fall_P1: Starting Item (Slash)")
            self_awareness_loc: Location = self.world.get_location(
                "ST_security_fall_P1: Starting Item (Self-Awareness)"
            )

            self.assertTrue(slash_loc.can_reach(self.multiworld.state))
            self.assertTrue(self_awareness_loc.can_reach(self.multiworld.state))

    def test_item_and_location_ids_are_never_reserved(self) -> None:
        # Archipelago reserves ids <= 0 for its own use (docs/world api.md,
        # "IDs <= 0 are global and reserved"). A real item/location with id 0
        # would be falsy, and code that checks `if item.code`/`if location.address`
        # instead of `is not None` would silently misclassify it as an event.
        for item in self.multiworld.itempool:
            with self.subTest(item=item.name):
                self.assertTrue(item.code is None or item.code > 0)

        for location in self.multiworld.get_locations(self.player):
            with self.subTest(location=location.name):
                self.assertTrue(location.address is None or location.address > 0)

    def _state_with_all_but(self, excluded_item_name: str | None) -> CollectionState:
        # Collect from the raw itempool (not `get_items()`/`collect_all_but`,
        # which also force-includes already-placed event items, bypassing
        # whether their own prerequisites were actually collected) and let a
        # single sweep discover which locked events become reachable - this
        # matches how a real player would actually progress.
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name != excluded_item_name:
                state.collect(item, prevent_sweep=True)
        state.sweep_for_advancements()
        return state

    def test_goal_beatability(self) -> None:
        with self.subTest("beatable with everything"):
            state = self._state_with_all_but(None)
            self.assertTrue(self.multiworld.can_beat_game(state))

        with self.subTest("not beatable missing a required Voice"):
            # Ati Defeated requires all 4 non-Noden voices to be turned in;
            # missing any one of them should make the goal unreachable.
            state = self._state_with_all_but("Liho's Voice")
            self.assertFalse(self.multiworld.can_beat_game(state))
