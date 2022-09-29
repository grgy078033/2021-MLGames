"""
Agent learns the policy based on Q-learning with Q table.
Based on the example here: https://medium.com/@tuzzer/cart-pole-balancing-with-q-learning-b54c6068d947
"""
import math

import gym
import numpy as np


def choose_action(state, q_table, action_space, epsilon):
    if np.random.random_sample() < epsilon: # 有 ε 的機率會選擇隨機 action (Exploration)
        return action_space.sample() 
    else: # 其他時間根據現有 policy 選擇 action (Exploitation)
          # 也就是在 Q table 裡目前 state 中，選擇擁有最大 Q value 的 action
        return np.argmax(q_table[state]) 

def get_state(observation, n_buckets, state_bounds):
    state = [0] * len(observation) 
    for i, s in enumerate(observation): # 每個 feature 有不同的分配
        l, u = state_bounds[i][0], state_bounds[i][1] # 每個 feature 值的範圍上下限
        if s <= l: # 低於下限，分配為 0
            state[i] = 0
        elif s >= u: # 高於上限，分配為最大值
            state[i] = n_buckets[i] - 1
        else: # 範圍內，依比例分配
            state[i] = int(((s - l) / (u - l)) * n_buckets[i])

    return tuple(state)

if __name__ == '__main__':
    env = gym.make('CartPole-v0')

    # 準備 Q table
    ## Environment 中各個 feature 的 bucket 分配數量
    ## 1 代表任何值皆表同一 state，也就是這個 feature 其實不重要
    n_buckets = (1, 1, 6, 3)

    ## Action 數量 
    n_actions = env.action_space.n

    ## State 範圍 
    state_bounds = list(zip(env.observation_space.low, env.observation_space.high))
    state_bounds[1] = [-0.5, 0.5]
    state_bounds[3] = [-math.radians(50), math.radians(50)]
    
    ## Q table，每個 state-action pair 存一值 
    q_table = np.zeros(n_buckets + (n_actions,))

    # 一些學習過程中的參數
    get_epsilon = lambda i: max(0.01, min(1, 1.0 - math.log10((i+1)/25)))  # epsilon-greedy; 隨時間遞減
    get_lr = lambda i: max(0.01, min(0.5, 1.0 - math.log10((i+1)/25))) # learning rate; 隨時間遞減 
    gamma = 0.99 # reward discount factor

    # Q-learning
    for i_episode in range(200):
        epsilon = get_epsilon(i_episode)
        lr = get_lr(i_episode)

        observation = env.reset() # reset environment to initial state for each episode
        rewards = 0 # accumulate rewards for each episode
        state = get_state(observation, n_buckets, state_bounds) # 將連續值轉成離散 
        for t in range(250):
            env.render()

            # Agent takes action
            action = choose_action(state, q_table, env.action_space, epsilon) # choose an action based on q_table 
            observation, reward, done, info = env.step(action) # do the action, get the reward

            rewards += reward
            next_state = get_state(observation, n_buckets, state_bounds)

            # 更新 Q table
            q_next_max = np.amax(q_table[next_state])
            q_table[state + (action,)] += lr * (reward + gamma * q_next_max - q_table[state + (action,)])

            # 前進下一 state 
            state = next_state

            if done:
                print('Episode finished after {} timesteps, total rewards {}'.format(t+1, rewards))
                break

    env.close() # need to close, or errors will be reported
