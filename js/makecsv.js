$(document).ready(function() {
    $('#start').change(function() {
        getStartDate();
    })
    $('#end').change(function() {
        getEndDate();
    })
    $('#download-btn').click(function() {
        if (verifyParams() == true) {
            makeCsvFile();
            download("Rellenar.csv", csvtoload);
        }
    })
});
//---------------------------------------------------
var d1 = null;
var d2 = null;
var csvArray = [];
var csvtoload = "";
//---------------------------------------------------

function getStartDate() {
    d1 = new Date(document.getElementById('start').value);
    d1.setHours(0);
}

function getEndDate() {
    d2 = new Date(document.getElementById('end').value);
    d2.setHours(0);
}

function checkDates() { //verify neither date is null
    if (d1 == null || d2 == null) {
        return false;
    } else {
        return true;
    }
}

function validDates() { //verify start/end dates make sense
    let wrongdate = false;
    if (d1.getYear() > d2.getYear()) {
        wrongdate = true;
    } else if (d1.getYear() == d2.getYear()) {
        if (d1.getMonth() > d2.getMonth()) {
            wrongdate = true;
        } else if (d1.getMonth() == d2.getMonth()) {
            if (d1.getDate() > d2.getDate()) {
                wrongdate = true;
            }
        }
    }
    return wrongdate;
}

function verifyParams() {
    if ($('#radioHorario').is(':checked') == $('#radioCuarto').is(':checked')) { //verify radio button is not unchecked
        alert('Elijir un tipo de horario') //traducir
        return false;
    }
    if (checkDates()) {
        if (validDates()) {
            alert('La fecha de fin no puede ser anterior a la del inicio')
            return false;
        }
    } else { //missing date(s) case
        alert('Averiguar que las dos fechas estan puestas')
        return false;
    }
    return true
}

function makeCsvFile() {
    csvArray = []; //reset global values
    csvtoload = "";
    if ($('#radioHorario').is(':checked')) { // create horario csv array
        csvArray.push(["Fecha", "Hora", "Consumo Activa"]);
        while (d1.toLocaleDateString() != d2.toLocaleDateString()) { //create rows for day.start to day.end-1
            csvArray.push([d1.toLocaleDateString(), d1.getHours(), ]);
            d1.setHours(d1.getHours() + 1);
        }
        for (let i = 0; i < 24; i++) { //create rows for day.end
            csvArray.push([d2.toLocaleDateString(), i, ]);
        }

    }
    if ($('#radioCuarto').is(':checked')) { // create 1/4 horario csv array
        csvArray.push(["Fecha", "Hora", "Cuarto", "Consumo Activa"]);
        while (d1.toLocaleDateString() != d2.toLocaleDateString()) { //create rows for day.start to day.end-1
            for (let h = 1; h < 5; h++) { // Create 4 rows/h
                csvArray.push([d1.toLocaleDateString(), d1.getHours(), h, ]);
            }
            d1.setHours(d1.getHours() + 1);
        }
        for (let i = 0; i < 24; i++) { //create rows for day.end
            for (let h = 1; h < 5; h++) { // Create 4 rows/h
                csvArray.push([d2.toLocaleDateString(), i, h, ]);
            }
        }
    }

    for (let j = 0; j < csvArray.length; j++) { // create string chain of array content
        for (let k = 0; k < csvArray[j].length; k++) {
            if (k != 0) {
                csvtoload = csvtoload + ';'
            }
            csvtoload = csvtoload + csvArray[j][k].toString()
        }
        csvtoload = csvtoload + '\n';
    }

}

function download(filename, text) { // https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
    var element = document.createElement('a');
    element.setAttribute('href', 'data:csv/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}