from typing import Any, Callable

import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor
from torchvision.transforms import Compose, ToPILImage, ToTensor, Resize

from result import Result, Ok, Err

class CNN(nn.Module):
    '''
    Convolutional Neural Net for processing a sequence of Atari-like RGB images.
    '''

    preprocessor: Callable[..., Tensor]

    def __init__(self, width: int, height: int, outputs: int, set_preprocessor: bool = False) -> None:
        '''
        Creates the layers for the CNN.
        '''
        super().__init__()

        self.conv3x16 = nn.Conv2d(3, 16, kernel_size=5, stride=2)
        self.conv16x32 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.conv32x32 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        
        self.bn16 = nn.BatchNorm2d(16)
        self.bn32 = nn.BatchNorm2d(32)

        connections = CNN.__get_connections__(width, height, kernel_size=5, stride=2, out_channel=32)
        self.head = nn.Linear(connections, outputs)

        if set_preprocessor: self.preprocessor = Compose([ToPILImage(), Resize((width, height)), ToTensor()])

    def preprocessor_exists(self) -> bool:
        '''
        Checks if the <CNN>.preprocessor callable has been set.
        '''
        return getattr(self, 'preprocessor', None) is None

    def set_preprocessor(self, preprocess: Callable[..., Tensor], overwrite: bool = False) -> Result[None, ValueError]:
        '''
        Sets the preprocessor the provided value.
        '''        
        if self.preprocessor_exists() or overwrite: self.preprocessor = preprocess; return Ok(None)
        
        else: return Err(ValueError('tried to overwrite <CNN>.preprocessor without overwrite = True'))

    def preprocess(self, inputs: Any) -> Result[Tensor, ValueError]:
        '''
        Preprocesses inputs using the preprocessor.
        '''
        if not self.preprocessor_exists(): 
            try:
                return Ok(self.preprocessor(inputs))
            except Exception as error: return Err(ValueError(error))
        else: 
            return Err(ValueError('tried to call <CNN>.preprocessor on a None value'))

    @classmethod
    def __get_connections__(cls, width: int, height: int, kernel_size: int, stride: int, out_channel: int) -> int:
        '''
        Computes the number of linear connections required to encode an image of this width and height.

        Source: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
        '''

        def connections(dimension: int) -> int: return (dimension - (kernel_size - 1) - 1) // stride + 1

        width_connections: int = connections(connections(connections(width)))
        height_connections: int = connections(connections(connections(height)))

        return width_connections * height_connections * out_channel
        
    def forward(self, input: Tensor) -> Tensor:
        '''
        Forward pass of an input through the CNN.
        '''
        input = F.relu(self.bn16(self.conv3x16(input)))
        input = F.relu(self.bn32(self.conv16x32(input)))
        input = F.relu(self.bn32(self.conv32x32(input)))

        input = input.view(input.size(0), -1)

        return self.head(input)
