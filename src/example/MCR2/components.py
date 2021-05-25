'''
Components for the MCR2 example.
'''

import sys; sys.path.append('../')  # silly hack to get the zalia package

# built-in imports
from typing_extensions import TypeAlias

# external imports
from torch import Tensor, eye, zeros


'''
Basic Components.
'''

ExpansionMatrixType: TypeAlias = Tensor

CompressionMatrixType: TypeAlias = Tensor

ClassMembershipType: TypeAlias = Tensor

StackedClassMembershipType: TypeAlias = Tensor

FeatureMatrixType: TypeAlias = Tensor

EpsilonHyperParameterType: TypeAlias = float

MaximumCodingRateType: TypeAlias = float


class ExpansionMatrixFactory:
    '''
    Class that can make an `ExpansionMatrixType`.
    '''

    @classmethod
    def make_expansion_matrix(cls, input: FeatureMatrixType, epsilon: EpsilonHyperParameterType) -> ExpansionMatrixType:
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
    def make_compression_matrix(cls, input: FeatureMatrixType, membership: ClassMembershipType, epsilon: EpsilonHyperParameterType) -> CompressionMatrixType:
        '''
        Makes a `CompressionMatrixType` from `input`, `memberships` and `epsilon`.
        '''
        d, m = input.shape
        
        I: Tensor = eye(d)
        alpha: float = d / (m*epsilon)

        return alpha * (I + alpha * input@membership@input.T).inverse()


class CompressionStrategy:
    '''
    Strategy that can use a `StackedClassMembershipType` to compress the coding rate of a `FeatureMatrixType` instance.
    '''

    @classmethod
    def apply_compression_strategy(cls, input: FeatureMatrixType, memberships: StackedClassMembershipType, epsilon: EpsilonHyperParameterType) -> FeatureMatrixType:
        '''
        Applies a compression strategy to compute the coding rate of the `input` using a `CompressionMatrixType` for each class in this `memberships` instance.
        ''' 
        d, m = input.shape
  
        compression: Tensor = zeros(d, m)
        
        membership: ClassMembershipType  # type declaration

        for membership in memberships:

            compression_matrix = CompressionMatrixFactory.make_compression_matrix(input = input, membership = membership, epsilon = epsilon)
            
            trace: Tensor = membership.trace() + 1e-8
            gamma: Tensor = trace / m

            compression += gamma * compression_matrix@input@membership
        
        return compression


class MaximumCodingRateStrategy:
    '''
    Class that can transform a `FeatureMatrixType` to increase the difference between the mixed and simple coding rates of the distribution.
    '''

    @classmethod
    def apply_coding_rate_strategy(cls, input: FeatureMatrixType, memberships: ClassMembershipType, epsilon: EpsilonHyperParameterType) -> FeatureMatrixType:
        '''
        Applies a coding rate strategy to transform the `input` into a distribution with a better coding rate.
        '''
        expansion_matrix = ExpansionMatrixFactory.make_expansion_matrix(input = input, epsilon = epsilon)

        expanded_features = expansion_matrix@input

        compressed_features = CompressionStrategy.apply_compression_strategy(input = input, memberships = memberships, epsilon = epsilon)

        return input + (expanded_features - compressed_features) 

