from fastapi import APIRouter, WebSocket
from ..settings import *
from .. import schemas
import random

router = APIRouter()

@router.websocket('/create_room')
def create_room_route(websocket: WebSocket, request: schemas.create_room):
    owner = (websocket, request.owner_name)
    room_number = create_room(owner, request.imposters)
    join_room(room_number, owner)
    return ({'room_number': room_number})


@router.websocket('/join_game')
def join_game(websocket: WebSocket, request: schemas.player):
    player = (websocket, request.player_name)
    if request.room_number in temporary_rooms:
        join_room(request.room_number, player)


@router.websocket("/start/{room_number}")
def start_game(room_number):
    if room_number in temporary_rooms:
        room: Room = temporary_rooms[room_number]
        imposters = random.sample(room.players, room.imposters)
        for player in room.players:
            if player not in imposters:
                room.manager.send_personal_message(f"The location is {random.sample(places,1)}.", player[0])
            else:
                room.manager.send_personal_message(f"You are the imposter!! Try to blend in.", player[0])
            
