from queue import Queue
from copy import deepcopy
import time


def main():
    print(solve_identical_disks(4, 2))
    print(solve_identical_disks(4, 3))
    print(solve_identical_disks(5, 2))
    print(solve_identical_disks(5, 3))
    print("##########################")
    print(solve_distinct_disks(4, 2))
    print(solve_distinct_disks(4, 3))
    print(solve_distinct_disks(5, 2))
    print(solve_distinct_disks(5, 3))

def solve_identical_disks(length, n):

    q = Queue()
    visited = []
    disks_state = [1 if i < n else 0 for i in range(length)] 
    total_moves = []
    q.put((total_moves, disks_state))

    while not q.empty():
        total_moves, current_disks = q.get()
        if sum(current_disks[length-n:]) == n:
            return total_moves
        if current_disks in visited:
            continue
        else:
            visited.append(current_disks)
        
        def move_disks(step, location):
            new_disks = deepcopy(current_disks)
            temp = new_disks[location]
            new_disks[location] = new_disks[location + step]
            new_disks[location + step] = temp
            new_moves = deepcopy(total_moves)
            new_moves.append((location, location + step))
            return (new_moves, new_disks)

        for i in range(length):
            if i < length - 1 and current_disks[i] != 0 and current_disks[i+1] == 0:
                q.put(move_disks(1, i))
            if i < length - 2 and current_disks[i] != 0 and current_disks[i + 1] != 0 and current_disks[i + 2] == 0:
                q.put((move_disks(2, i)))
    return None



def solve_distinct_disks(length, n):
    q = Queue()
    visited = []
    disks_state = [i if i <= n else 0 for i in range(1, length + 1)]
    total_moves = []
    q.put((total_moves, disks_state))
    
    while not q.empty():
        total_moves, current_disks = q.get()
        goal = sorted(current_disks, reverse=True)
        if sum(current_disks[length-n:]) == ((1 + n) * n) // 2 and goal[:n] == current_disks[length - n:]:
            return total_moves
        if current_disks in visited:
            continue
        else:
            visited.append(current_disks)

        def move_disks(step, location):
            new_disks = deepcopy(current_disks)
            temp = new_disks[location]
            new_disks[location] = new_disks[location + step]
            new_disks[location + step] = temp
            new_moves = deepcopy(total_moves)
            new_moves.append((location, location + step))
            return (new_moves, new_disks)

        for i in range(length):
                    if i < length - 1 and current_disks[i] != 0 and current_disks[i+1] == 0:
                        q.put(move_disks(1, i))
                    if i < length - 2 and current_disks[i] != 0 and current_disks[i + 1] != 0 and current_disks[i + 2] == 0:
                        q.put(move_disks(2, i))
                    if i > 0 and current_disks[i] != 0 and current_disks[i - 1] == 0:
                        q.put(move_disks(-1, i))
                    if i > 1 and current_disks[i] != 0 and current_disks[i - 1] != 0 and current_disks[i - 2] == 0:
                        q.put(move_disks(-2, i))
    return None



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

