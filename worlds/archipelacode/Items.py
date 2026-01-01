from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .Options import LanguageChoice
from .Types import ArchipelaCodeItem, ItemData

if TYPE_CHECKING:
    from . import ArchipelaCodeWorld


def create_itempool(world: "ArchipelaCodeWorld") -> list[Item]:
    itempool: list[Item] = []

    for name in item_table.keys():
        data = item_table.get(name)

        if data is None:
            continue

        item_type: ItemClassification = item_table.get(name).classification

        if item_type is ItemClassification.filler or item_type is ItemClassification.trap:
            continue

        # if data.code in world.precollected_items:
        # continue

        # PLANNED:
        # if data.language == "py" and not world.options.EnablePython:
        # continue
        #
        # if data.language == "js" and not world.options.EnableJavascript:
        # continue
        #
        # if data.language == "ts" and not world.options.EnableTypescript:
        # continue
        #
        # if data.language == "go" and not world.options.EnableGolang:
        # continue

        if data.language == "py" and not (world.options.LanguageChoice == LanguageChoice.option_python):
            continue

        if data.language == "js" and not (world.options.LanguageChoice == LanguageChoice.option_javascript):
            continue

        if data.language == "ts" and not (world.options.LanguageChoice == LanguageChoice.option_typescript):
            continue

        if data.language == "go" and not (world.options.LanguageChoice == LanguageChoice.option_golang):
            continue

        amount_to_create: int = item_frequencies.get(name, 1) - world.precollected_items.count(name)

        itempool += create_multiple_items(world, name, amount_to_create, item_type)

    itempool += create_junk_items(world, len(world.included_locations) - len(itempool))
    return itempool


def create_item(world: "ArchipelaCodeWorld", name: str) -> Item:
    data = item_table[name]
    return ArchipelaCodeItem(name, data.classification, data.code, world.player)


def create_multiple_items(
    world: "ArchipelaCodeWorld",
    name: str,
    count: int = 1,
    item_type: ItemClassification = ItemClassification.progression,
) -> list[Item]:
    data = item_table[name]
    return [ArchipelaCodeItem(name, item_type, data.code, world.player) for _ in range(count)]


def create_junk_items(world: "ArchipelaCodeWorld", count: int) -> list[Item]:
    junk_pool: list[Item] = []
    junk_list: dict[str, int] = {}
    ic: ItemClassification

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

    for _ in range(count):
        junk_pool.append(
            world.create_item(world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0])
        )

    return junk_pool


def get_item_name_from_id(id: int) -> str:
    for item_name, item in item_table.items():
        if item.code == id:
            return item_name


junk_items = {  # 1000 range for junk items
    "Github Copilot": ItemData(6700901000, ItemClassification.filler, "junk"),
    "Claude Code": ItemData(6700901001, ItemClassification.filler, "junk"),
    "Cursor": ItemData(6700901002, ItemClassification.filler, "junk"),
    "Google Jules": ItemData(6700901003, ItemClassification.filler, "junk"),
    "Gemini Code Assist": ItemData(6700901004, ItemClassification.filler, "junk"),
    "ChatGPT": ItemData(6700901005, ItemClassification.filler, "junk"),
    "Aider": ItemData(6700901006, ItemClassification.filler, "junk"),
}

misc_items = {  # 2000 range for misc items
    # "Progressive Line Count": ItemData(6700902000, ItemClassification.progression, "misc"),  # UNIMPLEMENTED CURRENTLY
    # "Progressive Character Limit": ItemData(6700902001, ItemClassification.progression, "misc"),  # UNIMPLEMENTED CURRENTLY
    "Progressive Problem Unlock": ItemData(6700902002, ItemClassification.progression, "misc"),
}

