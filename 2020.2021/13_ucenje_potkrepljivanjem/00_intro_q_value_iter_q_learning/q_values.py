import numpy as np
# T(s, a, s') shape=[s,a,s']
T = [
           # a0              # a1       #a2 
    [[0.7, 0.3, 0.0], [1.0, 0.0, 0.0], [0.8, 0.2, 0.0]], # s0
    [[0.0, 1.0, 0.0], None,            [0.0, 0.0, 1.0]], # s1
    [None,            [0.8, 0.1, 0.1], None]  # s2
]

# R(s, a, s') shape=[s, a, s']
R = [
    # a0           #a1        # a2
    [[+10, 0, 0], [0, 0, 0], [0,0,0]], # s0
    [[0, 0, 0] ,  [0, 0, 0], [0,0,-50]], # s1,
    [[0,0,0],     [+40, 0, 0], [0, 0, 0]], # s2
]

possible_actions = [[0,1,2], [0, 2], [1]]

Q_values = np.full((3,3), -np.inf) # 
for state, actions in enumerate(possible_actions):
    Q_values[state, actions] = 0.0

gamma = 0.8

for iteration in range(50):
    Q_prev = Q_values.copy()
    for s in range(3):
        for a in possible_actions[s]:
            Q_values[s, a] = np.sum([
                T[s][a][sp]*(R[s][a][sp] + gamma * np.max(Q_prev[sp]))
                for sp in range(3)
            ])

print(Q_values)
print(np.argmax(Q_values, axis=1))