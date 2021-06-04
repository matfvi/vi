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

alpha0 = 0.05 
decay = 0.005
gamma = 0.90
state = 0

def exploration_policy(state):
    return np.random.choice(possible_actions[state])

def step(state, action):
    p = T[state][action]
    next_state = np.random.choice([0,1,2], p = p)
    r = R[state][action][next_state]
    return next_state, r

Q_values = np.full((3,3), -np.inf)
for state, action in enumerate(possible_actions):
    Q_values[state][action] = 0 

for iteration in range(10000):
    action = exploration_policy(state)
    next_state, reward = step(state, action)
    next_value = np.max(Q_values[next_state])
    alpha = alpha0 / (1 + iteration * decay)
    Q_values[state, action] *= 1 - alpha
    Q_values[state, action] += alpha * (reward + gamma * next_value)
    state = next_state

print(Q_values)
print(np.argmax(Q_values, axis=1))