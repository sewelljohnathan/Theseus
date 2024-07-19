import os
import random
from collections.abc import Iterable

from utils import load_jsonc


class Part:
    """
    Class for Monster parts. Intended to be instantiated using factory methods.

    NOTE: Construction based on json data assumes a certain structure and a
    json structure that differs may lead to undefined behavior, if not erroring.
    Ensure that the json document passes this regex:
    {\s*(?:"[\w\d\s]+":\s*{\s*"baseStats":\s*{\s*"stitch":\s*[0-9]+,\s*"nerve":\s*[0-9]+,\s*"bone":\s*[0-9]+\s*},\s*"sockets":\s*{\s*"female":\s*[0-9]+,\s*"male":\s*[0-9]+\s*},\s*"slots":\s*[0-9]\s*},?\s*)*}
    """

    def __init__(
        self,
        stitches: int,
        nerves: int,
        bones: int,
        female_sockets_max: int,
        male_sockets_max: int,
        slots_max: int,
        modifier: float,
        titles: tuple[str],
    ):
        if isinstance(titles, Iterable) is False:
            raise ValueError('Argument "titles" must be an iterable.')

        # Rarity / Minigame modifier
        stitches *= modifier
        nerves *= modifier
        bones *= modifier

        # Title modifiers
        titles_data = load_jsonc(os.path.join(".", "data", "titles.jsonc"))
        for title in titles:
            if title not in titles_data:
                raise ValueError(f'Title "{title}" not found.')

            title_data = titles_data.get(title)
            for effects in title_data.get("effects"):

                scaling = effects.get("scaling")
                if scaling == "proportional":
                    stitches *= effects.get("stitch", 1)
                    nerves *= effects.get("nerve", 1)
                    bones *= effects.get("bone", 1)
                elif scaling == "static":
                    stitches += effects.get("stitch", 0)
                    nerves += effects.get("nerve", 0)
                    bones += effects.get("bone", 0)
                else:
                    raise RuntimeError(f'Invalid scaling metric "{scaling}"')

        stitches = round(stitches)
        nerves = round(nerves)
        bones = round(bones)

        self.stitches = stitches
        self.stitches_max = stitches
        self.nerves = nerves
        self.nerves_max = nerves
        self.bones = bones
        self.bones_max = bones
        self.female_sockets: list[Part] = []
        self.female_sockets_max = female_sockets_max
        self.male_sockets: list[Part] = []
        self.male_sockets_max = male_sockets_max
        self.slots = []
        self.slots_max = slots_max

    def __repr__(self):
        return f"""Part(
    stitches={self.stitches},
    nerves={self.nerves},
    bones={self.bones},
    female_sockets_max={self.female_sockets_max},
    female_sockets_used={len(self.female_sockets)},
    male_sockets_max={self.male_sockets_max},
    male_sockets_used={len(self.male_sockets)},
    slots_max={self.slots_max},
    slots_used={len(self.slots)}
)"""

    @classmethod
    def factory_natural(cls, name: str, titles: tuple[str] = tuple()):

        parts_data = load_jsonc(os.path.join(".", "data", "parts.jsonc"))

        part_data = parts_data.get(name)
        if part_data is None:
            raise ValueError(f'Part "{name}" not found.')

        base_stats = part_data.get("baseStats")
        stitches = base_stats.get("stitch")
        nerves = base_stats.get("nerve")
        bones = base_stats.get("bone")

        sockets = part_data.get("sockets")
        female_sockets_max = sockets.get("female")
        male_sockets_max = sockets.get("male")

        slots_max = part_data.get("slots")

        modifier = random.uniform(0.5, 2)

        return Part(
            stitches=stitches,
            nerves=nerves,
            bones=bones,
            female_sockets_max=female_sockets_max,
            male_sockets_max=male_sockets_max,
            slots_max=slots_max,
            modifier=modifier,
            titles=titles,
        )
