import numpy as np
import gym
from gym import wrappers
from tqdm import tqdm
import random
import matplotlib.pyplot as plt


"""
Igra predstavlja simulaciju kretanja po lancu, pri čemu su dozvoljene dve akcije:
- Akcija 0: kretanje unapred po lancu, bez nagrade
- Akcija 1: restart u stanje 0, dobija se mala nagrada 2

Ako se dostigne kraj lanca, dobija se velika nagrada vrednosti 10,
i ako agent u tom stanju nastavi kretanje unapred, dobija ponovo nagradu 10.

Prilikom preduzimanja akcije, postoji mala verovatnoća da se agent oklizne, i da bude učinjena suprotna akcija od zahtevane.
"""

class NChainAgent:

    def __init__(self, env, learning_rate, gamma, epsilon, min_epsilon, max_epsilon, decay_rate):
        self.env = env
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.state_size = env.observation_space.n
        self.action_size = env.action_space.n
        self.q_table = np.zeros((self.state_size, self.action_size))
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.max_epsilon = max_epsilon
        self.decay_rate = decay_rate

        self.show_info()

    def q_learning(self, max_steps=10, total_episodes=1000):
        self.episode_rewards = np.zeros(total_episodes)
        self.episode_epsilon = np.zeros(total_episodes)
        
        for episode_i in range(total_episodes):
            state = self.env.reset()

            for step in range(max_steps):
                # ========== VAS KOD IDE OVDE ==========
                # (e) Implementirati neophodne korake u algoritmu Q ucenja u okviru funkcije `q_learning`.

                # Odabir akcije
                action = self.get_action(state)
                # Azuriranje okruzenja
                new_state, reward, done, _ = self.env.step(action)

                # Azuriranje q tabele
                self.q_table[state, action] = self.update_q_table(state, new_state, action, reward, done)

                # Azuriranje stanja
                state = new_state

                # Akumuliramo nagradu po epizodi radi kasnije iscrtavanja
                self.episode_rewards[episode_i] += reward

                # Ako je okruzenje vratilo indikator da je kraj, stajemo sa iteriranjem
                if done:
                    break
                # ========== KRAJ VASEG KODA ==========

            # ========== VAS KOD IDE OVDE ==========
            # (e) Implementirati neophodne korake u algoritmu Q ucenja u okviru funkcije `q_learning`.
            # Pratimo vrednost eps vrednosti radi kasnije iscrtavanja
            self.episode_epsilon[episode_i] = self.epsilon

            # Azuriranje epsilon vrednosti za tekucu epizodu
            self.update_epsilon(episode_i)
            # ========== KRAJ VASEG KODA ==========

            if episode_i % 100 == 0:
                print(f'Episode {episode_i} done.')

    def get_action(self, state):
        """
        Odabir akcije na e-greedy nacin
        Args:
          state (int): Trenutno stanje okruzenja
        Returns:
          action (int): Akcija koju ce agent preduzeti u sledecem koraku.
        """
        # ========== VAS KOD IDE OVDE ==========
        # (b) U funkciji `get_action` implementirati odabir akcije na epsilon pohlepan nacin.
        if random.uniform(0,1) >= self.epsilon:
            action = np.argmax(self.q_table[state, :])
        else:
            action = self.env.action_space.sample()
        return action
        # ========== KRAJ VASEG KODA ==========

    def update_epsilon(self, episode):
        """
        Smanjuje se epsilon
        Args:
            episode (int): broj episode
        """
        # ========== VAS KOD IDE OVDE ==========
        # (d) U funkciji `update_epsilon` implementirati azuriranje epsilon po formuli koja je data u formulaciji zadatka.
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)
        # ========== KRAJ VASEG KODA ==========

    def update_q_table(self, state, new_state, action, reward, done):
        """
        Azurira se Q tablica.
        Args:
            state (int): trenutno stanje okruzenja
            new_state (int): novo stanje okruzenja
            action (int): trenutna akcija koju je izvrsio agent
            reward (int): trenutna nagrada koja je vracena za akciju `action`
            done (boolean): indikator o tome da li je epizoda zavrsena
        Returns:
            q_table (array): azurirana q tabela
        """
        # ========== VAS KOD IDE OVDE ==========
        # (c) U funkciji `update_q_table` implementirati azuriranje q tabele
        return self.q_table[state,action] + self.learning_rate * \
                            (reward + self.gamma * np.max(self.q_table[new_state, :]) * (1- done) - self.q_table[state, action])
        # ========== VAS KOD IDE OVDE ==========

    def show_info(self):
        print(f'State size: {self.state_size}')
        print(f'Action size: {self.action_size}')
        print(f'Q table shape: {self.q_table.shape}')
        print(f'learning_rate: {self.learning_rate}')
        print(f'gamma: {self.gamma}')
        print(f'epsilon: {self.epsilon}')
        print(f'min_epsilon: {self.min_epsilon}')
        print(f'max_epsilon: {self.max_epsilon}')
        print(f'decay_rate: {self.decay_rate}')

if __name__ == "__main__":
    # ========== VAS KOD IDE OVDE ==========
    # (a) Napraviti okruzenje NChain-v0 kroz biblioteku gym
    env = gym.make('NChain-v0')
    # ========== KRAJ VASEG KODA ==========

    learning_rate = 0.8
    gamma = 0.9
    eps = 1
    min_eps = 0
    max_eps = 1
    decay_rate = 0.008

    agent = NChainAgent(env, learning_rate, gamma, eps, min_eps, max_eps, decay_rate)

    max_steps = 10
    total_episodes = 1000

    agent.q_learning(max_steps=max_steps, total_episodes=total_episodes)

    # ========== VAS KOD IDE OVDE ==========
    # (f) Nacrtati kako se kroz epizode menjala nagrada koju je ostvarivao agent (oznaciti sta X i Y osa prikazuju).
    plt.plot(agent.episode_rewards)
    plt.xlabel('Broj epizode')
    plt.ylabel('Nagrada')
    plt.show()
    # ========== KRAJ VASEG KODA ==========

    # ========== VAS KOD IDE OVDE ==========
    # (g) Nacrtati kako se kroz epizode menjala vrednost za epsilon (oznaciti sta X i Y osa prikazuju).
    plt.plot(agent.episode_epsilon)
    plt.xlabel('Broj epizode')
    plt.ylabel('Epsilon')
    plt.show()
    # ========== KRAJ VASEG KODA ==========
