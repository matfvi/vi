import gym
import numpy as np
import math
from collections import deque
from tqdm import tqdm

class CartPole():
    def __init__(self, buckets=(1, 1, 6, 12,), n_episodes=1000, min_alpha=0.1, min_epsilon=0.1, gamma=1.0, ada_divisor=25, max_env_steps=None):
        # Parametar oznacava na koliko diskretnih atributa delimo redom 4 vrednosti koje opisuju stanje
        self.buckets = buckets
        # Broj epizoda tokom obucavanja
        self.n_episodes = n_episodes
        # Minimalni korak ucenja koji se dozvoljava
        self.min_alpha = min_alpha
        # Minimalno epsilon koje dozvoljavamo
        self.min_epsilon = min_epsilon
        # Faktor umenjenja gama
        self.gamma = gamma
        # Parametar koji se koristi da se malo finije azuriraju korak ucenja i epsilon
        self.ada_divisor = ada_divisor
        # Pravimo okruzenje
        self.env = gym.make('CartPole-v0')
        if max_env_steps is not None: self.env._max_episode_steps = max_env_steps

        # Inicijalizujemo Q tablicu, primetite da koristimo broj `bucket`-a jer cemo
        # da diskretizujemo parametre koji opisuju stanje.
        the_shape = self.buckets + (self.env.action_space.n,)
        self.Q = np.zeros(the_shape)

    def discretize(self, obs):
        """Diskretizuje kontinualne parametre"""
        upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50)]
        lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50)]
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    def choose_action_eps_greedy(self, state, epsilon):
        """Bira akciju na osnovu epsilon pohlepne politike"""
        return self.env.action_space.sample() if (np.random.random() <= epsilon) else np.argmax(self.Q[state])

    def choose_best_action(self, state):
        return np.argmax(self.Q[state])

    def update_q(self, state_old, action, reward, state_new, alpha):
        """
        Algoritam Q ucenja. Na predavanjima ste videli (1-alfa) uz prvi clan i alfa uz drugi clan.
        Cesto se u praksi srece i varijanta gde se Q(s, a) ubaci unutar drugog clana. Ovde je namerno
        ostavljena takva formulacija :)
        """
        self.Q[state_old][action] += alpha * (reward + self.gamma * np.max(self.Q[state_new]) - self.Q[state_old][action])

    # Azuriramo epsilon - jedan od nacina da se to uradi u praksi
    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    # Azuriramo korak ucenja - jedan od nacina da se to uradi u praksi
    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def test_agent(self, should_render=False):
        current_state = self.discretize(self.env.reset())
        done = False
        total_reward = 0

        while not done:
            # Render environment
            if should_render:
                self.env.render()

            # Biramo najbolju akciju koju je agent naucio
            action = self.choose_best_action(current_state)
            obs, reward, done, _ = self.env.step(action)
            new_state = self.discretize(obs)
            current_state = new_state
            total_reward += reward

        return total_reward

    def run(self, should_render=False):
        for e in tqdm(range(self.n_episodes)):
            # Diskretizujemo parametre koji opisuju stanja
            current_state = self.discretize(self.env.reset())

            # Uzimamo odg. korak ucenja i parametar epsilon za trenutnu iteraciju
            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            done = False
            i = 0

            while not done:
                # Render environment
                if should_render:
                    self.env.render()

                # Biramo akciju pomocu epsilon pohlepne politike
                action = self.choose_action_eps_greedy(current_state, epsilon)
                obs, reward, done, _ = self.env.step(action)
                new_state = self.discretize(obs)

                # Azuriramo Q tabelu
                self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += 1

            # print(f'Episode {e} completed.')

        if should_render:
            self.env.close()

if __name__ == "__main__":
    """
    Stanje u ovom svetu je opisano sa 4 kontinualne promenljive:
    - x (pozicija postolja) ∈ [-4.8, 4.8]
    - v (brzina postolja) ∈ [-3.4*10^38, 3.4*10^38]
    - theta (ugao štapa) ∈ [-0.42, 0.42]
    - w (ugaona brzina štapa) ∈ [-3.4*10^38, 3.4*10^38]

    Kod preuzet sa adrese:
    https://mc.ai/openai-gyms-cart-pole-balancing-using-q-learning/

    Ispostavlja se da atributi x i v mogu da se prakticno izostave iz ucenja.
    Razlog za to je sto se okruzenje restartuje samo nakon 200 koraka, a sansa
    da postolje izadje izvan za to vreme je jako "mala".

    Diskretizaciju cemo uraditi na sledeci nacin:
    - x (pozicija postolja) ∈ [-4.8, 4.8] -> 1 diskretna vrednost
    - v (brzina postolja) ∈ [-3.4*10^38, 3.4*10^38] -> diskretna vrednost
    - theta (ugao štapa) ∈ [-0.42, 0.42] -> 6 diskretnih vrednosti
    - w (ugaona brzina štapa) ∈ [-3.4*10^38, 3.4*10^38] -> 12 diskretnih vrednosti
    """

    solver = CartPole()
    print('Training agent')
    solver.run()
    print('done!')

    # Nakon treninga, mozemo da pustimo agenta da malo balansira :)
    print('Giving it a test run...')
    reward = solver.test_agent(True)
    print(f'done with reward: {reward}!')

    