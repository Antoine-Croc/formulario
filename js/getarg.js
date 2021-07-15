$(document).ready(function() {
    document.getElementById('hulp').innerText = getUrlVars().replaceAll(';', ':')
})


function getUrlVars() {
    var vars = window.location.href.split('=').pop();
    return vars;
}