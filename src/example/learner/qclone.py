from torch import nn, optim, Tensor

from ..experience.replay import Observation

class Learner: 
    '''
    Class that manages a learning routing.
    '''
    net: nn.Module

    def __init__(self, net: nn.Module) -> None:
        '''
        Inits an SGD optimiser and MSELoss.
        '''
        self.net = net

        self.optim = optim.SGD(self.net.parameters(), lr=0.01)
        
        self.loss = nn.MSELoss()

        
    def epoch(self, batch: Observation) -> None:
        '''
        Updates the online network with better predictions.
        '''
        preds = self.predict(batch.next_state)

        loss = self.loss(preds, batch.reward)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

    def predict(self, state: Tensor) -> Tensor: 
        '''
        Returns a prediction for this state.
        '''
        return self.net(state)
