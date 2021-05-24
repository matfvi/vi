import gym
import gym.spaces
import numpy as np
import random


def randomagent(verbose=False):
    # Niz u kome cemo cuvati sve nagrade
    scores = []
    
    # Pravimo taxi v3 okruzenje
    env = gym.make("Taxi-v3")

    # Ukupan broj epizoda koje ce agent da odigra
    episodes = 50000

    # Maksimalna duzina trajanja epizode
    max_steps = 100

    for episode in range(episodes):
        # Uzimamo pocetno stanje
        env.reset()
        done = False
        score = 0

        for _ in range(max_steps):
            # Izvrsavamo nasumicnu akciju
            action = env.action_space.sample()
            _, reward, done, _ = env.step(action)
            score += reward
            if done:
                break
        
        scores.append(score)
        if verbose:
            print("Episode: {}/{}, score: {}".format(episode+1, episodes, score))

    return scores


if __name__ == "__main__":
    randomagent(verbose=True)
