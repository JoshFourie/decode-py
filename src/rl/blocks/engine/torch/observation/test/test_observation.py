'''
This test module checks the behaviour of `.torch.observation.OpenAI_Observation`.
'''

from ..engine import OpenAI_Observation, OpenAI_ObservationFactory

def test_factory() -> None:
    '''
    Tests that the factory correctly initialises the OpenAI_Observation.
    '''
    exp = OpenAI_Observation[int, int, int, int](
        state = 0, 
        reward = 1, 
        transition = 2, 
        action = 3
    )

    test = OpenAI_ObservationFactory.new(
        state = 0, 
        reward = 1, 
        transition = 2, 
        action = 3
    ).unwrap()

    assert test.state == exp.state
    assert test.reward == exp.reward
    assert test.transition == exp.transition
    assert test.action == exp.action


def test_init() -> None:
    '''
    Tests that an OpenAI_Observation inits correctly.
    '''
    observation = OpenAI_Observation[int, int, int, int](
        state = 0, 
        reward = 1, 
        transition = 2, 
        action = 3
    )

    assert observation.state == 0
    assert observation.reward == 1
    assert observation.transition == 2
    assert observation.action == 3

def test_getters() -> None:
    '''
    Tests that an OpenAI_Observation correctly gets values.
    '''
    observation = OpenAI_Observation[int, int, int, int](
        state = 0, 
        reward = 1, 
        transition = 2, 
        action = 3
    )

    assert observation.get_state().unwrap() == 0
    assert observation.get_reward().unwrap() == 1
    assert observation.get_next_state().unwrap() == 2
    assert observation.get_action().unwrap() == 3

def test_setters() -> None:
    '''
    Tests that an OpenAI_Observation correctly sets values.
    '''
    observation = OpenAI_Observation[int, int, int, int](
        state = 0, 
        reward = 1, 
        transition = 2, 
        action = 3
    )

    assert observation.get_state().unwrap() == 0
    assert observation.get_reward().unwrap() == 1
    assert observation.get_next_state().unwrap() == 2
    assert observation.get_action().unwrap() == 3

    observation.set_state_(3).unwrap()
    observation.set_reward_(2).unwrap()
    observation.set_next_state_(1).unwrap()
    observation.set_action_(0).unwrap()

    assert observation.get_state().unwrap() == 3
    assert observation.get_reward().unwrap() == 2
    assert observation.get_next_state().unwrap() == 1
    assert observation.get_action().unwrap() == 0