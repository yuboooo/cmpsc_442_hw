from queue import PriorityQueue
import math


def main():
    scene1 = [[False, False, False], [False, True, False], [False, False, False]]
    scene2 = [[False, False, False], [True, True, True], [False, False, False]]
    print(find_path((0,0), (2, 1), scene1))

# Euclidean distance heuristic
def ed_h(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

def get_moves(current_location, scene):
    current_location_x, current_location_y = current_location
    max_x, max_y = len(scene) - 1, len(scene[0]) - 1
    for possible_move_x in range(current_location_x - 1, current_location_x + 2):
        for possible_move_y in range(current_location_y - 1, current_location_y + 2):
            if 0 <= possible_move_x <= max_x and 0 <= possible_move_y <= max_y and scene[possible_move_x][possible_move_y] == False:
                yield possible_move_x, possible_move_y

def find_path(start, goal, scene):
    # Edge case check: Can't start or end at obstacles
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None

    PQ = PriorityQueue()
    cost_till_current = 0
    total_cost = ed_h(start, goal) + cost_till_current
    current_path = [start]
    current_location = start
    PQ.put((total_cost, cost_till_current, current_path, current_location))
    visited = set()
    while not PQ.empty():
        _, cost_till_current, current_path, current_location = PQ.get()
        if current_location in visited:
            continue
        else:
            visited.add(current_location)
        if current_location == goal:
            return current_path
        for new_location in get_moves(current_location, scene):
            if new_location not in visited:
                updated_path = current_path + [new_location]
                PQ.put((cost_till_current + ed_h(current_location, new_location) + ed_h(new_location, goal), 
                cost_till_current + ed_h(current_location, new_location), updated_path, new_location))
    return None


if __name__ == "__main__":
    main()
