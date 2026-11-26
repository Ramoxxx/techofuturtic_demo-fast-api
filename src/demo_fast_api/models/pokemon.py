
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True
    )


class APIResource(APIModel):
    name: str
    url: str


class Ability(APIResource):
    pass


class Abilities(APIModel):
    is_hidden: bool
    slot: int
    ability: Ability | None = None


class Generation(APIResource):
    pass


class PastAbilities(APIModel):
    generation: Generation
    abilities: list[Abilities] = Field(default_factory=list)


class Forms(APIResource):
    pass


class Version(APIResource):
    pass


class GameIndices(APIModel):
    game_index: int
    version: Version


class VersionGroup(APIResource):
    pass


class MoveLearnMethod(APIResource):
    pass


class VersionGroupDetails(APIModel):
    level_learned_at: int
    version_group: VersionGroup
    move_learn_method: MoveLearnMethod
    order: int | None = None
    enhancement_level: int | None = None


class Move(APIResource):
    pass


class Moves(APIModel):
    move: Move
    version_group_details: list[VersionGroupDetails] = Field(
        default_factory=list
    )


class Species(APIResource):
    pass


class Home(APIModel):
    front_shiny: str | None = None
    front_female: str | None = None
    front_default: str | None = None
    front_shiny_female: str | None = None


class Showdown(APIModel):
    back_shiny: str | None = None
    back_female: str | None = None
    front_shiny: str | None = None
    back_default: str | None = None
    front_female: str | None = None
    front_default: str | None = None
    back_shiny_female: str | None = None
    front_shiny_female: str | None = None


class DreamWorld(APIModel):
    front_female: str | None = None
    front_default: str | None = None


class OfficialArtwork(APIModel):
    front_shiny: str | None = None
    front_default: str | None = None


class Other(APIModel):
    home: Home | None = None
    showdown: Showdown | None = None
    dream_world: DreamWorld | None = None
    official_artwork: OfficialArtwork | None = Field(
        default=None,
        alias="official-artwork"
    )


class Sprites(APIModel):
    other: Other | None = None
    versions: dict[str, Any] = Field(default_factory=dict)

    back_shiny: str | None = None
    back_female: str | None = None
    front_shiny: str | None = None
    back_default: str | None = None
    front_female: str | None = None
    front_default: str | None = None
    back_shiny_female: str | None = None
    front_shiny_female: str | None = None


class Cries(APIModel):
    latest: str | None = None
    legacy: str | None = None


class Stat(APIResource):
    pass


class Stats(APIModel):
    base_stat: int
    effort: int
    stat: Stat


class PastStats(APIModel):
    generation: Generation
    stats: list[Stats] = Field(default_factory=list)


class Type(APIResource):
    pass


class Types(APIModel):
    slot: int
    type: Type


class Pokemon(APIModel):
    id: int
    name: str
    base_experience: int | None = None
    height: int
    is_default: bool
    order: int
    weight: int

    abilities: list[Abilities] = Field(default_factory=list)
    past_abilities: list[PastAbilities] = Field(default_factory=list)
    forms: list[Forms] = Field(default_factory=list)
    game_indices: list[GameIndices] = Field(default_factory=list)

    held_items: list[Any] = Field(default_factory=list)
    location_area_encounters: str

    moves: list[Moves] = Field(default_factory=list)
    species: Species
    sprites: Sprites
    cries: Cries | None = None

    stats: list[Stats] = Field(default_factory=list)
    past_stats: list[PastStats] = Field(default_factory=list)
    types: list[Types] = Field(default_factory=list)
    past_types: list[Any] = Field(default_factory=list)
