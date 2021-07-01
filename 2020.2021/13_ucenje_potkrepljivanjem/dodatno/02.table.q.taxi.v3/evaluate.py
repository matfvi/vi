import matplotlib.pyplot as plt
import taxiagent
import randomagent

# Izvrsavamo oba algoritma
random_agent_scores = randomagent.randomagent(verbose=True)
q_agent_scores = taxiagent.taxiagent(verbose=True)

# Crtamo nagrade
plt.plot(random_agent_scores, "ko", markersize=0.3)
plt.title("Random Agent")
plt.xlabel('Episodes')
plt.ylabel('Score')
plt.show()

plt.plot(q_agent_scores, "ko", markersize=0.3)
plt.title("Q-learning Agent")
plt.xlabel('Episodes')
plt.ylabel('Score')
plt.show()
