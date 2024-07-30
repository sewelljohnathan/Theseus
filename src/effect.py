"""Module containing the Effect classes."""

from abc import ABC, abstractmethod


class Effect(ABC):
    """Abstract Effect parent class."""

    def __init__(self, health: float, defense: float, attack: float):
        """Initialize Effect."""
        self._health = health
        self._defense = defense
        self._attack = attack

    @abstractmethod
    def apply(
        self, health: float, defense: float, attack: float
    ) -> tuple[float, float, float]:
        """Return a tuple of new stats."""
        pass


class StaticEffect(Effect):
    """Class for static effects."""

    def apply(self, health: float, defense: float, attack: float):
        """Return a tuple of new stats."""
        return (health + self._health, defense + self._defense, attack + self._attack)


class ProportionalEffect(Effect):
    """Class for proportional effects."""

    def apply(self, health: float, defense: float, attack: float):
        """Return a tuple of new stats."""
        return (health * self._health, defense * self._defense, attack * self._attack)
