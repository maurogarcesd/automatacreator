from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from automaton.dfa import DFA
from automaton.enfa import ENFA
from automaton.nfa import NFA
from automaton.utils.common import check_type, check_expression
from automaton.utils.common import from_dict_to_json_format
from automaton.utils.common import from_json_to_dict
from automaton.utils.script import generate_dict_string

# from automaton import enfa

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/automaton/create', methods=['POST'])
def create_automaton():
    request_data = request.get_json()
    print(request_data)
    try:
        automaton = from_json_to_dict(request_data)
        states = automaton.get('states')
        symbols = automaton.get('symbols')
        initial = automaton.get('initial_state')
        final = automaton.get('final_states')
        transitions = automaton.get('transitions')

        if check_type(automaton) is 'nfa':
            nfa_automaton = NFA(symbols, states, initial, final, transitions)
            dfa_automaton = nfa_automaton.nfa_to_dfa()
        else:
            dfa_automaton = DFA(symbols, states, initial, final, transitions)

        dfa_automaton.minify()
        automaton_string = generate_dict_string(dfa_automaton.__dict__)
        data = from_dict_to_json_format(dfa_automaton.__dict__)

        success = True
        message = 'El Automata se ha creado con éxito'
    except Exception as error:
        success = False
        message = error
        data = {}
        automaton_string = ''
    response = jsonify({
        'success': success,
        'data': data,
        'message': message,
        'automaton': automaton_string
    })

    return response


@app.route('/regex/generate', methods=['POST'])
def generate_automaton():
    request_data = request.get_json()
    try:
        dfa_automaton = ENFA.regex_to_dfa(request_data['regex'])
        dfa_automaton.minify()
        automaton_string = generate_dict_string(dfa_automaton.__dict__)
        data = from_dict_to_json_format(dfa_automaton.__dict__)

        success = True
        message = 'El Automata se ha creado con éxito'
    except Exception as error:
        success = False
        message = error
        data = {}
        automaton_string = ''
    response = jsonify({
        'success': success,
        'data': data,
        'message': message,
        'automaton': automaton_string
    })

    return response


@app.route('/regex/match', methods=['POST'])
def match_string():
    request_data = request.get_json()

    automaton = from_json_to_dict(request_data['automaton'])
    match = check_expression(automaton, request_data['string'])

    return jsonify({'success': match})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('400.html'), 404


@app.errorhandler(500)
def exception_handler(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
