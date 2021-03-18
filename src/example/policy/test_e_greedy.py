from torch import Tensor, nn

from .e_greedy import eGreedy

import torch

class DummyCNN(nn.Module):

    def __init__(self):
        '''
        A dummy convolutional neural network for testing.
        '''
        super().__init__()

        self.passed = False

    def forward(self, state: Tensor) -> Tensor: 
        '''
        Changes self.passed to True and returns [0, 1, 2, 3, 4, 5].
        '''
        self.passed = True
        return torch.tensor([0., 0., 0., 0., 0., 100.])
        

def test_egreedy() -> None:
    '''
    Tests the preds arm of the annealing e-greedy policy.
    '''
    policy = eGreedy(actions=6)

    state: Tensor = torch.randn((3, 320, 210))
    cnn = DummyCNN()

    try: 
        action: int = policy.sample(state, cnn).expect('failed to sample an action')
        
        assert action == 5
        assert cnn.passed, 'policy did not call dummy network'
    
    except Exception as error: raise error
    
    