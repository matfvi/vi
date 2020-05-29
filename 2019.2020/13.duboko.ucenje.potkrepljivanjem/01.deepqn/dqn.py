import gym
import random
import os
import numpy as np
from collections      import deque
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt


class Agent():
    def __init__(self, state_size, action_size, cold_start=False):
        self.weight_backup = "cartpole_weight.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.learning_rate = 0.001
        self.gamma = 0.95
        self.exploration_rate = 1.0
        self.exploration_min = 0.01
        self.exploration_decay = 0.995
        self.network = self._build_model()

        if not cold_start:
            if os.path.isfile(self.weight_backup):
                self.load_model()
                # Trebalo bi sacuvati epsilon prilikom cuvanja modela kako bi mogli
                # da rekonstruisemo epsilon prilikom ucitavanja modela i nastavaka obucavanja.
                # Radi jednostavnosti, ovde cemo prosto pretpostaviti da model naucen
                # tako da ima smisla postaviti epsilon na minimalno dopustenu vrednost
                # (koju smo mi definisali prethodno).
                # Trebalo bi dakle:
                # self.exploration_rate = load_epsilon_from_file('train_info.json') ili nesto slicno
                # Ali mi cemo postaviti self.exploration_min
                self.exploration_rate = self.exploration_min

    def _build_model(self):
        """Builds a neural network for DQN to use."""
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def save_model(self):
        """Saves the model weights to the path set in the object."""
        self.network.save(self.weight_backup)

    def load_model(self):
        """LOads the model weights from the path set in the object."""
        self.network.load_weights(self.weight_backup)

    def act(self, state):
        """Acts according to epsilon greedy policy."""
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.network.predict(state)
        return np.argmax(act_values[0])

    # Cuvamo iskustvo u memoriji
    def remember(self, state, action, reward, next_state, done):
        """Saves experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    # Ucimo na osnovu informacija u memoriji
    def learn(self, sample_batch_size):
        if len(self.memory) < sample_batch_size:
            return
        sample_batch = random.sample(self.memory, sample_batch_size)
        for state, action, reward, next_state, done in sample_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.network.predict(next_state)[0])
            target_f = self.network.predict(state)
            target_f[0][action] = target
            self.network.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay

class CartPole:
    def __init__(self):
        self.sample_batch_size = 32
        self.episodes = 2000
        self.env = gym.make('CartPole-v1')

        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        self.agent = Agent(self.state_size, self.action_size)

    def load_model(self):
        self.agent.load_model()

    def run_test(self):
        state = self.env.reset()

        self.env.render()
        done = False

        index = 0
        while not done:
            state = np.reshape(state, [1, self.state_size])
            action = self.agent.act(state)
            next_state, _, done, _ = self.env.step(action)
            state = next_state
            index += 1
            self.env.render()
        print(f'Score: {index+1}')

    def run_train(self):
        scores = []
        for index_episode in range(self.episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])

            done = False
            index = 0
            while not done:
                # Uglavnom ne zelimo render tokom obucavanja
                # jer drasticno usporava proces optimizacije.
                # self.env.render()

                # Pustamo agenta da uradi neku akciju.
                action = self.agent.act(state)

                # Azuriramo stanje okruzenja.
                next_state, reward, done, _ = self.env.step(action)

                # Menjamo oblik vektora za stanje kako bi stanje kasnije
                # mogli da propustimo kroz mrezu. Setite se, mreza prihvata
                # podskup instanci kao prvu dimenziju, usled toga dodajemo
                # jedinicu na pocetak - jer je ovo jedna instanca.
                next_state = np.reshape(next_state, [1, self.state_size])

                # Cuvamo iskustvo.
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                index += 1


            # Ispis procesa obucavanja u konzoli.
            # SAVET IZ PRAKSE:
            # Nije lose povremeno ove informacije pisati u datoteku, ali treba biti
            # pazljiv da se to ne radi stalno - nema smisla stalno pristupati disku
            # radi upisa jedne linije. Predlog je pisati u datoteku na svakih k epizoda (npr. k=100).
            print(f'Episode {index_episode+1}/{self.episodes} Score: {index + 1}')

            # Belezimo nagradu koju je agent osvojio u epizodi.
            scores.append(index + 1)

            # Pustamo agenta da uci.
            self.agent.learn(self.sample_batch_size)

            # Primer: Ima smisla zaustaviti proces obucavanja ranije.
            # Kako je maksimalna nagrada 500 u ovom okruzenju, ako nas
            # agent u poslednjih 10 epizoda prosecno osvoji nagradu blizu
            # maksimalnoj, reklo bi se da je optimizacioni proces blizu resenja,
            # pa ima smisla tada zaustaviti trening.
            # Ovo je prosta heuristika, postoje mnogo sofisticiraniji pristupi
            # vodjenja optimizacije. Imajte u vidu da je DQN i delom nestabilan
            # i ne mora nuzno da konvergira - setite se predavanja :)
            if index_episode > 10:
                last_10 = scores[-10:]
                avg = sum(last_10) / 10
                if avg > 490:
                    break

        
        # Kada se optimizacioni proces zavrsi, cuvamo tezine mreze.
        self.agent.save_model()

        # Vracamo istoriju treninga.
        return scores