from pydantic import BaseModel


class create_room(BaseModel):
    owner_name: str
    imposters: int


class player(BaseModel):
    player_name: str
    room_number: str


class game_room(BaseModel):
    room_number: str