python_items = {  # 3100 range for Python items
    "Python 'if'": ItemData(6700903100, ItemClassification.progression, "py"),
    "Python 'for'": ItemData(6700903101, ItemClassification.progression, "py"),
    "Python '='": ItemData(6700903102, ItemClassification.progression, "py"),
    "Python Comparison Operators": ItemData(6700903103, ItemClassification.progression, "py"),
    "Python 'while'": ItemData(6700903104, ItemClassification.progression, "py"),
    "Python 'else'": ItemData(6700903105, ItemClassification.progression, "py"),
    "Python 'elif'": ItemData(6700903106, ItemClassification.progression, "py"),
    "Python 'match'": ItemData(6700903107, ItemClassification.progression, "py"),
    "Python '+'": ItemData(6700903108, ItemClassification.progression, "py"),
    "Python '-'": ItemData(6700903109, ItemClassification.progression, "py"),
    "Python '*'": ItemData(6700903110, ItemClassification.progression, "py"),
    "Python '/'": ItemData(6700903111, ItemClassification.progression, "py"),
    "Python '**'": ItemData(6700903112, ItemClassification.progression, "py"),
    "Python '//'": ItemData(6700903113, ItemClassification.progression, "py"),
    "Python '%'": ItemData(6700903114, ItemClassification.progression, "py"),
    "Python 'and'": ItemData(6700903115, ItemClassification.progression, "py"),
    "Python 'or'": ItemData(6700903116, ItemClassification.progression, "py"),
    "Python 'not'": ItemData(6700903117, ItemClassification.progression, "py"),
    "Python 'is'": ItemData(6700903118, ItemClassification.progression, "py"),
    "Python 'in'": ItemData(6700903119, ItemClassification.progression, "py"),
}

javascript_items = {  # 3200 range for Javascript items
    "Javascript '='": ItemData(6700903200, ItemClassification.progression, "js"),
    "Javascript Comparison Operators": ItemData(6700903201, ItemClassification.progression, "js"),
    "Javascript 'if'": ItemData(6700903202, ItemClassification.progression, "js"),
    "Javascript 'else'": ItemData(6700903203, ItemClassification.progression, "js"),
    "Javascript 'else if'": ItemData(6700903204, ItemClassification.progression, "js"),
    "Javascript 'switch'": ItemData(6700903205, ItemClassification.progression, "js"),
    "Javascript 'for'": ItemData(6700903206, ItemClassification.progression, "js"),
    "Javascript 'forEach'": ItemData(6700903207, ItemClassification.progression, "js"),
    "Javascript 'while'": ItemData(6700903208, ItemClassification.progression, "js"),
    "Javascript '+'": ItemData(6700903209, ItemClassification.progression, "js"),
    "Javascript '-'": ItemData(6700903210, ItemClassification.progression, "js"),
    "Javascript '*'": ItemData(6700903211, ItemClassification.progression, "js"),
    "Javascript '/'": ItemData(6700903212, ItemClassification.progression, "js"),
    "Javascript '%'": ItemData(6700903213, ItemClassification.progression, "js"),
    "Javascript '**'": ItemData(6700903214, ItemClassification.progression, "js"),
    "Javascript Increment/Decrement": ItemData(6700903215, ItemClassification.progression, "js"),
    "Javascript '&&'": ItemData(6700903216, ItemClassification.progression, "js"),
    "Javascript '||'": ItemData(6700903217, ItemClassification.progression, "js"),
    "Javascript '!'": ItemData(6700903218, ItemClassification.progression, "js"),
    "Javascript 'in'": ItemData(6700903219, ItemClassification.progression, "js"),
}

apcode_items = {  # 6700900000 range for items
    **junk_items,  # 1000
    **misc_items,  # 2000
    **python_items,  # 3100
    **javascript_items,  # 3200
}

item_table = {**apcode_items}

item_frequencies = {"Progressive Problem Unlock": 4}

junk_weights = {
    "Github Copilot": 50,
    "Claude Code": 50,
    "Cursor": 50,
    "Google Jules": 50,
    "Gemini Code Assist": 50,
    "ChatGPT": 50,
    "Aider": 50,
}
