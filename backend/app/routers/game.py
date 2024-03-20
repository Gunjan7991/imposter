from fastapi import APIRouter, WebSocket
from ..settings import *
from .. import schemas
import random

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.put('/create_room', response_model=None)
def create_room_route(request: schemas.imposter_in, response_model=None):
    room_id = create_room(request.num_of_imposter)
    return ({'room_id': room_id})


@router.put('/join_game')
def join_game(request: schemas.player):
    if request.verify in temporary_rooms:
        join_room(request.verify, request.name)


@router.websocket("/start/{room_number}")
def start_game(room_number):
    if room_number in temporary_rooms:
        imposters = random.sample(
            temporary_rooms[room_number]['players'], temporary_rooms[room_number]['num_of_imposters'])
