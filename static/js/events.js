$(document).ready(() => {
    let automatonLink = $("#autoamatonLink");
    let aboutLink = $("#aboutLink");
    let regexLink = $("#regexLink");

    let brandText = $("#brandText");

    let automatonContainer = $("#automatonContainer");
    let aboutContainer = $("#aboutContainer");

    let automatonForm = $("#automatonForm");
    let regexForm = $("#regexForm");

    let automatonFormInfo = $("#automatonFormInfo");
    let regexFormInfo = $("#regexFormInfo");

    let btnMatcherOpener = $("#btnMatcherOpener");
    let btnMatcherCloser = $("#btnMatcherCloser");
    let matcherContainer = $("#matcherContainer");

    let loader = $("#loader");
    let automatonSolutionResponse = $("#automatonSolutionResponse");

    let graphAutomatonLink = $("#graphAutomatonLink");
    let jsonAutomatonLink = $("#jsonAutomatonLink");
    let codeAutomatonLink = $("#codeAutomatonLink");

    let graphAutomatonContainer = $("#graphAutomatonContainer");
    let detailsAutomatonContainer = $("#detailsAutomatonContainer");
    let codeAutomatonContainer = $("#codeAutomatonContainer");

    let matchLoader = $("#matchLoader");

    aboutContainer.hide(0);
    regexForm.hide(0);
    automatonSolutionResponse.hide(0);
    loader.hide(0);
    detailsAutomatonContainer.hide(0);
    codeAutomatonContainer.hide(0);
    matcherContainer.hide(0);
    matchLoader.hide(0);
    automatonFormInfo.hide(0);
    regexFormInfo.hide(0);

    automatonLink.click(() => {
        automatonContainer.show(0);
        aboutContainer.hide(0);
    });

    aboutLink.click(() => {
        automatonContainer.hide(0);
        aboutContainer.show(0);
    });

    automatonLink.click(() => {
        brandText.text("AUTÓMATAS");
        automatonForm.show(0);
        regexForm.hide(0);
    });

    regexLink.click(() => {
        brandText.text("REGEX");
        automatonContainer.show(0);
        automatonForm.hide(0);
        regexForm.show(0);
    });

    graphAutomatonLink.click(() => {
        graphAutomatonContainer.show(0);
        detailsAutomatonContainer.hide(0);
        codeAutomatonContainer.hide(0);
    });

    jsonAutomatonLink.click(() => {
        graphAutomatonContainer.hide(0);
        detailsAutomatonContainer.show(0);
        codeAutomatonContainer.hide(0);
    });

    codeAutomatonLink.click(() => {
        graphAutomatonContainer.hide(0);
        detailsAutomatonContainer.hide(0);
        codeAutomatonContainer.show(0);
    });

    btnMatcherOpener.click(() => {
        btnMatcherOpener.hide("slow");
        matcherContainer.show("slow");
    });

    btnMatcherCloser.click(() => {
        btnMatcherOpener.show("slow");
        matcherContainer.hide("slow");
    });
});

function showAutomatonSolutionInfo() {
    $("#automatonSolutionInfo").show("slow");
    $("#automatonSolutionLoader").hide("slow");
    $("#automatonSolutionResponse").hide("slow");
}

function showAutomatonLoader() {
    $("#automatonSolutionInfo").hide("slow");
    $("#automatonSolutionLoader").show("slow");
    $("#automatonSolutionResponse").hide("slow");
}

function showAutomatonSolutionResponse() {
    $("#automatonSolutionInfo").hide("slow");
    $("#automatonSolutionLoader").hide("slow");
    $("#automatonSolutionResponse").show("slow");
}

function clearAutomatonFormInputs() {
    $("#statesInput").val("");
    $("#symbolsInput").val("");
    $("#initialInput").val("");
    $("#finalInput").val("");
    $("#transitionStateInput").val("");
    $("#transitionSymbolInput").val("");
    $("#transitionTargetInput").val("");
    $("#transitionsList").html(null);
}

function clearRegexFormInputs() {
    $("#regexInput").val("");
}

function showAutomatonInfo(automaton) {
    let automatonFormInfo = $("#automatonFormInfo");
    let automatonInfo = generateAutomatonInfo(automaton);
    automatonFormInfo.html(automatonInfo);
    automatonFormInfo.show("slow");
}

function showRegexInfo(regex) {
    let regexFormInfo = $("#regexFormInfo");
    let regexInfo = generateRegexInfo(regex);
    regexFormInfo.html(regexInfo);
    regexFormInfo.show("slow");
}

function hideAutomatonInfo() {
    $("#automatonFormInfo").hide(0);
}

function hideRegexInfo() {
    $("#regexFormInfo").hide(0);
}

function clearMatchFormInputs() {
    $("#stringInput").html("");
}

function showMatchLoader() {
    $("#matchLoader").show("slow");
}

function hideMatchLoader() {
    $("#matchLoader").hide("slow");
}