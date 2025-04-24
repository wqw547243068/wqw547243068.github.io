---
layout: post
title:  "强化学工具及应用"
date:   2020-05-15 17:34:00
categories: 深度学习
tags: 强化学习 增强学习 量化交易 游戏  俄罗斯方块
excerpt: RL工具包，及应用场景案例
author: 鹤啸九天
mathjax: true
permalink: /rl_application
---

* content
{:toc}

# 强化学习工具及应用

## RL 理论

详见站内专题: [强化学习](rl)


## 工具




### gym


OpenAI开发了用于研发和比较强化学习算法的工具包 gym库。

gym 提供方便快捷的**模拟器**接口，一行代码构建能够于强化学习算法交互的模拟器

#### 函数

step() 方法 非常核心，负责推进环境（模拟器或游戏）状态，并返回一些有用信息。
- 每一步，算法会传入一个动作到 step() 方法，然后返回新的状态、奖励等信息。

注：
- 新版 `Env.step` 函数现在返回5个值，而不是之前的4个。
- 这5个返回值分别是：`观测`（observation）、`奖励`（reward）、`是否结束`（done）、`是否截断`（truncated）和`其他信息`（info）。


step() 方法调用后返回四个主要元素：
- 观察（observation）：这通常是一个数组或其他数据结构，表示环境的当前状态。
- 奖励（reward）：一个数值，表示执行上一个动作后获得的即时奖励。
- 完成标记（done）：一个布尔值，表示是否达到了环境的结束条件。
- 额外信息（info）：一个字典，可能包含额外的调试信息或其他元数据。通常不应用于训练模型。

与其他技术比较，比如传统的监督学习，强化学习和 gym库的 step() 方法提供了更加动态和交互式的方式来训练模型。
- 监督学习中，一次性获取所有的输入和输出
- 而强化学习中，step() 方法让模型能够与环境进行连续的交互。

对于模拟复杂任务（比如游戏、机器人导航等）非常有用，因为允许模型在学习过程中不断地接收反馈，并据此调整行为。

示例

```py
# !pip install gym

import gym

env = gym.make('CarDriving-v0')
observation = env.reset() # 初始的观察
action = choose_action(observation)  # 算法选择的动作
observation, reward, done, info = env.step(action)
```

#### 示例



##### 月球车


代码

```py
import gym

env_name = "LunarLander-v2"
env = gym.make(env_name)          # 导入注册器中的环境

episodes = 10
for episode in range(1, episodes + 1):
    state = env.reset()           # gym风格的env开头都需要reset一下以获取起点的状态
    done = False
    score = 0

    while not done:
        env.render()              # 将当前的状态化成一个frame，再将该frame渲染到小窗口上
        action = env.action_space.sample()     # 通过随机采样获取一个随即动作
        n_state, reward, done, info = env.step(action)    # 将动作扔进环境中，从而实现和模拟器的交互
        score += reward
    print("Episode : {}, Score : {}".format(episode, score))

env.close()     # 关闭窗口
```


### pygame

【2025-4-24】win 11 上调试pygame做的俄罗斯方块游戏，按 E/R/T 无反应

Pygame 可能遇到**按键无响应**问题
- 尤其是在中文输入法模式下

分析
- Pygame 默认将输入法模式设置为中文，导致按键事件无法正常捕获

解决：
- ① 按 shift: 切换输入法模式即可
- ② 代码中关闭中文输入模式

```py
mport pygame

pygame.init()
screen = pygame.display.set_mode([640, 480])
pygame.key.stop_text_input() # 停止文本输入模式

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        print("你按下了q键")
  pygame.quit()
```


### Stable Baselines3

