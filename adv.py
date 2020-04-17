from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque
import time 
# Load world
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
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
playermap = {}
playermap[player.current_room.id] = {ex: '?' for ex in player.current_room.get_exits()}

cardinals = 'n e w s'.split()
counter_dir = {'n':'s','s':'n','e':'w','w':'e'}

# while len(que) > 0:
    #check playermap for room
            #if not in map
            # add room id ~~> (player.current_room.id)
                # add exits ~~> (player.current_room.get_exits())
                # add exit id or '?'

def bfs(player, playermap):
    que = deque() # append()/popleft()
    que.append([player.current_room.id])
    visited = set()
    direction_que = deque()
    directions = []

    while len(que) > 0:
        path = que.popleft()
        if direction_que:
            directions = direction_que.popleft()
        current_room = path[-1]
        

        if current_room == '?':
            return directions
        possible_dirs = list(playermap[current_room].keys())
        random.shuffle(possible_dirs)
        for direction in possible_dirs:
            print(playermap[current_room])
            if playermap[current_room][direction] not in visited:
                visited.add(current_room)
                new_dirs = directions + [direction]
                previous_room = current_room
                new_path = path + [playermap[current_room][direction]]
                que.append(new_path)
                direction_que.append(new_dirs)
            
            



#while playermap keys is smaller than world map keys
while len(playermap.keys()) < len(world.rooms.keys()):
    path = deque(bfs(player, playermap))

    while len(path) > 0:
        print(f'~~~~~~~~~Rooms Discovered: {len(playermap.keys())}~~~~~~~~~~~~~~')
        previous_room = player.current_room.id #set before moving
        direction = path.popleft() #get direction (reduce length)
        
        player.travel(direction) # moving
        current_room = player.current_room.id #update after move
        print(f'Moved {direction} to {current_room}')


        if current_room not in playermap:
            playermap[current_room] = {ex: '?' for ex in player.current_room.get_exits()}
        
        playermap[previous_room][direction] = current_room #update LAST rooms exit with current room id
        playermap[current_room][counter_dir[direction]] = previous_room

        traversal_path.append(direction)


        
    

       # ~~ RANDOM TRAVEL ~~ #
    # randir = random.choice(cardinals)
    # if playermap[player.current_room.id].get(randir, None) == '?':
    #     traversal_path.append(randir)
    #     player.travel(randir)





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
