'''
Plays the Atari Pong game with some existing blocks.
'''

import sys

from typing_extensions import TypeAlias; sys.path.append('../')  # silly hack to get the zalia package

import gym

from torch import Tensor

from src.rl.blocks import ReplayMemoryBlock, OpenAI_ObservationBlock

import streamlit as st


Observation: TypeAlias = OpenAI_ObservationBlock[Tensor, Tensor, Tensor, Tensor]
Memory: TypeAlias = ReplayMemoryBlock[Observation]

try:
    env = gym.make('Atlantis-ram-v0')

    state = env.reset()

    memory = Memory(engine = Memory.make.new(capacity = 1000).unwrap())


    observation_display = st.empty()
    memory_display = st.empty()

    memory.display(parent = memory_display, children = None).unwrap()

    done: bool = False
    while not done:
        env.render()

        action = env.action_space.sample()
        next_state, reward, done, info = env.step(action)

        observation = Observation(Observation.make.new(
            state = state,
            transition = next_state,
            reward = reward,
            action = action
        ).unwrap())

        observation.display(parent = observation_display, children = None).unwrap()

        memory.engine().unwrap().push(observation, overwrite = True).unwrap()
        memory.update(parent = memory_display, children = None).unwrap()

finally: env.close()