德国 German Aerospace Center (DLR) 研究员 [Antonin Raffin](https://araffin.github.io/#contact) 开发  [Stable Baselines3](https://araffin.github.io/post/sb3/) 强化学习算法工具包

Stable Baselines3 建立在PyTorch之上，提供清晰、简单且高效的强化学习算法实现。
- 该库是 Stable Baselines 库的延续，采用了更为现代和标准的编程实践

stable_baselines3 能够快速完成强化学习算法的搭建训练和评估，包括保存，录视频等
- [官方文档](https://stable-baselines3.readthedocs.io/en/master/)
- [使用Stable Baselines3进行强化学习实验示例](https://zhuanlan.zhihu.com/p/551082373)

Stable Baselines3 为图像 （CnnPolicies）、其他类型的输入要素 （MlpPolicies） 和多个不同的输入 （MultiInputPolicies） 提供策略网络。
- MlpPolicies: MLP 结构
- CnnPolicies: CNN 结构
- MultiInputPolicies: 


#### 安装

命令

```sh
pip install stable_baselines3 gym shimmy pygame
# 或源码
git clone https://github.com/DLR-RM/stable-baselines3.git
```



#### 函数


##### BaseAlgorithm

A2C 和 PPO 继承自 `BaseAlgorithm` 类。

重要函数
- `__init__`: 构造函数,初始化方法用于配置算法的参数和环境。
- `_setup_model` 方法: 设置算法需要的模型，例如神经网络架构。
- `learn` 方法: 主要训练循环，其中包含了数据收集、优化等步骤。
- `collect_rollouts` 方法 (仅在 A2C 中): 收集经验数据，这些数据将用于训练。
- `_update` 方法 (仅在 PPO 中): 核心更新步骤，包括执行多次优化迭代。

#### 功能


##### 日志

stable_baselines3 封装了 tensorboard 前端服务, 可视化接口

```sh
tensorboard -logdir .\tensorboard\LunarLander-v2\
```

##### loss

loss 是当前策略网络查询得到的Q值和固定的目标网络查询的Q值的L1 loss



#### 模型


模型参数

```py
model = DQN(
    "MlpPolicy", 
    env=env, 
    learning_rate=5e-4,
    batch_size=128,
    buffer_size=50000,
    learning_starts=0,
    target_update_interval=250,
    policy_kwargs={"net_arch" : [256, 256]},
    verbose=1,
    tensorboard_log="./tensorboard/LunarLander-v2/"
)
```




#### 应用


##### 离线策略 Pendulum

同时用多个离线策略算法环境，更新 `gradient_steps` 参数
- 将其设置为 `gradient_steps=-1`，以执行所收集到的转换所需的所有梯度步骤

代码

```py
import gym

from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env

env = make_vec_env("Pendulum-v0", n_envs=4, seed=0)

# We collect 4 transitions per call to `ènv.step()`
# and performs 2 gradient steps per call to `ènv.step()`
# if gradient_steps=-1, then we would do 4 gradients steps per call to `ènv.step()`
model = SAC('MlpPolicy', env, train_freq=1, gradient_steps=2, verbose=1)
model.learn(total_timesteps=10_000)
```


##### 小车单摆 CartPole

PPO 训练 CartPole


```py
import gym
from stable_baselines3 import PPO

def main():
    env = gym.make('CartPole-v1')  # 创建环境
    model = PPO("MlpPolicy", env, verbose=1)  # 创建模型
    model.learn(total_timesteps=20000)  # 训练模型
    model.save("ppo_cartpole")  # 保存模型
    test_model(model)  # 测试模型


def test_model(model):
    env = gym.make('CartPole-v1', render_mode='human')  # 可视化只能在初始化时指定
    obs, _ = env.reset()
    done1, done2 = False, False
    total_reward = 0

    while not done1 or done2:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done1, done2, info = env.step(action)
        total_reward += reward

    print(f'Total Reward: {total_reward}')
    env.close()


if __name__ == "__main__":
    main()
```

另一个示例

```py
import gym
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed

def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = gym.make(env_id)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env_id = "CartPole-v1"
    num_cpu = 4  # Number of processes to use
    # Create the vectorized environment
    env = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])

    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you.
    # You can choose between `DummyVecEnv` (usually faster) and `SubprocVecEnv`
    # env = make_vec_env(env_id, n_envs=num_cpu, seed=0, vec_env_cls=SubprocVecEnv)

    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=25_000)

    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
```

##### 月球车 LunarLander


```py
import gym

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


env_name = "LunarLander-v2"
env = gym.make(env_name)          # 导入注册器中的环境
env = DummyVecEnv([lambda : env]) # env 包装，从而将环境向量化, 便于同时使用多个环境，提高采样和训练的效率

model = DQN(
    "MlpPolicy", # DQN 策略, MLP 神经网络
    env=env,
    verbose=1
)

# 启动训练
# total_timesteps 总时间步, 模拟的 state,action,reward,next state 采样数量
model.learn(total_timesteps=1e5)

# 评估效果
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=False)
env.close()
mean_reward, std_reward # (-166.24617834256043, 50.530194648006685)
# 模型保存
model.save("./model/LunarLander3.pkl")
```

预测

```py
env = gym.make(env_name)
model = DQN.load("./model/LunarLander3.pkl")

state = env.reset()
done = False 
score = 0
while not done:
    action, _ = model.predict(observation=state)
    state, reward, done, info = env.step(action=action)
    score += reward
    env.render()
env.close()
score
```

另一个完整示例

```py
import gym

from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

# Create environment
env = gym.make('LunarLander-v2')

# Instantiate the agent
model = DQN('MlpPolicy', env, verbose=1)
# Train the agent
model.learn(total_timesteps=int(2e5))
# Save the agent
model.save("dqn_lunar")
del model  # delete trained model to demonstrate loading

# Load the trained agent
# NOTE: if you have loading issue, you can pass `print_system_info=True`
# to compare the system on which the model was trained vs the current one
# model = DQN.load("dqn_lunar", env=env, print_system_info=True)
model = DQN.load("dqn_lunar", env=env)

# Evaluate the agent
# NOTE: If you use wrappers with your environment that modify rewards,
#       this will be reflected here. To evaluate with original rewards,
#       wrap environment in a "Monitor" wrapper before other wrappers.
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

# Enjoy trained agent
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    env.render()
```

## 应用


### 量化交易

#### 强化学习量化交易分类

- 【2022-3-14】[【RL-Fintech】强化学习在金融量化领域的最新进展](https://zhuanlan.zhihu.com/p/472254985)
- RL在量化交易里面的应用，大致分为4种：
  - Portfolio Management（投资组合管理）—— 低频
    - 通过灵活分配资产权重获得更高超额收益的问题。现实中的应用例子比如选股和指数增强基金。一般的解决方案是对股票的涨价潜力进行打分，买入具有上涨潜力的股票并增加权重，卖出可能跌或者相对弱势的股票。这是一个多时间序列（Multiple Time Series）上的权重再分配问题。
    - 两篇baseline是 AlphaStock（2019） 和 DeepTrader（2021）
  - Single-asset trading signal （单资产交易信号） —— 中高频
    - 单资产的交易信号问题是指对单一资产进行买卖操作以获得比单纯持有更高利润的问题。监督学习在这类问题中取得了比较大的成功。
    - 前面介绍的PM问题进来的研究热点在于时空关系的发掘方面，并没有很多RL算法设计上的独特创新。事实上RL独特的reward设计在2000-2006年左右研究得比较多，当时受制于算力，一般都还是单一资产的交易问题上进行应用。
  - Execution（交易执行）—— 高频
  - Option hedging（期权对冲和定价）。
  - 其中PM一般是**低频**交易，单股交易信号一般是中高频，交易执行一般是**高频**tick级数据上的策略，至于期权定价则是理论和实践统一起来的工作。
  - ![](https://pic1.zhimg.com/80/v2-8e107d2e5429947601312abd7d61f498_720w.jpg)

### 如何应用RL

- 【2021-4-6】[强化学习（Reinforcement Learning）在量化交易领域如何应用](https://www.zhihu.com/question/45116323/answer/758082798)

> 讲个大实话：这个问题的答案其实都不用看，肯定都不靠谱，靠谱的肯定不会告诉你

感兴趣的朋友可以在[BigQuant AI](https://bigquant.com/%3Futm_source%3Dzhihu%26utm_medium%3Dzhihu_answer%26utm_campaign%3D190723_758082798_zhihu_answer)平台上动手实践一下
 
1\. 相比（无）监督学习，强化学习在量化领域应用时，首先需要建立一个环境，在环境中定义state，action，以及reward等。定义的方式有多种选择，比如：
- **state**: 可以将n天的价格，交易量数据组合成某一天的state,也可以用收益率或是其他因子组合作为某一天的state，如果想要定义有限个的state,可以定义为appreciated/ hold_value/ depreciated这样3类。
- **action**: 可以定义为buy/sell两种, 也可以定义为buy/sell/hold三种，或者定义为一个（-1,1）之间的一个连续的数，-1和1分别代表all out 和 holder两个极端。
- **reward**: 可以定义为新旧总资产价值之间的差，或是变化率，也可以将buy时的reward定义为0，sell时的定义为买卖价差。
 
2\. 需要选择一个具体的强化学习方法：
- 1) Q-table (具体可参考：[Reinforcement Learning Stock Trader](https://link.zhihu.com/?target=https%3A//bigquant.com/community/t/topic/169658%3Futm_source%3Dzhihu%26utm_medium%3Dzhihu_answer%26utm_campaign%3D190723_758082798_zhihu_answer))
  - ![](https://pic1.zhimg.com/50/v2-32586bdcd7b20c55790c2447583e3b2a_hd.jpg?source=1940ef5c)
  - ![](https://pic1.zhimg.com/80/v2-32586bdcd7b20c55790c2447583e3b2a_720w.jpg?source=1940ef5c)
  - Q-table里state是有限的，而我们定义的state里面的数据往往都是连续的，很难在有限个state里面去很好的表达。
- 2) Deep Q Network（参考：[Reinforcement Learning for Stock Prediction](https://link.zhihu.com/?target=https%3A//bigquant.com/community/t/topic/169658%3Futm_source%3Dzhihu%26utm_medium%3Dzhihu_answer%26utm_campaign%3D190723_758082798_zhihu_answer) ）
  - ![](https://pic2.zhimg.com/50/v2-d3b707c6c64979f4309f1227728c8ab4_hd.jpg?source=1940ef5c)
  - ![](https://pic2.zhimg.com/80/v2-d3b707c6c64979f4309f1227728c8ab4_720w.jpg?source=1940ef5c)
  - 在1的基础上，将Q-table的功能用一个深度学习网络来实现，解决了有限个state的问题。
- 3) Actor Critic （参考：[Deep-Reinforcement-Learning-in-Stock-Trading](https://link.zhihu.com/?target=https%3A//bigquant.com/community/t/topic/169658%3Futm_source%3Dzhihu%26utm_medium%3Dzhihu_answer%26utm_campaign%3D190723_758082798_zhihu_answer)）
  - ![](https://pic1.zhimg.com/50/v2-cb2603beb4737f06c371cbbe0f07d3a4_hd.jpg?source=1940ef5c)
  - ![](https://pic1.zhimg.com/80/v2-cb2603beb4737f06c371cbbe0f07d3a4_720w.jpg?source=1940ef5c)
  - 用两个模型，一个同DQN输出Q值，另一个直接输出行为。但由于两个模型参数更新相互影响，较难收敛。
- 4) DDPG（参考：[ml-stock-prediction](https://link.zhihu.com/?target=https%3A//bigquant.com/community/t/topic/169658%3Futm_source%3Dzhihu%26utm_medium%3Dzhihu_answer%26utm_campaign%3D190723_758082798_zhihu_answer)）
  - ![](https://pic1.zhimg.com/50/v2-5caa0ee24f9e5466f54cda356c241985_hd.jpg?source=1940ef5c)
  -  ![](https://pic1.zhimg.com/80/v2-5caa0ee24f9e5466f54cda356c241985_720w.jpg?source=1940ef5c)
  - 加入了不及时更新参数的模型，解决难收敛的问题
 
3\. 由于多数方法中都用到了深度神经网络，我们还需要对神经网络的模型，深度，还有其他参数进行一个选择。

4\. 比较简单的应用逻辑是对单个股票某一时间段进行择时，如果需要也可以在这个基础上进行一些调整，对某个股票池的股票进行分析，调整为一个选股策略。

## 游戏


### 俄罗斯方块

#### 经典俄罗斯方块

【2025-3-12】经典俄罗斯方块

DQN玩俄罗斯方块
- Tensorflow 代码: 
  - 【2019】 [Tetris-DQN](https://github.com/michiel-cox/Tetris-DQN)
  - 【2023】[DQN_tetris](https://github.com/bruce8866/DQN_tetris) 含动图、特征
- pytorch 代码
  - 【2020】[Deep Q-learning for playing Tetris](https://github.com/vietnh1009/Tetris-deep-Q-learning-pytorch/tree/master)
  - 【2021】[Tetris_DQN_PyTorch](https://github.com/treejw/Tetris_DQN_PyTorch) 韩国人, 包含奖励函数、原理、demo动图
  - 【2024】[Tetris-DQN-NEAT](https://github.com/CarlSvejstrup/Tetris-DQN-NEAT/) DQN 和 NEAT,包含多个奖励机制,
    - Neat 算法论文《Evolving Neural Networks through Augmenting Topologies》,整体框架可分为三部分：交叉、变异与适应度。

Features
- Cleared Lines
- Bumpiness (Sum of height difference between each column)
- Holes (Space with block on top of it)
- Sum of heights


Reward system 1 (NES Tetris)
- 0 lines cleared = number of soft drops
- 1 lines cleared = 40 + number of soft drops
- 2 lines cleared = 100 + number of soft drops
- 3 lines cleared = 300 + number of soft drops
- 4 lines cleared = 1200 + number of soft drops
- temination = -25

#### 二维俄罗斯方块

改进版：二维俄罗斯方块

BlockBlast reimplementation + RL agents
- GitHub：[BlockBlast-Game-AI-Agent](https://github.com/RisticDjordje/BlockBlast-Game-AI-Agent/tree/main)


依赖包

```sh
pip install pygame gymnasium stable_baselines3
```


### 雅达利（吃豆子）

DeepMind开发出过一个能在57款雅达利游戏上都超越人类玩家的智能体，背后依靠的同样是强化学习算法。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/18aa479e3b6f4d6196905e8cc3636d6d~noop.image)

### 赛车

【2022-9-7】[怎样从零开始训练一个AI车手？](https://www.toutiao.com/article/7138644640294683172)
- 一个智能体（你的猫）在与环境（有你的你家）互动的过程中，在奖励（猫条）和惩罚（咬头）机制的刺激下，逐渐学会了一套能够最大化自身收益的行为模式（安静，躺平）
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/c5cf85edc3544651833d93825813ed15~noop.image)
- 如何训练AI司机
- 借用一个道具：来自亚马逊云科技的Amazon DeepRacer。一辆看上去很概念的小车，跟真车的比例是1比18。车上安装了处理器、摄像头，甚至还可以配置激光雷达，为的就是实现自动驾驶——当然，前提就是我们先在车上部署训练好的强化学习算法。算法的训练需要在虚拟环境中进行，为此Amazon DeepRacer配套了一个管理控制台，里面包含一个3D赛车模拟器，能让人更直观地看到模型的训练效果。
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/65cd202b74434959b401da2ede132212~noop.image)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/c22635fcd5694544839c34d230c468c0~noop.image)

### 混沌球

[混沌球背后的核心技术](https://rct.ai/zh-hans/blog/the-key-technology-behind-morpheus-engine)
- [视频地址](https://rct.ai/static/images/395a257365304e399533516544b18b3c.mp4)

<video width="620" height="440" controls="controls" autoplay="autoplay">
  <source src="https://rct.ai/static/images/395a257365304e399533516544b18b3c.mp4" type="video/mp4" />
</video>

<iframe src="https://rct.ai/static/images/395a257365304e399533516544b18b3c.mp4&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" height="600" width="100%"> </iframe>

混沌球算法提升游戏交互体验
- 传统的叙事，无论是单线的故事，还是现在几乎所有的所谓 “交互式电影”，都仍然是基于 “**事件**” 作为叙事的基本单元，也就是什么事情发生了，然后什么事情发生了。传统的交互式数字娱乐内容，无非是让用户可以自由的从给定的两到三个选项中，选择不同的接下来会发生的事件，整个叙事仍然是基于预先定义好的路径来往前推进的。
- 而混沌球与传统的叙事方式完全不同，我们将 “事件” 替换为一个又一个明确定义了入口和出口的**黑盒**，在每一个切片的混沌球里，开始和结局（一个或者多个）是确定的，但是玩家每一次如何从开始到达结局，则是**混沌**的，是路径不明确的。这个路径只有当玩家不断的和虚拟世界里的虚拟人物 NPC 作出交互，这些 NPC 根据深度强化学习训练后的模型作出动态且实时的反应来推动剧情发展之后，才会被确定下来。这也是我们为什么命名为**混沌球**算法的原因。因此，做到真正的交互式叙事的关键，在于将叙事的中心，从故事本身，转移到故事里的所有可能参与者身上，由所有可能参与者的逻辑来共同推动和串联不同的剧情可能性。
- ![](https://rct.ai/static/images/88e5ceea1dd64e12803b3e411adf6e23.png)

仿真引擎工作方式
- ![](https://rct.ai/static/images/af5afdef214a4fe18d1a96f1dfea50b7.png)

### 公园散步

机器人的公园漫步
- 并非是在实验室的模拟环境，而是在真实的室内外地形中，作者采用强化学习和机器人控制器相结合的方法，在短短20分钟内成功让机器人学会四足行走
- [项目地址](https://github.com/ikostrikov/walk_in_the_park)
- [论文地址](https://arxiv.org/abs/2208.07860)
- [A Walk in the Park: Learning to Walk in 20 Minutes With Model-Free Reinforcement Learning](https://sites.google.com/berkeley.edu/walk-in-the-park)，含机器狗的演示[视频](https://www.youtube.com/embed/YO1USfn6sHY)
- <iframe width="560" height="315" src="https://www.youtube.com/embed/YO1USfn6sHY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


### 围棋


待定



# 结束


