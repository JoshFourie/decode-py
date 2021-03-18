from .replay import ReplayMemory, ReplayMemoryError, Observation

import torch
from torch import Tensor

from result import Ok, Err, Result
from enum import Enum

class ReplayMemoryField(Enum):
    State = 1
    Action = 2
    NextState = 3
    Reward = 4

def get_prefilled(state_dim: torch.Size, action_dim: torch.Size, next_state_dim: torch.Size, reward_dim: torch.Size) -> Observation:
    state: Tensor = torch.zeros(state_dim) + ReplayMemoryField.State.value
    action: Tensor = torch.zeros(action_dim) + ReplayMemoryField.Action.value
    next_state: Tensor = torch.zeros(next_state_dim) + ReplayMemoryField.NextState.value
    reward: Tensor = torch.zeros(reward_dim) + ReplayMemoryField.Reward.value

    return Observation(state, action, next_state, reward)

def get_memory(capacity: int, prefilled: int, 
                state_dim: torch.Size, action_dim: torch.Size, 
                next_state_dim: torch.Size, reward_dim: torch.Size) -> Result[ReplayMemory, ReplayMemoryError]:
    '''
    Returns a ReplayMemory object or an error on failure. 
    '''
    memory = ReplayMemory(capacity)

    for _ in range(prefilled): 
        # push a dummy obervation onto the memory stack
        state, action, next_state, reward = get_prefilled(state_dim, action_dim, next_state_dim, reward_dim)
        
        dummy_observation = Observation(state, action, next_state, reward)
        
        if memory.push(dummy_observation).is_err(): return Err(ReplayMemoryError.IndexError)

    return Ok(memory)

def test_batch() -> None:
    '''
    Test that ReplayMemory can return a batched Observation.
    '''
    # test config
    batch_size = 5
    actions_n = 6
    features = 10
    
    # test set-up
    state_dim = torch.Size([features, features])
    expected_state_dim = torch.Size([batch_size, features, features])
    
    action_dim = torch.Size([actions_n])
    expected_action_dim = torch.Size([batch_size, actions_n])
    
    next_state_dim = torch.Size([features, features])
    expected_next_state_dim = torch.Size([batch_size, features, features])

    reward_dim = torch.Size([actions_n])
    expected_reward_dim = torch.Size([batch_size, actions_n])
    
    expected_states = torch.zeros(expected_state_dim) + ReplayMemoryField.State.value
    expected_actions = torch.zeros(expected_action_dim) + ReplayMemoryField.Action.value
    expected_next_states = torch.zeros(expected_next_state_dim) + ReplayMemoryField.NextState.value
    expected_rewards = torch.zeros(expected_reward_dim) + ReplayMemoryField.Reward.value

    # test targets
    memory = get_memory(10, 10, state_dim, action_dim, next_state_dim, reward_dim).expect('failed to get ReplayMemory instance')
    batch = memory.sample_batch(batch_size).expect('failed to get batch of observations from memory instance')
  
    # test assertions
    assert (expected_states == batch.state).float().mean() == 1, 'batch.state returned incorrectly'
    assert (expected_actions == batch.action).float().mean() == 1, 'batch.action returned incorrectly'
    assert (expected_next_states == batch.next_state).float().mean() == 1, 'batch.next_state returned incorrectly'
    assert (expected_rewards == batch.reward).float().mean() == 1, 'batch.reward returned incorrectly'
