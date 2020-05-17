# Vežbe 12 - Učenje potkprepljivanjem (eng. Reinforcement learning)

- 01.table.q.frozen.lake
    - `frozen_lake_qlearning.ipynb`
        - Okruženje [FrozenLake-v0](https://gym.openai.com/envs/FrozenLake-v0/)
        - Uvod u *q* učenje
- 02.table.q.taxi
    - `randomagent.py`
        - Konstruiše agenta koju bira nasumičnu akciju
        - Okruženje [Taxi-v3](https://gym.openai.com/envs/Taxi-v3/)
    - `taxiagent.py`
        - Obučava agenta pomoću q učenja
        - Okruženje [Taxi-v3](https://gym.openai.com/envs/Taxi-v3/)
    - `evaluate.py`
        - Poredi prethodna dva agenta
- 03.cartpole
    - `cartpole.py`
        - Okruženje [CartPole-v0](https://gym.openai.com/envs/CartPole-v0/)
        - Diskretizuje kontinualne parametre koji opisuju stanja

## Biblioteka `gym`

Instalira se kao i većina drugih python paketa pomoću alata `pip`.

```
pip install gym
```

Kratak [tutorial](https://hub.packtpub.com/create-your-first-openai-gym-environment-tutorial/) za biblioteku.

## Tabelarno Q učenje

Beleške iz skripte možete pronaći [ovde](beleske.rl.pdf).

Materijali zasnovani na sledećin člancima i kodovima:
- [Frozen lake q learning](https://gist.github.com/jojonki/6291f8c3b19799bc2f6d5279232553d7)
- [Taxi-v3 q learning](https://github.com/phossen/reinforcement-learning-1)
- [Cartpole q learning](https://mc.ai/openai-gyms-cart-pole-balancing-using-q-learning/)

## Dodatni resursi

Dodatni resursi:
- Biblioteka [gym](https://gym.openai.com/)
- Tutorial za q učenje: [ovde](https://www.novatec-gmbh.de/en/blog/introduction-to-q-learning/)
- Beleške iz skripte: [ovde](beleske.rl.pdf)