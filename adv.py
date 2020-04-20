from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
lowest = 99999999
while True:
    world = World()


    # You may uncomment the smaller graphs for development and testing purposes.
    # map_file = "maps/test_line.txt"
    # map_file = "maps/test_cross.txt"
    # map_file = "maps/test_loop.txt"
    # map_file = "maps/test_loop_fork.txt"
    map_file = "maps/main_maze.txt"

    # Loads the map into a dictionary
    room_graph=literal_eval(open(map_file, "r").read())
    world.load_graph(room_graph)

    # Print an ASCII map
    # world.print_rooms()

    player = Player(world.starting_room)

    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
    traversal_path = []

    reverse_choices = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    seen_rooms = {}

    # check if room has been found yet in our seen_rooms dictionary, if not found, add it to the dictionary with default values
    def add_seen_room(room):
        if room.id not in seen_rooms:
            north = south = east = west = None

            for valid_dir in room.get_exits():

                if valid_dir == 'n':
                    north = '?'
                elif valid_dir == 's':
                    south = '?'
                elif valid_dir == 'e':
                    east = '?'
                elif valid_dir == 'w':
                    west = '?'
                
            seen_rooms[room.id] = {'n': north, 's': south, 'e': east, 'w': west}

    # player.current_room.id
    # player.current_room.get_exits()
    # player.travel(direction)

    def steps_to_room(room):
        q = Queue()
        visited = set()

        path = [room]

        room_list = []

        steps = []

        # enqueue a PATH TO the starting node
        q.enqueue(path)

        # while our queue isn't empty
        while q.size() > 0:
        # dequeue, this is our current_path
            current_path = q.dequeue()
        # whatever is last in the current_path is our current_node
            current_room = current_path[-1]
        # check if current_node is destination_vertex
            add_seen_room(current_room)
            if '?' in seen_rooms[current_room.id].values():
                room_list = current_path
                # print(steps)
                break
                # break 

            # check if we have visited this node before
            if current_room not in visited:
                visited.add(current_room)
                # get our neighbors
                for direction in current_room.get_exits():
                    check_room = current_room.get_room_in_direction(direction)
                    # make each neighbor its own copy of the path
                    path_copy = current_path[:]
                    # and add the neighbor to it
                    path_copy.append(check_room)
                    # enqueue the path_copy
                    q.enqueue(path_copy)

        return room_list

    stack = Stack()

    # check if room has been found yet in our seen_rooms dictionary, if not found, add it to the dictionary with default values
    def add_seen_room(room):
        if room.id not in seen_rooms:
            north = south = east = west = None

            for valid_dir in room.get_exits():

                if valid_dir == 'n':
                    north = '?'
                elif valid_dir == 's':
                    south = '?'
                elif valid_dir == 'e':
                    east = '?'
                elif valid_dir == 'w':
                    west = '?'
                
            seen_rooms[room.id] = {'n': north, 's': south, 'e': east, 'w': west}

    # player.current_room.id
    # player.current_room.get_exits()
    # player.travel(direction)

    while True:
        # Pull a random direction from our current room
        rand_dir = random.choice(player.current_room.get_exits())

        current_room = player.current_room

        # Add our room to the seen_rooms dictionary
        add_seen_room(current_room)

        # print(seen_rooms)

        ##################################################
        ##################################################
        ##################################################

        foundQ = False
        for stuff in seen_rooms.values():
            if '?' in stuff.values():
                foundQ = True
        
        if foundQ == False:
            break
        
        # If we've already checked every direction in this room, move back.
        if '?' not in seen_rooms[current_room.id].values():

            # print(stack.stack)

            rooms = steps_to_room(current_room)

            for i in range(len(rooms)):
                if i < len(rooms) - 1:
                    for direction in rooms[i].get_exits():
                        if rooms[i].get_room_in_direction(direction).id == rooms[i + 1].id:
                            # print('took step')
                            player.travel(direction)
                            traversal_path.append(direction)

        # If chosen direction has already been explored, start over and generate a random direction we haven't explored yet
        if seen_rooms[current_room.id][rand_dir] != '?':
            continue

        ##################################################
        ##################################################
        ##################################################

        # If our direction is valid, push to stack as our next movement
        stack.push(rand_dir)
        current_path = stack.pop()
        current_dir = current_path[-1]
        
        # Travel in our direction and update our stack and traversal path
        player.travel(current_dir)
        traversal_path.append(current_dir)
        stack.push(current_dir)
        to_room = player.current_room

        # Update our seen_rooms dictionary to set our previous rooms direction to current rooms id
        seen_rooms[current_room.id][current_dir] = to_room.id
        
        # Add current room to our seen_rooms dictionary
        add_seen_room(to_room)

        # Update values of current rooms direction to point to previous room
        seen_rooms[to_room.id][reverse_choices[current_dir]] = current_room.id

        # print(traversal_path)


    # TRAVERSAL TEST - DO NOT MODIFY
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        if len(traversal_path) < lowest:
            lowest = len(traversal_path)
        print(lowest)
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")




