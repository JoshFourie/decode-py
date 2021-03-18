import torch
import pytest

from torch import Tensor, nn
from result import Result, Err

from ..experience.test_replay import Observation, get_memory

from .qclone import Learner

class DummyDQN(nn.Module):
    '''
    Class that mocks up a DQN for testing an optimiser.
    '''

    def __init__(self, inputs: int, outputs: int) -> None:
        '''
        Inits a mock DQN with a single linear and activation layer.
        '''
        
        super().__init__()

        self.l1 = nn.Linear(inputs, inputs)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(inputs, outputs)

    def forward(self, inputs: Tensor) -> Tensor:
        '''
        Returns a forward pass of the dummy DQN
        '''
        return self.l2(self.relu(self.l1(inputs)))
    

# helper functions
def get_observation_batch(size: int, state_dim: torch.Size, action_dim: torch.Size) -> Result[Observation, ValueError]:
    '''
    Returns a batch of observations for testing.
    '''
    try:
        memory = get_memory(
            capacity = size, 
            prefilled = size, 
            state_dim = state_dim, 
            action_dim = action_dim,
            next_state_dim = state_dim, 
            reward_dim = action_dim
        ).expect('failed to get a memory instance')

    except Exception as error: return Err(ValueError(f'failed to get observations: {error}'))    

    return memory.sample_batch(size).map_err( lambda error: ValueError(f'failed to sample observations: {error}') )
    
def accuracy(preds: Tensor, rewards: Tensor, tolerance: float = 0.001) -> float:
    '''
    Returns accuracy of predictions and rewards with error tolerance.
    '''
    return float(preds.isclose(rewards, rtol=tolerance).float().mean().item())


# test functions
def test_step() -> None:
    '''
    Does q_clone.RMS_SmoothL1 correctly step a DQN?
    '''
    # set up config
    batch_size = 512 # try do it with a batch of two observations

    action_dim = torch.Size([212]) # there are 2 possible actions
    state_dim = torch.Size([480]) # a state is a flattened 3x3 tensor

    tolerance = 0.0001 # error tolerance 
    
    # get dummy instances
    batch = get_observation_batch(size = batch_size, state_dim = state_dim, action_dim = action_dim).expect('failed to get a batch of observations')

    test_net = DummyDQN(inputs = state_dim[0], outputs = action_dim[0])
    
    # set up a learner
    learner = Learner(net = test_net)

    # get a baseline accuracy
    preds = learner.predict(batch.next_state); baseline = accuracy(preds = preds, rewards = batch.reward, tolerance = tolerance)

    # update the online network three times
    for _ in range(9): learner.epoch(batch)

    # assert better performance
    preds = learner.predict(batch.next_state); learned = accuracy(preds = preds, rewards = batch.reward)

    assert learned > baseline, f'expected {learned} > {baseline}'