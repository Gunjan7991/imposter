import datetime
import random
import string


# Dictionary to store temporary rooms
temporary_rooms = {}

# Places for game purpose.
places = ['Hotel', 'Museum', 'Amusement Park',
          'Dog Park', 'Gas Station', 'Resturant']

# Define expiration time for rooms (in seconds)
ROOM_EXPIRATION_TIME = 3600  # 1 hour


def generate_random_string():
    # Define the characters to choose from
    characters = string.ascii_uppercase + string.digits

    # Generate a random string of specified length
    random_room = ''.join(random.choice(characters) for _ in range(8))
    if random_room in  temporary_rooms:
        generate_random_string()
    return  random_room


def create_room(num_of_imposters: int):
    room_id = generate_random_string()
    room_data = {
        'created_at': datetime.datetime.now(),
        'players': [],
        'num_of_imposters': num_of_imposters,
        # Add more game-related data here
    }
    temporary_rooms[room_id] = room_data
    return room_id


def get_room(room_id):
    return temporary_rooms.get(room_id)


def join_room(room_id, player_name):
    room = get_room(room_id)
    if room:
        room['players'].append(player_name)
        return True
    return False


def is_room_expired(room_id):
    room = get_room(room_id)
    if room:
        expiration_time = room['created_at'] + \
            datetime.timedelta(seconds=ROOM_EXPIRATION_TIME)
        return datetime.datetime.now() > expiration_time
    return True


def remove_room(room_id):
    if room_id in temporary_rooms and is_room_expired(room_id):
        del temporary_rooms[room_id]
