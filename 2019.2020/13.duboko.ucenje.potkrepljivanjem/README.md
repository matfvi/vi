# Vežbe 13 - Duboko učenje potkprepljivanjem (eng. Deep Reinforcement learning)

U ovom delu bavićemo se dubokim učenjem potkrpeljivanjem (eng. Deep Reinforcement learning) i pogledaćemo dva poznata algoritma:

- REINFORCE iz Policy gradient porodice algoritama
- Duboka Q mreža (eng. Deep Q network)

Neki članci i kursevi koji vam mogu biti korisni:
- David Silver, Deep RL kurs, [YouTube](https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ)
- Andrej Karpathy blog, [Deep Reinforcement Learning: Pong from Pixels](http://karpathy.github.io/2016/05/31/rl/)
- Medium: [Reinforcement Learning w/ Keras + OpenAI: DQNs](https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c)

### Duboka Q mreža (eng. Deep Q network)

<img src="https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fnature14236/MediaObjects/41586_2015_Article_BFnature14236_Fig1_HTML.jpg" alt="rl diagram">

Duboka Q mreža (eng. Deep Q network) je predstavnik takozvanih
**off policy** algoritama,
odnosno algoritama koji ne uče direktno politiku, već pokušavaju
da aproksimiraju optimalnu Q vrednost. Dva od poznatijih
radova na ovu temu su:
- [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)
- [Human-level control through deep reinforcement learning](https://web.stanford.edu/class/psych209/Readings/MnihEtAlHassibis15NatureControlDeepRL.pdf) 


- `01.deepqn`
    - `dqn.py`
        - Implementacija DQN-a
    - `01.train.dqn.py`
        - Obučava DQN nad okruženjem [CartPole-v1](https://gym.openai.com/envs/CartPole-v1/)
    - `02.run.dqn.py`
        - Pokreće i ilustruje obučeni DQN
- `beleske.rl.pdf`
    - Nastavak beleški iz oblasti RL