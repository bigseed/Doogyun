import numpy as np


def k(s):
    n = 10
    l = []
    for _ in range(n):
        info = dict(x=s.copy())
        l.append(info)
    return l


b = np.array([[1, 2], [3, 4]])
r = k(b)
r[0]['x'] = 1
print(r)
