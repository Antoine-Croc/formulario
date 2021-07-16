$(document).ready(function() {
    document.getElementById('hulp').innerText = getUrlVars().replaceAll(';', ':')
        //document.getElementById('hulp').innerText = "12:34:56"
})


function getUrlVars() {
    var vars = window.location.href.split('=').pop();
    return vars;
}