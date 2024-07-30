"""Module contains the Part class."""

import os
import random
from collections.abc import Iterable

from effect import Effect, ProportionalEffect, StaticEffect
from utils import load_jsonc


class Title:
    """Stores a list of effects cooresponding to a title."""

    titles_data: dict = None

    def __init__(self, title_name: str):
        """Instantiate Title."""
        self.effects: list[Effect] = []

        title_data = Title.get_template_data(title_name)

        for effects in title_data.get("effects"):

            scaling = effects.get("scaling")
            if scaling == "proportional":
                self.effects.append(
                    ProportionalEffect(
                        effects.get("health", 1),
                        effects.get("defense", 1),
                        effects.get("attack", 1),
                    )
                )
            elif scaling == "static":
                self.effects.append(
                    StaticEffect(
                        effects.get("health", 0),
                        effects.get("defense", 0),
                        effects.get("attack", 0),
                    )
                )
            else:
                raise RuntimeError(f'Invalid scaling metric "{scaling}"')

    @classmethod
    def get_template_data(cls, title_name: str):
        """Return the template data for a title given the name."""
        if cls.titles_data is None:
            cls.titles_data = load_jsonc(os.path.join(".", "data", "titles.jsonc"))

        title_data = cls.titles_data.get(title_name)
        if title_data is None:
            raise ValueError(f'Title "{title_name}" not found.')

        return title_data


class Part:
    """
    Class for Monster parts. Intended to be instantiated using factory methods.

    NOTE: Construction based on json data assumes a certain structure and a
    json structure that differs may lead to undefined behavior, if not erroring.
    """

    parts_data: dict = None

    def __init__(
        self,
        health: float,
        attack: float,
        defense: float,
        female_sockets_max: int,
        male_sockets_max: int,
        slots_max: int,
        modifier: float,
        titles: tuple[Title],
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

        for title in titles:
            for effect in title.effects:
                self.apply_effect(effect)

    def __repr__(self):
        """Return repr for class."""
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
        """Apply an effect to a part."""
        self.health, self.defense, self.attack = effect.apply(
            self.health, self.defense, self.attack
        )

    @classmethod
    def factory_natural(cls, part_name: str, titles: tuple[str] = tuple()):
        """
        Construct a Part.

        This is intended to be used for naturally generated parts.
        """
        part_data = Part.get_template_data(part_name)

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
    def factory_player(
        cls,
        part_name: str,
        modifier: float,
        health: int,
        defense: int,
        attack: int,
        titles: tuple[str] = tuple(),
    ):
        """
        Construct a Part.

        This is intended to be used for minigame generated parts.
        """
        part_data = Part.get_template_data(part_name)

        sockets = part_data.get("sockets")
        female_sockets_max = sockets.get("female")
        male_sockets_max = sockets.get("male")
        slots_max = part_data.get("slots")

        return Part(
            health=health,
            defense=defense,
            attack=attack,
            female_sockets_max=female_sockets_max,
            male_sockets_max=male_sockets_max,
            slots_max=slots_max,
            modifier=modifier,
            titles=titles,
        )

    @classmethod
    def get_template_data(cls, part_name: str):
        """Return the template data for a part given the name."""
        if cls.parts_data is None:
            cls.parts_data = load_jsonc(os.path.join(".", "data", "parts.jsonc"))

        part_data = cls.parts_data.get(part_name)
        if part_data is None:
            raise ValueError(f'Part "{part_name}" not found.')

        return part_data
