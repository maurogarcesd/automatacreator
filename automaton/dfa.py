from automaton.exceptions.exception import AutomatonException


class DFA(object):
    def __init__(self, symbols: set, states: set, initial_state: str,
                 final_states: set, transitions: dict):
        self.symbols = symbols
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

        self.validate_dfa()

    def validate_dfa(self) -> None:
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
        for state, transition in self.transitions.items():
            self.check_transition_symbols(transition)
            self.check_transition_target_states(transition)

    def check_transition_symbols(self, transition: dict) -> None:
        for symbol in transition.keys():
            if symbol not in self.symbols:
                raise AutomatonException(
                    f'check_transition_symbols ==> '
                    f'{symbol} es un símbolo inválido'
                )

    def check_transition_target_states(self, transition: dict) -> None:
        for target_state in transition.values():
            if target_state not in self.states:
                raise AutomatonException(
                    f'check_transition_target_states ==> '
                    f'{target_state} es un estado inválido'
                )

    def minify(self) -> None:
        self.delete_strange_states()
        self.delete_equivalents_states()

    def delete_strange_states(self) -> None:
        valid_states = set()
        states_stack = []
        states_checked = []

        states_stack.append(self.initial_state)
        while states_stack:
            state = states_stack.pop()
            transition = self.transitions[state]

            for symbol, target_state in transition.items():
                if target_state not in states_checked:
                    states_stack.append(target_state)

            states_checked.append(state)
            valid_states.add(state)

        self.states = valid_states
        original_states = list(self.transitions.keys())

        for state in original_states:
            if state not in self.states:
                del self.transitions[state]

    def delete_equivalents_states(self):
        pass

    def make_transition(self, state: str, symbol: str) -> str:
        transition = self.transitions.get(state)
        return transition.get(symbol)

    def check_expression(self, expression: str) -> bool:
        state = self.initial_state
        for item in expression:
            state = self.make_transition(state, item)
            print(state, " ==> ", item)
        return state in self.final_states


if __name__ == '__main__':
    from automaton.examples.dfa import strange_states as example

    automaton = DFA(
        example.get('symbols'),
        example.get('states'),
        example.get('initial_state'),
        example.get('final_states'),
        example.get('transitions')
    )

    automaton.minify()
    print(automaton.transitions)
