################################################################################
# DFA examples
################################################################################
odd_zeros_pair_ones = {
    'symbols': {'0', '1'},
    'states': {'CPUP', 'CIUP', 'CPUI', 'CIUI'},
    'initial_state': 'CPUP',
    'final_states': {'CIUP'},
    'transitions': {
        'CPUP': {'0': 'CIUP', '1': 'CIUI'},
        'CIUP': {'0': 'CPUP', '1': 'CIUI'},
        'CPUI': {'0': 'CIUI', '1': 'CPUP'},
        'CIUI': {'0': 'CPUI', '1': 'CIUP'}
    }
}

automaton_test = {
    "states": {"B", "A"},
    "symbols": {"0", "1"},
    "initial_state": "A",
    "final_states": {"B"},
    "transitions": {
        "B": {"1": "B", "0": "B"},
        "A": {"1": "B", "0": "A"}
    }
}

strange_states = {
    'symbols': {'a', 'b'},
    'states': {'0', '1', '2', '3', '4', '5', '6', '7', '8'},
    'initial_state': '0',
    'final_states': {'1', '2', '6', '7'},
    'transitions': {
        '0': {'a': '1', 'b': '5'},
        '1': {'a': '2', 'b': '7'},
        '2': {'a': '2', 'b': '5'},
        '3': {'a': '5', 'b': '7'},
        '4': {'a': '5', 'b': '6'},
        '5': {'a': '3', 'b': '1'},
        '6': {'a': '8', 'b': '0'},
        '7': {'a': '0', 'b': '1'},
        '8': {'a': '3', 'b': '6'}
    }
}

json_format_example = {
    'states': ['a', 'b'],
    'symbols': ['0', '1'],
    'initial': 'a',
    'final': ['b'],
    'transitions': [
        {'state': 'a', 'symbol': '0', 'target': 'a'},
        {'state': 'a', 'symbol': '1', 'target': 'b'},
        {'state': 'b', 'symbol': '0', 'target': 'b'},
        {'state': 'b', 'symbol': '1', 'target': 'b'}
    ]
}
