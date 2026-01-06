import math
import statistics
import sys
from re import S

from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

from .Helpers import split_array
from .Items import create_item, create_itempool, item_table, junk_weights
from .Locations import (
    get_location_names,
    get_location_table,
    get_locations_by_required_features_count,
    get_locations_by_required_features_count_for_language,
)
from .Options import APCodeOptions, LanguageChoice
from .Regions import create_regions
from .Rules import set_rules
from .Types import Language, LocData, VersionIdentifier


class ArchiwebaCode(WebWorld):
    theme = "partyTime"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide for setting up ArchipelaCode to be played in Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["ShackledMars261"],
        )
    ]


class ArchipelaCodeWorld(World):
    """ArchipelaCode is an implementation of LeetCode problems in Archipelago, tasking you with solving a random selection of (free) programming problems. However, you must unlock various "language features", including variable declaration, if statements, comparison operators, and more."""

    game = "ArchipelaCode"
    web = ArchiwebaCode()
    options_dataclass = APCodeOptions
    options: APCodeOptions
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()

    archipelacode_apworld_version: VersionIdentifier = VersionIdentifier(0, 0, 2)

    included_locations: list[LocData] = []
    included_languages: list[Language] = []
    precollected_items: list[Item] = []

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(junk_weights.keys()), weights=junk_weights.values(), k=1)[0]

    def create_regions(self):
        create_regions(self)

    def generate_early(self):
        # PLANNED:
        # if self.options.EnablePython:
        # self.included_languages.append(Language("Python3", ["python3"]))
        # if self.options.EnableJavascript:
        # self.included_languages.append(Language("Javascript", ["javascript"]))
        # if self.options.EnableTypescript:
        # self.included_languages.append(Language("Typescript", ["typescript"]))
        # if self.options.EnableGolang:
        # self.included_languages.append(Language("Golang", ["golang"]))

        if self.options.LanguageChoice == LanguageChoice.option_python:
            self.included_languages.append(Language("Python3", ["python3"]))
        elif self.options.LanguageChoice == LanguageChoice.option_javascript:
            self.included_languages.append(Language("Javascript", ["javascript"]))
        elif self.options.LanguageChoice == LanguageChoice.option_typescript:
            self.included_languages.append(Language("Typescript", ["typescript"]))
        elif self.options.LanguageChoice == LanguageChoice.option_golang:
            self.included_languages.append(Language("Golang", ["golang"]))

        self.create_starting_items()
        self.set_early_items()

        self.generate_included_locations_v2()

        # avg_features_required: int = statistics.mean(
        # len(locdata_obj.required_features["python3"]) for locdata_obj in self.included_locations
        # )
        #
        # while avg_features_required > 6.0:
        # self.generate_included_locations()
        # avg_features_required: int = statistics.mean(
        # len(locdata_obj.required_features["python3"]) for locdata_obj in self.included_locations
        # )
        # print(avg_features_required)

        for loc in self.included_locations:
            pass
            # print(loc.name)
            # print(loc.required_features)
            # print(
            # f"{loc.name}: {statistics.mean(len(required_features) for required_features in loc.required_features.values())}"
            # )

    def generate_included_locations_v2(self):
        self.included_locations = []
        selected_lang: Language = self.included_languages[0]  # NEEDS TO BE CHANGED FOR MULTI-LANG SUPPORT

        ZERO_REQUIRED_PERCENTAGE: float = 0.20  # should probably be hidden yaml option

        easy_locations: list[LocData] = []
        medium_locations: list[LocData] = []
        hard_locations: list[LocData] = []

        locations_by_feature_count: dict[str, list[LocData]] = {}

        location_title_slugs_by_feature_count = get_locations_by_required_features_count_for_language(
            selected_lang.langSlugs[0]
        )  # NEEDS TO BE CHANGED FOR MULTI-LANG SUPPORT

        for data in get_location_table().values():
            included_slugs: list[str] = []
            for lang_slug in data.lang_slugs:
                for lang in self.included_languages:
                    if lang_slug in lang.langSlugs:
                        included_slugs.append(lang_slug)
            if len(included_slugs) == 0:
                continue
            new_loc = LocData(
                data.id,
                data.name,
                data.title_slug,
                data.difficulty,
                included_slugs,
                data.required_features,
            )
            for required_feature_count, values in location_title_slugs_by_feature_count.items():
                if new_loc.title_slug in values["problems"]:
                    if required_feature_count not in locations_by_feature_count.keys():
                        locations_by_feature_count[required_feature_count] = []
                    locations_by_feature_count[required_feature_count].append(new_loc)
                    if not required_feature_count == "0":
                        match data.difficulty:
                            case "EASY":
                                easy_locations.append(new_loc)
                            case "MEDIUM":
                                medium_locations.append(new_loc)
                            case "HARD":
                                hard_locations.append(new_loc)
                    break

        locations_by_feature_count = dict(sorted(locations_by_feature_count.items(), key=lambda x: int(x[0])))

        # for key, values in locations_by_feature_count.items():
        # print(f"{key}: {len(values)}")

        max_amount_of_features: int = self.random.randint(14, 16)

        amount_of_each_group: int = math.floor(self.options.TotalProblemCount / max_amount_of_features)
        extra_locations_needed: int = self.options.TotalProblemCount % max_amount_of_features

        group_amounts: dict[str, int] = {}
        leftovers: int = 0
        for feature_amount, locations in locations_by_feature_count.items():
            if int(feature_amount) >= max_amount_of_features:
                continue
            if len(locations) < amount_of_each_group:
                group_amounts[feature_amount] = len(locations)
                leftovers += amount_of_each_group - len(locations)
            else:
                group_amounts[feature_amount] = amount_of_each_group

        leftovers += extra_locations_needed

        while leftovers > 0:
            for feature_amount, locations in locations_by_feature_count.items():
                if (
                    int(feature_amount) >= max_amount_of_features
                    or group_amounts[feature_amount] >= len(locations)
                    or leftovers == 0
                ):
                    continue
                group_amounts[feature_amount] += 1
                leftovers -= 1

        for feature_amount, locations in locations_by_feature_count.items():
            if int(feature_amount) >= max_amount_of_features:
                continue
            self.included_locations.extend(
                self.random.sample(
                    locations,
                    k=group_amounts[feature_amount],
                    # k=min(
                    # (
                    # amount_of_each_group + extra_locations_needed
                    # if int(feature_amount) == 0
                    # else amount_of_each_group
                    # ),
                    # (self.options.TotalProblemCount - len(self.included_locations)),
                    # ),
                )
            )

        # self.included_locations.extend(
        # self.random.sample(
        # locations_by_feature_count["0"],
        # k=max(
        # len(location_title_slugs_by_feature_count["0"]),
        # math.floor(ZERO_REQUIRED_PERCENTAGE * self.options.TotalProblemCount),
        # ),
        # )
        # )

        # self.included_locations.extend(
        # self.random.sample(
        # easy_locations, k=round(self.options.TotalProblemCount * 0.4 * (1.0 - ZERO_REQUIRED_PERCENTAGE))
        # )
        # )
        # self.included_locations.extend(
        # self.random.sample(
        # medium_locations, k=round(self.options.TotalProblemCount * 0.3 * (1.0 - ZERO_REQUIRED_PERCENTAGE))
        # )
        # )
        # self.included_locations.extend(
        # self.random.sample(
        # hard_locations, k=round(self.options.TotalProblemCount * 0.3 * (1.0 - ZERO_REQUIRED_PERCENTAGE))
        # )
        # )

        self.included_locations = self.lightly_shuffle(
            self.included_locations, 0.12
        )  # Makes it so you don't only get easy problems in the first few batches, while still giving you generally easier problems at the start

        # print("Regions:")
        # for index, loc_arrays in enumerate(split_array(self.included_locations, 5), 1):
        # print(f" - {index}:")
        # for index, l in enumerate(loc_arrays):
        # print(f"   - {l.name}: {len(l.required_features['python3'])} ({l.difficulty})")
        # print(f"Total amount of problems: {len(self.included_locations)}")
        # print(
        # f"Total amount of problems with zero required features: {len([loc for loc in self.included_locations if len(loc.required_features['python3']) == 0])}"
        # )

    def generate_included_locations(self):
        self.included_locations = []
        easy_locations: list[LocData] = []
        medium_locations: list[LocData] = []
        hard_locations: list[LocData] = []
        for data in get_location_table().values():
            included_slugs: list[str] = []
            for lang_slug in data.lang_slugs:
                for lang in self.included_languages:
                    if lang_slug in lang.langSlugs:
                        included_slugs.append(lang_slug)
            if len(included_slugs) == 0:
                continue
            new_loc = LocData(
                data.id,
                data.name,
                data.title_slug,
                data.difficulty,
                included_slugs,
                data.required_features,
            )
            match data.difficulty:
                case "EASY":
                    easy_locations.append(new_loc)
                case "MEDIUM":
                    medium_locations.append(new_loc)
                case "HARD":
                    hard_locations.append(new_loc)

        self.included_locations.extend(
            self.random.sample(easy_locations, k=round(self.options.TotalProblemCount * 0.4))
        )
        self.included_locations.extend(
            self.random.sample(medium_locations, k=round(self.options.TotalProblemCount * 0.3))
        )
        self.included_locations.extend(
            self.random.sample(hard_locations, k=round(self.options.TotalProblemCount * 0.3))
        )

        self.included_locations = self.lightly_shuffle(
            self.included_locations, 0.08
        )  # Makes it so you don't only get easy problems in the first few batches, while still giving you generally easier problems at the start

        for _ in range(
            3
        ):  # it's 4 AM and I'm too tired to figure out a better solution. I don't even know why it's happening. - ShackledMars261, 9/19/25 4:19 AM
            dupe_check: list[str] = []
            easys_to_add: int = 0
            mediums_to_add: int = 0
            hards_to_add: int = 0
            for index, loc in enumerate(self.included_locations):
                if loc.name not in dupe_check:
                    dupe_check.append(loc.name)
                    continue
                self.included_locations.pop(index)
                match loc.difficulty:
                    case "EASY":
                        easys_to_add += 1
                    case "MEDIUM":
                        mediums_to_add += 1
                    case "HARD":
                        hards_to_add += 1

            for _ in range(easys_to_add):
                self.included_locations.append(self.random.choice(easy_locations))
            for _ in range(mediums_to_add):
                self.included_locations.append(self.random.choice(medium_locations))
            for _ in range(hards_to_add):
                self.included_locations.append(self.random.choice(hard_locations))

        self.included_locations.sort(
            key=lambda loc: statistics.mean(
                len(required_features) for required_features in loc.required_features.values()
            )
        )

    def set_rules(self):
        set_rules(self)

    def fill_slot_data(self):
        loc_arrays = split_array(self.included_locations, 5)
        slot_data: dict[str, any] = {
            "items": {},
            "regions": {},
            "metadata": {"included_languages": {}},
        }
        for index, array in enumerate(loc_arrays):
            slot_data["regions"][str(index)] = {}
            for loc in array:
                slot_data["regions"][str(index)][loc.id] = {
                    "id": int(loc.id),
                    "title": loc.name,
                    "titleSlug": loc.title_slug,
                    "difficulty": loc.difficulty,
                }

        # print(slot_data["regions"])

        for item_name, item_id in self.item_name_to_id.items():
            slot_data["items"][item_id] = item_name

        slot_data["metadata"]["EndGoal"] = round(
            float(self.options.TotalProblemCount.value) * float(self.options.EndGoal.value) / 100.0
        )

        slot_data["metadata"]["minimum_extension_version"] = (
            f"{self.archipelacode_apworld_version.major}.{self.archipelacode_apworld_version.minor}.{self.archipelacode_apworld_version.patch}"
        )

        # slot_data["metadata"]["included_languages"]["python3"] = True if self.options.EnablePython else False
        # slot_data["metadata"]["included_languages"]["javascript"] = True if self.options.EnableJavascript else False

        slot_data["metadata"]["included_languages"]["python3"] = (
            True if (self.options.LanguageChoice == LanguageChoice.option_python) else False
        )
        slot_data["metadata"]["included_languages"]["javascript"] = (
            True if (self.options.LanguageChoice == LanguageChoice.option_javascript) else False
        )

        # print(f"Python {'Enabled' if (self.options.LanguageChoice == LanguageChoice.option_python) else 'Disabled'}")
        # print(
        # f"Javascript {'Enabled' if (self.options.LanguageChoice == LanguageChoice.option_javascript) else 'Disabled'}"
        # )

        return slot_data

    def lightly_shuffle(self, orig_list: list, orderliness: float = 0.2) -> list:
        return sorted(
            orig_list,
            key=lambda i: self.random.gauss(orig_list.index(i) * orderliness, 1),
        )

    def create_starting_items(self) -> None:
        """Get starting items used for the StartWithBasics option."""
        items: list[Item] = []
        for language in self.included_languages:
            match language.lang:
                case "Python3":
                    pass
                    # items.append(self.create_item("Progressive Problem Unlock"))
                    # items.append(self.create_item("Python 'if'"))
                    # items.append(self.create_item("Python 'else'"))
                    # items.append(self.create_item("Python 'for'"))
                    # items.append(self.create_item("Python 'while'"))
                    # items.append(self.create_item("Python '='"))
                    # items.append(self.create_item("Python Comparison Operators"))
                    # items.append(self.create_item("Python 'in'"))
                    # items.append(self.create_item("Python 'is'"))
                    # items.append(self.create_item("Python '+'"))
                    # items.append(self.create_item("Python '-'"))
                    # items.append(self.create_item("Python '*'"))
                    # items.append(self.create_item("Python '**'"))
                    # items.append(self.create_item("Python '/'"))
                    # items.append(self.create_item("Python '//'"))
                    # items.append(self.create_item("Python '%'"))
                    # items.append(self.create_item("Python 'and'"))
                    # items.append(self.create_item("Python 'not'"))

        for item in items:
            # print(f"Precollecting {item.name}")
            # print(item.classification)
            self.multiworld.push_precollected(item)
            self.precollected_items.append(item.code)

    def set_early_items(self) -> None:
        items: list[Item] = []
        for language in self.included_languages:
            match language.lang:
                case "Python3":
                    pass
                    # items.append(self.create_item("Progressive Problem Unlock"))
                    # items.append(self.create_item("Python 'or'"))
                    # items.append(self.create_item("Progressive Problem Unlock"))
                    # items.append(self.create_item("Progressive Problem Unlock"))
                    # items.append(self.create_item("Python '='"))
                    # items.append(self.create_item("Python Comparison Operators"))
                    # items.append(self.create_item("Python 'in'"))
                    # items.append(self.create_item("Python '-'"))
                    # items.append(self.create_item("Python '+'"))
                    # items.append(self.create_item("Python 'if'"))
                    # items.append(self.create_item("Python 'for'"))

        for item in items:
            # print(f"Setting Sphere 1: {item.name}")
            self.multiworld.early_items[self.player][item.name] = 1

        # print(self.multiworld.early_items[self.player])
