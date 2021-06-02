import gym
import tensorflow as tf
import numpy as np
def simple_rule_policy(obs):
    angle = obs[2]
    return 0 if angle < 0 else 1


env = gym.make('CartPole-v1')
obs = env.reset()

n_inputs = env.observation_space.shape[0]

n_iterations = 150
n_epsiode_per_update = 10
n_max_steps = 100
discount_factor = 0.95
lr = 0.01

optimizator = tf.keras.optimizers.Adam(lr=lr)
loss_fn = tf.keras.losses.binary_crossentropy

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(5, activation='elu', input_shape=[n_inputs]),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


def play_one_step(env, obs, model, loss_fn):
    with tf.GradientTape() as tape:
        left_prob = model(obs[np.newaxis])
        action = (tf.random.uniform([1,1]) > left_prob)
        y_target = tf.constant([[1.0]]) - tf.cast(action, tf.float32) #  1 <-
        loss = tf.reduce_mean(loss_fn(y_target, left_prob))
    grads = tape.gradient(loss, model.trainable_variables)
    obs, reward, done, _ = env.step(int(action[0,0].numpy()))
    return obs, reward, done, grads

def play_multiple_episodes(env, n_episodes, n_max_steps, model, loss_fn):
    all_rewards = []
    all_grads = []
    for episode in range(n_episodes):
        current_rewards = []
        current_grads = []
        obs = env.reset()
        for step in range(n_max_steps):
            obs, reward, done, grads = play_one_step(env, obs, model, loss_fn)
            current_rewards.append(reward)
            current_grads.append(grads)
            if done:
                break
        all_rewards.append(current_rewards)
        all_grads.append(current_grads)
    return all_rewards, all_grads

def discount_rewards(rewards, discount_factor):
    discounted = np.array(rewards)
    for step in range(len(rewards) - 2, -1, -1):
        discounted[step] += discounted[step + 1] * discount_factor
    return discounted

def discount_and_normalize_rewards(all_rewards, discount_factor):
    all_discounted_rewards = [discount_rewards(rewards, discount_factor) for rewards in all_rewards]
    flat_rewards = np.concatenate(all_discounted_rewards)
    rewards_mean = flat_rewards.mean()
    rewards_std = flat_rewards.std()
    return [(discounted_rewards - rewards_mean) / rewards_std for discounted_rewards in all_discounted_rewards]

print(discount_rewards([10, 0, -50], discount_factor=0.8))
print(discount_and_normalize_rewards([[10, 0, -50], [10,20]], discount_factor=0.8))

for iteration in range(n_iterations):
    print(iteration)
    all_rewards, all_grads = play_multiple_episodes(env, n_epsiode_per_update, n_max_steps, model, loss_fn)
    total_rewards = sum(map(sum, all_rewards))
    print("\rIteration: {}, mean rewards: {:1f}".format(iteration, total_rewards/n_epsiode_per_update), end="")
    all_final_rewards = discount_and_normalize_rewards(all_rewards, discount_factor)

    all_mean_grads = []
    for var_index in range(len(model.trainable_variables)):
        mean_grads = tf.reduce_mean(
            [final_reward * all_grads[epsiode_index][step][var_index] 
            for epsiode_index, final_rewards in enumerate(all_final_rewards) 
            for step, final_reward in enumerate(final_rewards)], axis=0
        )
        all_mean_grads.append(mean_grads)
    optimizator.apply_gradients(zip(all_mean_grads, model.trainable_variables))

import animate
frames = animate.render_policy_net(model)
animate.plot_animation(frames)