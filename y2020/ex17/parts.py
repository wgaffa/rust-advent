from multiprocessing import Pool


# @profile
def neighbours_of_point(p, deltas=set(), cache=dict()):
    if not deltas:
        delta = [-1] * len(p)
        for _ in range(3 ** len(p)):
            if not all(x == 0 for x in delta):
                deltas.add(tuple(delta))
            ptr = 0
            while ptr < len(delta):
                if delta[ptr] < 1:
                    delta[ptr] += 1
                    break
                else:
                    delta[ptr] = -1
                    ptr += 1
    tp = tuple(p)
    if tp not in cache:
        cache[tp] = set(tuple(a + b for a, b in zip(p, delta)) for delta in deltas)
    return cache[tp]


# @profile
def count_neighbours(board, p, deltas=set()):
    if not deltas:
        deltas.update(neighbours_of_point([0] * len(p)))
    return sum(1 for delta in deltas if tuple(a + b for a, b in zip(p, delta)) in board)


def rules(args):
    board, cell = args
    n = count_neighbours(board, cell)
    if (cell in board and n in {2, 3}) or (cell not in board and n == 3):
        return cell


# @profile
def next_board(board):
    ret = set()
    to_look_up = set(board)  # copy
    for p in board:
        to_look_up.update(neighbours_of_point(p))
    with Pool(16) as pool:
        for cell in pool.map(rules, ((board, x) for x in to_look_up)):
            if cell:
                ret.add(cell)
    # for cell in to_look_up:
    #     n = count_neighbours(board, cell)
    #     if (cell in board and n in {2, 3}) or (cell not in board and n == 3):
    #         ret.add(cell)
    return ret


# @profile
def main():
    with open("input.txt") as f:
        inpu = f.read()

    board = set()
    for y, row in enumerate(inpu.splitlines()):
        for x, cell in enumerate(row):
            if cell == "#":
                board.add((x, y, 0, 0))
                # board.add((x, y, 0))

    for _ in range(6):
        board = next_board(board)

    print(len(board))


if __name__ == "__main__":
    main()
