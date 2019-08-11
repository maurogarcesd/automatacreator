$(document).ready(() => {
    let statesInput = $("#statesInput");
    let symbolsInput = $("#symbolsInput");
    let initialInput = $("#initialInput");
    let finalInput = $("#finalInput");
    let transitionStateInput = $("#transitionStateInput");
    let transitionSymbolInput = $("#transitionSymbolInput");
    let transitionTargetInput = $("#transitionTargetInput");
    let transitionsList = $("#transitionsList");
    let transitions = [];
    let btnAddTransition = $("#btnAddTransition");
    let btnCreateAutomaton = $("#btnCreateAutomaton");
    let btnClearAutomaton = $("#btnClearAutomaton");

    let regexInput = $("#regexInput");
    let btnGenerateAutomaton = $("#btnGenerateAutomaton");

    let stringInput = $("#stringInput");
    let btnMatchString = $("#btnMatchString");

    let btnDownloadScript = $("#btnDownloadScript");

    btnAddTransition.click((event) => {
        event.preventDefault();
        let state = transitionStateInput.val().toUpperCase();
        let symbol = transitionSymbolInput.val().toUpperCase();
        let target = transitionTargetInput.val().toUpperCase();
        let transitionsText = "";

        if (state !== "" && symbol !== "" && target !== "") {
            let transition = {"state": state, "symbol": symbol, "target": target};

            transitions.unshift(transition);
            transitions.forEach(value => {
                transitionsText += `<tr>
                                        <td>${value["state"]}</td>
                                        <td>${value["symbol"]}</td>
                                        <td>${value["target"]}</td>
                                    </tr>`;
            });
        } else {
            failMessage("Todos los campos son requeridos");
        }

        transitionsList.html(transitionsText);
        transitionStateInput.val("");
        transitionSymbolInput.val("");
        transitionTargetInput.val("");
    });

    btnClearAutomaton.click((event) => {
        event.preventDefault();
        clearAutomatonFormInputs();
        hideAutomatonInfo();

        transitions = [];
    });

    btnCreateAutomaton.click((event) => {
        event.preventDefault();
        showAutomatonLoader();

        let states = statesInput.val().toUpperCase().split(',');
        let symbols = symbolsInput.val().toUpperCase().split(',');
        let initial = initialInput.val().toUpperCase();
        let final = finalInput.val().toUpperCase().split(',');

        if (states.length > 0 && symbols.length > 0 && initial !== "" && final.length > 0 && transitions.length > 0) {
            let automatonData = {
                "states": states,
                "symbols": symbols,
                "initial": initial,
                "final": final,
                "transitions": transitions
            };

            showAutomatonInfo(automatonData);

            $.ajax({
                type: "POST", url: "/automaton/create", data: JSON.stringify(automatonData),
                contentType: "application/json; charset=utf-8", dataType: "json",
            }).done(function (response) {
                console.log(response);
                if (response.success) {
                    localStorage.setItem("automaton", JSON.stringify(response.data));
                    showAutomatonSolutionResponse();
                    clearAutomatonFormInputs();
                    buildGraph(response.data);
                    buildJsonText(response.data);
                    buildPythonScript(response.automaton);
                    transitions = [];
                } else {
                    showAutomatonSolutionInfo();
                    failMessage(response.message);
                }
            }).fail(function () {
                showAutomatonSolutionInfo();
                failMessage("Ha ocurrido un error, por favor revisa tu configuración o inténtalo más tarde");
            });
        } else {
            showAutomatonSolutionInfo();
            failMessage("Por favor verifica que hayas ingresado todos los campos");
        }
    });

    btnGenerateAutomaton.click((event) => {
        event.preventDefault();
        let regex = regexInput.val().toUpperCase();

        if (regex !== "") {
            let regexData = {"regex": regex};
            showRegexInfo(regexData);

            $.ajax({
                type: "POST", url: "/regex/generate", data: JSON.stringify(regexData),
                contentType: "application/json; charset=utf-8", dataType: "json",
            }).done(function (response) {
                console.log(response);
                if (response.success) {
                    localStorage.setItem("automaton", JSON.stringify(response.data));
                    showAutomatonSolutionResponse();
                    clearRegexFormInputs();
                    buildGraph(response.data);
                    buildJsonText(response.data);
                    buildPythonScript(response.automaton);
                } else {
                    showAutomatonSolutionInfo();
                    failMessage(response.message);
                }
            }).fail(function () {
                showAutomatonSolutionInfo();
                failMessage("Ha ocurrido un error, por favor revisa tu configuración o inténtalo más tarde");
            });
        } else {
            showAutomatonSolutionInfo();
            failMessage("Por favor verifica que hayas ingresado todos los campos");
        }
    });

    btnMatchString.click((event) => {
        event.preventDefault();
        let string = stringInput.val().toUpperCase();

        if (string !== "") {
            showMatchLoader();
            let automaton = JSON.parse(localStorage.getItem("automaton"));
            let data = {"string": string, "automaton": automaton};

            $.ajax({
                type: "POST", url: "/regex/match", data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8", dataType: "json",
            }).done(function (response) {
                hideMatchLoader();
                console.log(response);
                if (response.success) {
                    successMessage("La cadena coincide con el autómata");
                } else {
                    failMessage("La cadena no coincide con el autómata");
                }
            }).fail(function () {
                hideMatchLoader();
                showAutomatonSolutionInfo();
                failMessage("Ha ocurrido un error, por favor revisa tu configuración o inténtalo más tarde");
            });
        } else {
            showAutomatonSolutionInfo();
            failMessage("Por favor verifica que hayas ingresado todos los campos");
        }
    });

    btnDownloadScript.click((event) => {
        event.preventDefault();
        downloadScript();
    });
});

