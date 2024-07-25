"""
Module contains the Part class.
"""

import os
import random
from collections.abc import Iterable

from effect import Effect, ProportionalEffect, StaticEffect
from utils import load_jsonc


class Part:
    """
    Class for Monster parts. Intended to be instantiated using factory methods.

    NOTE: Construction based on json data assumes a certain structure and a
    json structure that differs may lead to undefined behavior, if not erroring.
    """

    def __init__(
        self,
        health: float,
        attack: float,
        defense: float,
        female_sockets_max: int,
        male_sockets_max: int,
        slots_max: int,
        modifier: float,
        titles: tuple[str],
    ):
        """Instantiate Part."""
        if isinstance(titles, Iterable) is False:
            raise ValueError('Argument "titles" must be an iterable.')

        self.health = health
        self.health_max = health
        self.defense = defense
        self.attack = attack
        self.female_sockets: list[Part] = []
        self.female_sockets_max = female_sockets_max
        self.male_sockets: list[Part] = []
        self.male_sockets_max = male_sockets_max
        self.slots = []
        self.slots_max = slots_max

        # Rarity / Minigame Effect
        self.apply_effect(ProportionalEffect(modifier, modifier, modifier))

        # Title effects
        titles_data = load_jsonc(os.path.join(".", "data", "titles.jsonc"))
        for title in titles:
            if title not in titles_data:
                raise ValueError(f'Title "{title}" not found.')

            title_data = titles_data.get(title)
            for effects in title_data.get("effects"):

                scaling = effects.get("scaling")
                if scaling == "proportional":
                    self.apply_effect(
                        ProportionalEffect(
                            effects.get("health", 1),
                            effects.get("defense", 1),
                            effects.get("attack", 1),
                        )
                    )
                elif scaling == "static":
                    self.apply_effect(
                        StaticEffect(
                            effects.get("health", 0),
                            effects.get("defense", 0),
                            effects.get("attack", 0),
                        )
                    )
                else:
                    raise RuntimeError(f'Invalid scaling metric "{scaling}"')

    def __repr__(self):
        return f"""Part(
    health={self.health},
    defense={self.defense},
    attack={self.attack},
    female_sockets_max={self.female_sockets_max},
    female_sockets_used={len(self.female_sockets)},
    male_sockets_max={self.male_sockets_max},
    male_sockets_used={len(self.male_sockets)},
    slots_max={self.slots_max},
    slots_used={len(self.slots)}
)"""

    def apply_effect(self, effect: Effect):
        self.health, self.defense, self.attack = effect.apply(
            self.health, self.defense, self.attack
        )

    @classmethod
    def factory_natural(cls, name: str, titles: tuple[str] = tuple()):

        parts_data = load_jsonc(os.path.join(".", "data", "parts.jsonc"))

        part_data = parts_data.get(name)
        if part_data is None:
            raise ValueError(f'Part "{name}" not found.')

        cost = part_data.get("cost")
        sockets = part_data.get("sockets")
        female_sockets_max = sockets.get("female")
        male_sockets_max = sockets.get("male")
        slots_max = part_data.get("slots")

        return Part(
            health=cost // 3,
            defense=cost // 3,
            attack=cost // 3,
            female_sockets_max=female_sockets_max,
            male_sockets_max=male_sockets_max,
            slots_max=slots_max,
            modifier=random.uniform(0.5, 2),
            titles=titles,
        )

    @classmethod
    def factory_player(cls, name: str, modifier: float, titles: tuple[str] = tuple()):

        parts_data = load_jsonc(os.path.join(".", "data", "parts.jsonc"))

        part_data = parts_data.get(name)
        if part_data is None:
            raise ValueError(f'Part "{name}" not found.')

        cost = part_data.get("cost")
        sockets = part_data.get("sockets")
        female_sockets_max = sockets.get("female")
        male_sockets_max = sockets.get("male")
        slots_max = part_data.get("slots")

        return Part(
            health=cost // 3,
            defense=cost // 3,
            attack=cost // 3,
            female_sockets_max=female_sockets_max,
            male_sockets_max=male_sockets_max,
            slots_max=slots_max,
            modifier=modifier,
            titles=titles,
        )
