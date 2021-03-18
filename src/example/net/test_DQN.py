from .DQN import CNN

import torch
from torch import Tensor

def test_preprocess(file: str = 'src/example/net/test_tensor.pt') -> None:
    '''
    Tests that CNN can preprocess torchvision into a 3-channel tensor.
    '''
    rgb_array: Tensor = torch.load(file)

    assert rgb_array.shape == torch.Size([210, 160, 3]), 'expected tensor from four Pong-v0-like arrays'
    
    cnn = CNN(width=160, height=210, outputs=6, set_preprocessor = True)

    processed: Tensor = cnn.preprocess(rgb_array).expect('failed to preprocess rgb_array')

    assert processed.shape == torch.Size([3, 160, 210])
    
    dummy_batch = torch.stack([processed])

    try: cnn(dummy_batch)
    
    except Exception as e: raise ValueError(e, 'cnn failed to forward pass the dummy batch')