####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


# # Load world
# lowest = 99999999
# while True:
#     world = World()

#     # You may uncomment the smaller graphs for development and testing purposes.
#     # map_file = "maps/test_line.txt"
#     # map_file = "maps/test_cross.txt"
#     # map_file = "maps/test_loop.txt"
#     # map_file = "maps/test_loop_fork.txt"
#     map_file = "maps/main_maze.txt"

#     # Loads the map into a dictionary
#     room_graph=literal_eval(open(map_file, "r").read())
#     world.load_graph(room_graph)

#     # Print an ASCII map
#     # world.print_rooms()

#     player = Player(world.starting_room)

#     # Fill this out with directions to walk
#     # traversal_path = ['n', 'n']
#     traversal_path = []

#     reverse_choices = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

#     seen_rooms = {}

#     stack = Stack()

#     # check if room has been found yet in our seen_rooms dictionary, if not found, add it to the dictionary with default values
#     def add_seen_room(room):
#         if room.id not in seen_rooms:
#             north = south = east = west = None

#             for valid_dir in room.get_exits():

#                 if valid_dir == 'n':
#                     north = '?'
#                 elif valid_dir == 's':
#                     south = '?'
#                 elif valid_dir == 'e':
#                     east = '?'
#                 elif valid_dir == 'w':
#                     west = '?'
                
#             seen_rooms[room.id] = {'n': north, 's': south, 'e': east, 'w': west}

#     # player.current_room.id
#     # player.current_room.get_exits()
#     # player.travel(direction)

#     while True:
#         # Pull a random direction from our current room
#         rand_dir = random.choice(player.current_room.get_exits())

#         current_room = player.current_room

#         # Add our room to the seen_rooms dictionary
#         add_seen_room(current_room)

#         # print(seen_rooms)

#         ##################################################
#         ##################################################
#         ##################################################

#         foundQ = False
#         for stuff in seen_rooms.values():
#             if '?' in stuff.values():
#                 foundQ = True
        
#         if foundQ == False:
#             break
        
#         # If we've already checked every direction in this room, move back.
#         if '?' not in seen_rooms[current_room.id].values():

#             # print(stack.stack)

#             direction = stack.pop()
#             # If direction is None, we've reached the end of our stack
#             if direction == None:
#                 break

#             # # # Reverse direction and move backwards
#             go_back = reverse_choices[direction]

#             player.travel(go_back)

#             # Update our traversal path to show us moving backwards
#             traversal_path.append(go_back)

#         # If chosen direction has already been explored, start over and generate a random direction we haven't explored yet
#         if seen_rooms[current_room.id][rand_dir] != '?':
#             continue

#         ##################################################
#         ##################################################
#         ##################################################

#         # If our direction is valid, push to stack as our next movement
#         stack.push(rand_dir)
#         current_path = stack.pop()
#         current_dir = current_path[-1]
        
#         # Travel in our direction and update our stack and traversal path
#         player.travel(current_dir)
#         traversal_path.append(current_dir)
#         stack.push(current_dir)
#         to_room = player.current_room

#         # Update our seen_rooms dictionary to set our previous rooms direction to current rooms id
#         seen_rooms[current_room.id][current_dir] = to_room.id
        
#         # Add current room to our seen_rooms dictionary
#         add_seen_room(to_room)

#         # Update values of current rooms direction to point to previous room
#         seen_rooms[to_room.id][reverse_choices[current_dir]] = current_room.id

#         # print(traversal_path)
    
#     # TRAVERSAL TEST - DO NOT MODIFY
#     visited_rooms = set()
#     player.current_room = world.starting_room
#     visited_rooms.add(player.current_room)

#     for move in traversal_path:
#         player.travel(move)
#         visited_rooms.add(player.current_room)

#     if len(visited_rooms) == len(room_graph):
#         if len(traversal_path) < lowest:
#             lowest = len(traversal_path)
#         print(lowest)
#         print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
#     else:
#         print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#         print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# ####### 
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
