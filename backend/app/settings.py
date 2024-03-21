import datetime
import random
import string
from utils import ConnectionManager
from fastapi import websockets

# A Temporary dataStructure to hold all the game's key information.
temporary_rooms: dict = {}
# Places for game purpose.
places = ['Hotel', 'Museum', 'Amusement Park',
          'Dog Park', 'Gas Station', 'Resturant']

class Room:
    def __init__(self, owner, imposters) -> None:
        # Room Name:
        self.room_number: str = self.generate_random_string()
        # Define expiration time for rooms (in seconds)
        self.ROOM_EXPIRATION_TIME: int = 3600  # 1 hour
        # A seperate connection manager per room.
        self.manager = ConnectionManager()
        # Define created time to keep track of room's time limit.
        self.created_at: datetime = datetime.datetime.now(),
        # Tuple for owner name and owner websocket
        self.owner: tuple = owner,
        # Value got when the room is defined by user.
        self.imposters: int = imposters
        # Players Value
        self.players: list = []

    def generate_random_string(self):
        # Define the characters to choose from
        characters = string.ascii_uppercase + string.digits
        # Generate a random string of specified length
        random_room = ''.join(random.choice(characters) for _ in range(5)).join(
            '-').join(random.choice(characters) for _ in range(5))
        if random_room in temporary_rooms:
            self.generate_random_string()
        return random_room


def create_room(owner: tuple, num_of_imposters: int):
    room = Room(owner=owner, imposters=num_of_imposters)
    room.players.append(owner)
    temporary_rooms[room.room_number] = room
    return room.room_number


def get_room(room_number):
    return temporary_rooms.get(room_number)


def join_room(room_number, player):
    room: Room = get_room(room_number)
    if room:
        room.players.append(player)
        return True
    return False


def is_room_expired(room_number):
    room: Room = get_room(room_number)
    if room:
        expiration_time = room['created_at'] + \
            datetime.timedelta(seconds=room.ROOM_EXPIRATION_TIME)
        return datetime.datetime.now() > expiration_time
    return True


def remove_room(room_number):
    if room_number in temporary_rooms and is_room_expired(room_number):
        room: Room = get_room(room_number)
        room.manager.disconnect_all()
        del temporary_rooms[room_number]
