from dataclasses import dataclass


@dataclass(frozen=True)
class Sticker:
    """Cromo identificable del album."""

    id: int
    equipo: str = ""
