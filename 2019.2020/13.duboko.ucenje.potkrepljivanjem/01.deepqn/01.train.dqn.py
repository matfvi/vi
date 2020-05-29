import gym
import random
import os
import numpy as np
from collections      import deque
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from dqn import Agent, CartPole


if __name__ == "__main__":
    cartpole = CartPole()
    scores = cartpole.run_train()
    plt.plot(scores)
    plt.savefig('scores.png')
    plt.show()
