import re
import timeit
from collections import deque


def rpn_solver(rpn):
    res = deque()
    for x in rpn:
        if x == "*":
            a = res.pop()
            b = res.pop()
            res.append(a * b)
        elif x == "+":
            a = res.pop()
            b = res.pop()
            res.append(a + b)
        else:
            res.append(x)

    return res[0]


def solve1(s):
    cb = s.find(")")
    if cb >= 0:
        ob = s[:cb].rfind("(")
        return solve1(s[:ob] + solve1(s[ob + 1 : cb]) + s[cb + 1 :])
    stack = deque()
    for p in s.split():
        if p in {"+", "*"}:
            stack.append(p)
        else:
            stack.appendleft(p)
    ret = deque()
    for p in stack:
        if p == "+":
            a = ret.pop()
            b = ret.pop()
            ret.append(a + b)
        elif p == "*":
            a = ret.pop()
            b = ret.pop()
            ret.append(a * b)
        else:
            ret.append(int(p))
    return str(ret[0])


print("part1     ", sum(int(solve1(line)) for line in open("input.txt")))


def tokenizer(s):
    return re.findall(r"\d+|[()+*]", s)


def solve1RPN(s):
    stacks = [deque()]
    for token in tokenizer(s):
        if token in {"+", "*"}:
            stacks[-1].append(token)
        elif token == "(":
            stacks.append(deque())
        elif token == ")":
            s = stacks.pop()
            while s:
                stacks[-1].appendleft(s.pop())
        elif token.isdigit():
            stacks[-1].appendleft(int(token))
    # print(stacks)

    return rpn_solver(stacks[-1])


print("part1 RPN ", sum(int(solve1RPN(line)) for line in open("input.txt")))


from math import prod


def solve2(s):
    cb = s.find(")")
    if cb >= 0:
        ob = s[:cb].rfind("(")
        return solve2(s[:ob] + solve2(s[ob + 1 : cb]) + s[cb + 1 :])
    return str(prod(sum(int(y.strip()) for y in x.split("+")) for x in s.split("*")))


print("part2    ", sum(int(solve2(line)) for line in open("input.txt")))


def toRPN(s, debug=False):
    brackets_groups = []

    stacks = deque((deque(),))
    for c in tokenizer(s):
        if debug:
            print(f"---> {c}")
        if c == "+" and stacks[-1][-1] == "+":
            stacks[-1].append(c)
        elif c == "+" and stacks[-1][-1] != "+":
            n = stacks[-1].popleft()
            stacks.append(deque((n, c)))
        elif c == "*":
            stacks[-1].append(c)
        elif c == "(":
            brackets_groups.append(stacks)
            stacks = deque((deque(),))
        elif c == ")":
            while len(stacks) > 1:
                stack = stacks.pop()
                while stack:
                    stacks[-1].appendleft(stack.pop())
            if debug:
                print(f"--> {stacks=}")
            to_the_left = rpn_solver(stacks[0])
            stacks = brackets_groups.pop()
            stacks[-1].appendleft(to_the_left)
        else:
            stacks[-1].appendleft(int(c))
        if debug:
            print(f"{brackets_groups=}")
            print(f"{stacks=}")

    while len(stacks) > 1:
        stack = stacks.pop()
        while stack:
            stacks[-1].appendleft(stack.pop())

    return stacks[0]


def solve2RPN(expr, debug=False):
    rpn = toRPN(expr, debug)
    if debug:
        print(f"{rpn=}")

    return rpn_solver(rpn)


print("part2 RPN", sum(int(solve2RPN(line)) for line in open("input.txt")))


print(
    "solve1   ",
    timeit.timeit(
        'sum(int(solve1(line)) for line in open("input.txt"))',
        setup="from __main__ import solve1",
        number=100,
    ),
)
print(
    "solve1RPN",
    timeit.timeit(
        'sum(int(solve1RPN(line)) for line in open("input.txt"))',
        setup="from __main__ import solve1RPN",
        number=100,
    ),
)
print(
    "solve2   ",
    timeit.timeit(
        'sum(int(solve2(line)) for line in open("input.txt"))',
        setup="from __main__ import solve2",
        number=100,
    ),
)
print(
    "solve2RPN",
    timeit.timeit(
        'sum(int(solve2RPN(line)) for line in open("input.txt"))',
        setup="from __main__ import solve2RPN",
        number=100,
    ),
)
