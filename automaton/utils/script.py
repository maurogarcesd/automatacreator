from automaton.examples.dfa import automaton_test
from automaton.utils.common import check_expression


def generate_dict_string(automaton: dict):
    states = ', '.join([f'"{state}"' for state in automaton.get('states')])
    symbols = ', '.join([f'"{symbol}"' for symbol in automaton.get('symbols')])
    initial = f'"{automaton.get("initial_state")}"'
    final = ', '.join([f'"{final}"' for final in automaton.get('final_states')])

    transitions = ''
    for state, transition in automaton.get('transitions').items():
        transitions += f'\t\t"{state}":' + '{'
        for symbol, target in transition.items():
            transitions += f'"{symbol}": "{target}", '
        transitions = transitions[: -2]
        transitions += '}, \n'

    automaton_string = 'automaton_test = {\n'
    automaton_string += '\t"states": {' + states + '}, \n'
    automaton_string += '\t"symbols": {' + symbols + '}, \n'
    automaton_string += '\t"initial_state": ' + initial + ', \n'
    automaton_string += '\t"final_states": {' + final + '}, \n'
    automaton_string += '\t"transitions": {\n' + transitions[:-3] + '\n\t}'
    automaton_string += '\n}'

    return automaton_string


if __name__ == '__main__':
    print(check_expression(automaton_test, '00011'))
    generate_dict_string(automaton_test)
