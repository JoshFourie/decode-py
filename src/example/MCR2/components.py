'''
Components for the MCR2 example.
'''

import sys; sys.path.append('../')  # silly hack to get the zalia package

# built-in imports
from typing_extensions import TypeAlias

# library imports
from src.showcase.maker.simple import SimpleMakerFacade
from src.showcase.assembler.simple import SimpleAssembler
from src.showcase.database.simple import SimpleGraphDB

# external imports
from torch import Tensor, eye


'''
Basic Components.
'''

ExpansionMatrixType: TypeAlias = Tensor

class ExpansionMatrixFactory:
    '''
    Class that can make an `ExpansionMatrixType`.
    '''

    @classmethod
    def make_expansion_matrix(cls, input: Tensor, epsilon: int) -> ExpansionMatrixType:
        '''
        Makes an `ExpansionMatrixType` from `input` and `epsilon`.
        '''
        d, m = input.shape
        
        I = eye(d)

        alpha = d / (m*epsilon)

        return alpha * (I + alpha * input@input.T).inverse()
