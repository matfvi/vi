import gym
import gym.spaces
import numpy as np
import random


def taxiagent(verbose=False):
    # Niz u kome cemo cuvati sve nagrade
    scores = []
    
    # Pravimo taxi v3 okruzenje
    env = gym.make("Taxi-v3")

    # Inicijalizujemo Q tabelu
    Q = np.zeros((env.observation_space.n, env.action_space.n))

    # Epsilon koje cemo koristiti za istrazivanje okruzenja
    epsilon = 1.0
    # Minimalno epsilon koje cemo dopustiti tokom rada
    epsilon_min = 0.005
    # Faktor smanjivanja epsilon parametra
    epsilon_decay = 0.99993
    # Ukupan broj epizoda koje ce agent da odigra
    episodes = 50000
    # Maksimalna duzina trajanja epizode
    max_steps = 100
    # Korak ucenja (alfa)
    learning_rate = 0.65
    # Faktor umanjenja (eng. discount), gama
    gamma = 0.65

    for episode in range(episodes):
        # Uzimamo pocetno stanje
        state = env.reset()
        done = False
        score = 0

        for _ in range(max_steps):
            # Sa verovatnocom (1-epsilon) biramo najbolju akciju koju znamo.
            if random.uniform(0, 1) > epsilon:
                action = np.argmax(Q[state, :])
            # Inace biramo nasumicnu akciju.
            else:
                action = env.action_space.sample()

            # Izvrsavamo odabranu akciju.
            next_state, reward, done, _ = env.step(action)

            # Uracunavamo tekucu nagradu za nagradu u okviru epizode.
            score += reward

            # Azuriramo Q tabelu.
            Q[state, action] = (1 - learning_rate) * Q[state, action] + learning_rate * (reward + gamma * np.max(Q[next_state,:]))

            # Azuriramo stanje.
            state = next_state

            if done:
                break
        
        # Smanjujemo epsilon (Exploration-Exploitation trade-off)
        if epsilon >= epsilon_min:
            epsilon *= epsilon_decay

        scores.append(score)
        
        if verbose:
            print("Episode: {}/{}, score: {}".format(episode+1, episodes, score))
    
    return scores


if __name__ == "__main__":
    taxiagent(verbose=True)
