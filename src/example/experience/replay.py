import torch
from torch import Tensor

import random

from typing import List, NamedTuple
from result import Ok, Err, Result
from enum import Enum


class Observation(NamedTuple):
    '''
    Class that manages observations in an environment.
    '''

    state: Tensor
    action: Tensor
    next_state: Tensor
    reward: Tensor


class ReplayMemoryError(Enum):
    '''
    Class that manages errors in a ReplayMemory instance.
    '''
    SampleSizeTooLarge = 0
    IndexError = 1


class ReplayMemory:
    '''
    Class for managing experience replay buffers in the DQN.
    '''

    capacity: int
    memory: List[Observation]
    position: int

    def __init__(self, capacity: int):
        '''
        Object for storing experience replays in DQN.
        '''
        self.capacity = capacity
        self.memory = list()
        self.position = 0

    def push(self, observation: Observation) -> Result[None, ReplayMemoryError]:
        '''
        Saves an experience into the buffer.
        '''
        if len(self.memory) < self.capacity: self.memory.append(observation)
        else: 
            try:
                self.memory[self.position] = observation
            except:
                return Err(ReplayMemoryError.IndexError)

        self.position += 1; self.position %= self.capacity

        return Ok(None)

    def __sample__(self, sample_size: int) -> Result[List[Observation], ReplayMemoryError]: 
        '''
        Randomly samples the experience replay buffer.
        '''
        if len(self) < sample_size:
            return Err(ReplayMemoryError.SampleSizeTooLarge)
        else:
            try: return Ok(random.sample(self.memory, sample_size)); 
            except Exception as error: raise error

    def __len__(self) -> int: return len(self.memory)
    
    def sample_batch(self, size: int) -> Result[Observation, ReplayMemoryError]:
        '''
        Returns an Observation from a randomly sampled batch of observations.
        '''
        samples = self.__sample__(size).unwrap()

        states: List[Tensor] = list()
        actions: List[Tensor] = list()
        next_states: List[Tensor] = list()
        rewards: List[Tensor] = list()

        for sample in samples:
            states.append(sample.state)
            actions.append(sample.action)
            next_states.append(sample.next_state)
            rewards.append(sample.reward)

        batch = Observation(state=torch.stack(states),
                            action=torch.stack(actions),
                            next_state=torch.stack(next_states),
                            reward=torch.stack(rewards))
        
        return Ok(batch)
            

