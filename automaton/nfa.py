import itertools

from automaton.dfa import DFA
from automaton.exceptions.exception import AutomatonException


class NFA(object):

    def __init__(self, symbols: set, states: set, initial_state: str,
                 acceptation_states: set, transitions: dict):
        self.symbols = symbols
        self.states = states
        self.initial_state = initial_state
        self.final_states = acceptation_states
        self.transitions = transitions

        self.validate_nfa()

    def validate_nfa(self) -> None:
        self.check_initial_state()
        self.check_acceptation_states()
        self.check_transitions()

    def check_initial_state(self) -> None:
        if self.initial_state not in self.states:
            raise AutomatonException(
                f'check_initial_state ==> '
                f'{self.initial_state} es un estado inválido'
            )

    def check_acceptation_states(self) -> None:
        for state in self.final_states:
            if state not in self.states:
                raise AutomatonException(
                    f'check_acceptation_states ==> '
                    f'{state} es un estado inválido'
                )

    def check_transitions(self) -> None:
        for state_transition in self.transitions.items():
            self.check_transition_symbols(state_transition[1])
            self.check_transition_target_states(state_transition[1])

    def check_transition_symbols(self, transition: dict) -> None:
        for symbol in transition.keys():
            if symbol not in self.symbols:
                raise AutomatonException(
                    f'check_transition_symbols ==> '
                    f'{symbol} es un símbolo inválido'
                )

    def check_transition_target_states(self, transition: dict) -> None:
        for target_state in transition.values():
            if ',' in target_state:
                target_state = target_state.replace(' ', '').split(',')

            for state in target_state:
                if state not in self.states:
                    raise AutomatonException(
                        f'check_transition_target_states ==> '
                        f'{target_state} es un estado inválido'
                    )

    def nfa_to_dfa(self) -> DFA:
        dfa_states = set()
        dfa_final_states = set()
        dfa_transitions = dict()

        states_stack = []
        states_checked = []
        states_stack.append(self.initial_state)
        while states_stack:
            actual_state = states_stack.pop()
            dfa_transition = dict()

            for symbol, state in self.transitions.get(actual_state).items():
                new_state_name = self.build_space_name(state)
                dfa_transition.update({symbol: new_state_name})

                final_state = self.get_final_state(new_state_name)
                if final_state:
                    dfa_final_states.update({final_state})

                if new_state_name not in states_checked:
                    states_stack.append(new_state_name)

                new_state_transition = self.build_state_targets(new_state_name)
                self.transitions.update({new_state_name: new_state_transition})
            dfa_transitions.update({actual_state: dfa_transition})
            states_checked.append(actual_state)

        dfa_states.update(dfa_transitions.keys())
        return DFA(self.symbols, dfa_states, self.initial_state,
                   dfa_final_states, dfa_transitions)

    def get_final_state(self, new_state_name: str):
        final_states = [i for i in new_state_name if i in self.final_states]
        return new_state_name if final_states else None

    def build_state_targets(self, new_state_name: str):
        new_state_transition = dict()
        for global_symbol in self.symbols:
            target_state = ''
            for state in new_state_name:
                target_state += self.transitions[state].get(global_symbol)
            new_state_transition.update({global_symbol: target_state})

        return new_state_transition

    @staticmethod
    def build_space_name(dirty_space_name: str):
        """
        process:
            - Get list with valid states names
            - Sort the values and build string with it
            - Delete duplicate values
        :param dirty_space_name:
        :return:
        """
        states = [i for i in dirty_space_name if i is not ' ' and i is not ',']
        states_sorted = ''.join(sorted(states))
        return ''.join(char for char, _ in itertools.groupby(states_sorted))


if __name__ == '__main__':
    from automaton.examples import odd_ones as example

    automaton = NFA(
        example.get('symbols'),
        example.get('states'),
        example.get('initial_state'),
        example.get('final_states'),
        example.get('transitions')
    )

    dfa = automaton.nfa_to_dfa()
    print(dfa.__dict__)
