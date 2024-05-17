from collections import deque
import sys

dq = deque()

for i in range(1, len(sys.argv)):
    dq.append(sys.argv[i])
    if len(dq) == 3:
        print(dq)
        dq.clear()

