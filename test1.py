import numpy as np


def arithmetic_progression(x, common_difference):
    progression = [1]
    while True:
        progression.append(progression[-1] + common_difference)
        if progression[-1] > x:
            break

    return progression[:-1]


a = arithmetic_progression(100, 3)
print(a)
