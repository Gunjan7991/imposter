from pydantic import BaseModel


class imposter_in(BaseModel):
    num_of_imposter: int


class player(BaseModel):
    name: str
    verify: str


class game_room(BaseModel):
    room_number: str
