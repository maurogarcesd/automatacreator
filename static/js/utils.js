function generateAutomatonInfo(automaton) {
    let automatonInfo = `
        <b>Estados: </b> ${automaton.states.join(', ')} <br>
        <b>Símbolos: </b> ${automaton.symbols.join(', ')} <br>
        <b>Inicial: </b> ${automaton.initial} <br>
        <b>Finales: </b> ${automaton.final.join(', ')} <br>`;

    automatonInfo += `<b>Transiciones: </b><br>`;
    automaton.transitions.forEach((transition) => {
        automatonInfo += `&nbsp&nbsp&nbsp&nbsp&nbsp${transition.state} con ${transition.symbol} => ${transition.target} <br>`
    });

    return automatonInfo;
}

function generateRegexInfo(regex) {
    return `<b>Expresión: </b> ${regex.regex}`;
}


function buildGraph(automatonJson) {
    let container = document.getElementById("graphAutomatonContainer");
    let graphAutomatonContainer = $("#graphAutomatonContainer");
    let automatonSolutionResponse = $("#automatonSolutionResponse");

    let nodes = populateNodes(automatonJson);
    let edges = populateEdges(automatonJson);

    graphAutomatonContainer.height(automatonSolutionResponse.height() - 30);
    graphAutomatonContainer.width(automatonSolutionResponse.width() - 30);

    let network = new vis.Network(container, {nodes: nodes, edges: edges}, {});
}

function populateNodes(automatonJson) {
    let nodes = [];
    let initial = automatonJson.initial;

    automatonJson.final.forEach((final) => {
        if (final === initial) {
            nodes.push({id: initial, label: initial, color: "#2196f3"});
            initial = undefined;
        } else {
            nodes.push({id: final, label: final, color: "#a5d6a7"});
        }
        automatonJson.states.splice(automatonJson.states.indexOf(final), 1);
    });

    if (initial !== undefined) {
        nodes.push({id: initial, label: initial, color: "#90caf9"});
    }
    automatonJson.states.splice(automatonJson.states.indexOf(initial), 1);

    automatonJson.states.forEach(state => {
        if (state === "e") {
            nodes.push({id: state, label: state, color: "#ef9a9a"});
        } else {
            nodes.push({id: state, label: state, color: "#b39ddb"});
        }
    });

    return nodes;
}

function populateEdges(automatonJson) {
    let edges = [];
    automatonJson.transitions.forEach(value => {
        edges.push({
            from: value["state"],
            to: value["target"],
            arrows: "to",
            label: value["symbol"]
        })
    });

    return edges;
}


function buildJsonText(automaton) {
    let detailTransitions = '';
    automaton.transitions.forEach(value => {
        detailTransitions += `<tr>
                            <td>${value.state}</td>
                            <td>${value.symbol}</td>
                            <td>${value.target}</td>
                        </tr>`
    });

    $("#detailAutomatonStates").html(`<b>Estados: </b> ${automaton.states.join(', ')}`);
    $("#detailAutomatonSymbols").html(`<b>Símbolos: </b> ${automaton.symbols.join(', ')}`);
    $("#detailAutomatonInitial").html(`<b>Inicial: </b> ${automaton.initial}`);
    $("#detailAutomatonFinal").html(`<b>Finales: </b> ${automaton.final.join(', ')}`);
    $("#detailAutomatonTransitions").html(detailTransitions);
}

function buildPythonScript(automaton) {
    console.log(automaton);
    let pythonScript = generatePythonTemplate(automaton);
    localStorage.setItem("script", pythonScript);
    $("#codeAutomaton").html(`<code >${pythonScript}</code>`)
}

function generatePythonTemplate(automaton) {
    return `${automaton}` +
        '\n\n' +
        'def check_expression(automaton, expression: str) -> bool:\n' +
        '    state = automaton.get(\'initial_state\')\n' +
        '    for item in expression.upper():\n' +
        '        if item not in automaton.get(\'symbols\'):\n' +
        '            return False\n' +
        '        transition = automaton.get(\'transitions\').get(state)\n' +
        '        state = transition.get(item)\n' +
        '    return state in automaton.get(\'final_states\')\n' +
        '\n\n' +
        'string = input(\'Ingrese la cadena >> \')\n' +
        'print(check_expression(automaton_test, string))'
}

function downloadScript() {
    let script = localStorage.getItem("script");
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(script));
    element.setAttribute('download', 'automaton.py');

    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/**
 * show toast message when something goes bad
 * @param message
 */
function failMessage(message) {
    M.toast({html: message, classes: "fail-message"});
}

/**
 * show toast message when something goes fine
 * @param message
 */
function successMessage(message) {
    M.toast({html: message, classes: "success-message"});
}
