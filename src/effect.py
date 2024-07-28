from abc import ABC, abstractmethod


class Effect(ABC):

    def __init__(self, health: float, defense: float, attack: float):
        self._health = health
        self._defense = defense
        self._attack = attack

    @abstractmethod
    def apply(
        self, health: float, defense: float, attack: float
    ) -> tuple[float, float, float]:
        pass


class StaticEffect(Effect):

    def __init__(self, health: float, defense: float, attack: float):
        super().__init__(health, defense, attack)

    def apply(self, health: float, defense: float, attack: float):
        return (health + self._health, defense + self._defense, attack + self._attack)


class ProportionalEffect(Effect):

    def __init__(self, health: float, defense: float, attack: float):
        super().__init__(health, defense, attack)

    def apply(self, health: float, defense: float, attack: float):
        return (health * self._health, defense * self._defense, attack * self._attack)
