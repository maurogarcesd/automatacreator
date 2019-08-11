from automaton.dfa import DFA
from automaton.utils import common


class ENFA:
    def __init__(self, symbols: set, states: set, initial_state: str,
                 final_state: str, transitions: dict):
        self.symbols = symbols
        self.states = states
        self.initial_state = initial_state
        self.final_state = final_state
        self.transitions = transitions

    def enfa_to_dfa(self):
        closure = self.get_epsilon_closure()

        dfa_symbols = list(self.symbols)
        dfa_transitions = dict()
        dfa_initial_state = '_'.join(closure.get(self.initial_state))

        print(f'initial state ==> {dfa_initial_state}')

        if 'e' in dfa_symbols:
            dfa_symbols.remove('e')

        stack_states = [dfa_initial_state]
        states_checked = []
        while stack_states:
            actual_state = stack_states.pop()
            states_checked.append(actual_state)

            dfa_transition = dict()
            print(f'actual state ==> {actual_state}')
            for symbol in dfa_symbols:
                target = self.build_target(symbol, actual_state, closure)
                dfa_transition.update({symbol: target})

                if target not in states_checked:
                    stack_states.append(target)

            dfa_transitions.update({actual_state: dfa_transition})

        dfa_final_states = []
        for dfa_state in dfa_transitions.keys():
            if self.final_state in dfa_state:
                dfa_final_states.append(dfa_state)

        return DFA(set(dfa_symbols), set(dfa_transitions.keys()),
                   dfa_initial_state, set(dfa_final_states), dfa_transitions)

    def get_epsilon_closure(self):
        epsilon_closures = dict()
        states_to_check = list(self.states)
        states_to_check.remove(self.final_state)

        epsilon_closures.update({self.final_state: [self.final_state]})

        for state in states_to_check:
            array_closure = self.build_epsilon_closure(state)
            epsilon_closures.update({state: array_closure})

        return epsilon_closures

    def build_epsilon_closure(self, state):
        array_states = list()
        stack_states = list([state])

        while stack_states:
            actual_state = stack_states.pop()
            array_states.append(actual_state)

            if actual_state == self.final_state:
                continue
            else:
                transition = self.transitions.get(actual_state)
                items = tuple(transition.items())
                symbol, target_state = items[0][0], items[0][1]
                if symbol is 'e' and ',' in target_state:
                    state_one, state_two = target_state.split(',')
                    stack_states.append(state_one)
                    stack_states.append(state_two)
                elif symbol is 'e' and ',' not in target_state:
                    stack_states.append(target_state)
                    array_states.append(target_state)
                else:
                    array_states.append(state)

        return list(set(array_states))

    def build_target(self, symbol: str, array_state: str, closure: dict):
        target = 'e'
        for state in array_state.split('_'):
            if state is not 'e':
                try:
                    response = self.transitions.get(state).get(symbol)
                    if response:
                        target = response
                        break
                except Exception as e:
                    print(f'{state}, {symbol} not exists: {e}')

        dfa_state = '_'.join(closure.get(target)) if target is not 'e' else 'e'

        return dfa_state

    @staticmethod
    def regex_to_dfa(regex: str):
        automaton = ENFA.regex_to_enfa(regex)
        return automaton.enfa_to_dfa()

    @staticmethod
    def regex_to_enfa(regular_expression: str):
        regular_expression = common.insert_dot_operator(regular_expression)
        postfix = common.to_postfix(regular_expression)

        return ENFA.postfix_to_enfa(postfix)

    @staticmethod
    def postfix_to_enfa(postfix: str):
        if postfix is '':
            return ENFA.basic_epsilon('0')

        stack = []
        for token in postfix:
            if token is '*':
                stack.append(ENFA.build_star_closure(stack.pop()))
            elif token is '+':
                stack.append(ENFA.build_plus_closure(stack.pop()))
            elif token is '|':
                right = stack.pop()
                left = stack.pop()
                stack.append(ENFA.build_union(left, right))
            elif token is '.':
                right = stack.pop()
                left = stack.pop()
                stack.append(ENFA.build_concatenation(left, right))
            else:
                state = ENFA.get_max_state(stack[-1].states) if stack else '0'
                stack.append(ENFA.basic_symbol(state, token))

        return stack.pop()

    @staticmethod
    def basic_epsilon(max_state: str):
        print(f'Building basic epsilon')
        initial_state, final_state = ENFA.get_initial_final_states(max_state)

        symbols = {'e'}
        states = {initial_state, final_state}
        transitions = {initial_state: {'e': final_state}}

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def basic_symbol(max_state: str, symbol: str):
        print(f'Building basic symbol for {symbol}')
        initial_state, final_state = ENFA.get_initial_final_states(max_state)

        symbols = {symbol}
        states = {initial_state, final_state}
        transitions = {initial_state: {symbol: final_state}}

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def build_concatenation(first_enfa, second_enfa):
        print(f'Building concatenation between {first_enfa.__dict__} and '
              f'{second_enfa.__dict__}')
        symbols = first_enfa.symbols.union(second_enfa.symbols)
        states = first_enfa.states.union(second_enfa.states)
        initial_state = first_enfa.initial_state
        final_state = second_enfa.final_state

        transitions = dict()
        transitions.update(first_enfa.transitions)
        transitions.update(second_enfa.transitions)
        transitions.update({first_enfa.final_state: {
            'e': second_enfa.initial_state
        }})

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def build_union(first_enfa, second_enfa):
        print(f'Building union between {first_enfa.__dict__} and '
              f'{second_enfa.__dict__}')
        max_state = ENFA.get_max_state(first_enfa.states, second_enfa.states)
        initial_state, final_state = ENFA.get_initial_final_states(max_state)

        symbols = {'e'}.union(first_enfa.symbols.union(second_enfa.symbols))
        states = {initial_state, final_state}.union(
            first_enfa.states.union(second_enfa.states))

        transitions = dict()
        transitions.update(first_enfa.transitions)
        transitions.update(second_enfa.transitions)
        transitions.update({first_enfa.final_state: {'e': final_state}})
        transitions.update({second_enfa.final_state: {'e': final_state}})
        transitions.update({initial_state: {
            'e': f'{first_enfa.initial_state},{second_enfa.initial_state}'
        }})

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def build_star_closure(enfa):
        print(f'Building star closure for {enfa.__dict__}')
        max_state = ENFA.get_max_state(enfa.states)
        initial_state, final_state = ENFA.get_initial_final_states(max_state)

        symbols = {'e'}.union(enfa.symbols)
        states = {initial_state, final_state}.union(enfa.states)

        transitions = dict()
        transitions.update(enfa.transitions)
        transitions.update({initial_state: {
            'e': f'{enfa.initial_state},{final_state}'
        }})
        transitions.update({enfa.final_state: {
            'e': f'{enfa.initial_state},{final_state}'
        }})

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def build_plus_closure(enfa):
        print(f'Building plus closure for {enfa.__dict__}')
        max_state = ENFA.get_max_state(enfa.states)
        initial_state, final_state = ENFA.get_initial_final_states(max_state)

        symbols = {'e'}.union(enfa.symbols)
        states = {initial_state, final_state}.union(enfa.states)

        transitions = dict()
        transitions.update(enfa.transitions)
        transitions.update({initial_state: {'e': enfa.initial_state}})
        transitions.update({enfa.final_state: {
            'e': f'{enfa.initial_state},{final_state}'
        }})

        enfa = ENFA(symbols, states, initial_state, final_state, transitions)
        print(f'Result {enfa.__dict__} \n\n')
        return enfa

    @staticmethod
    def get_max_state(first_enfa_states: set, second_enfa_states=None):
        if second_enfa_states is not None:
            states = first_enfa_states.union(second_enfa_states)
        else:
            states = first_enfa_states

        number_states = [int(i) for i in states]
        return str(max(number_states))

    @staticmethod
    def get_initial_final_states(max_state: str):
        initial_state = f'{int(max_state) + 1}'
        final_state = f'{int(max_state) + 2}'

        return initial_state, final_state


if __name__ == '__main__':
    text = 'ABC*CD*(A|B)'
    dfa = ENFA.regex_to_dfa(text)
    print(dfa.__dict__)
