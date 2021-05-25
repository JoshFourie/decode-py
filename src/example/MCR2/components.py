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

CompressionMatrixType: TypeAlias = Tensor


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
        
        I: Tensor = eye(d)

        alpha: float = d / (m*epsilon)

        return alpha * (I + alpha * input@input.T).inverse()


class CompressionMatrixFactory:
    '''
    Class that can make a `CompressionMatrixType`.
    '''

    @classmethod
    def make_compression_matrix(cls, input: Tensor, memberships: Tensor, epsilon: int) -> CompressionMatrixType:
        '''
        Makes a `CompressionMatrixType` from `input`, `memberships` and `epsilon`.
        '''
        d, m = input.shape
        
        I: Tensor = eye(d)
        alpha: float = d / (m*epsilon)

        return alpha * (I + alpha * input@memberships@input.T).inverse()
