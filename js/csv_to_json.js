const reader = new FileReader();
var csvArray = [];
var contentGood = true;
var contentRow = [];
var csvCuarto = false;
//--------------------------------------

reader.onload = function(e) { //target csv text (accessible because no encoding)
    document.querySelector('.output').innerText = e.target.result;
}

function getText() { //recuperate hidden .csv text from html page
    return document.getElementById('csvtext_use').innerText;
}

function splitcsv(txt) {
    if (txt[5] == ';') {
        return txt.split('\n').map(line => line.split(';')) //split character defined by csv input format(iso-8859 here)
    } else if (txt[5] == ',') {
        return txt.split('\n').map(line => line.split(',')) //utf-8 format
    } else {
        return false;
    }
}

validkeys = ["Fecha", "Hora", "Cuarto", "Consumo Activa"]; //define which columns you want to be sent server-side in case client modified given file

function formatCSV_JSON(txt) { //Big function that does what it's called
    csvArray = splitcsv(txt);
    if (typeof(csvArray) == "boolean") {
        if (!csvArray && !csvTested) {
            alert('Archivo csv tiene malo formato')
            return false;
        } else {
            return true; //this case happens when file is already in JSON and client clicks on the format buttons again.
        }
    }

    var Jkeys = csvArray[0]; //recuperate json keys
    var index = 0; //reset
    var removeIndex = []; //reset
    var isIn = null;
    for (const key of Jkeys) {
        isIn = false;
        for (const vkey of validkeys) { //verify if the keys of input file are required
            if (vkey == key) {
                isIn = true;
            }
        }
        if (!isIn) { //add index of unwanted column keys from highest to lowest
            removeIndex.unshift(index)
        }
        index += 1;
    }
    for (k of removeIndex) {
        Jkeys.splice(k, 0); //remove from keys unwanted column keys but from highest to smallest so not to change indexation while removing
        for (let l = 0; l < csvArray.length; l++) { //remove from every array the values of unwanted columns
            csvArray[l].splice(k, 1);
        }
    }
    fileFullcsv(csvArray); //verify all the content values of Consumo Activa
    //here we start to format the input values in JSON 
    csvCuarto = (csvArray[0].length == validkeys.length) //verify type of file by comparing file keys to all keys
    var jsonStrtot = '[';
    for (let i = 1; i < csvArray.length; i++) {
        if (csvArray[i].length == Jkeys.length) {
            var jsonStr = "";
            for (let j = 0; j < Jkeys.length; j++) {
                let ok = csvArray[i][j].replace(',', '.'); //this is due to iso-8859 csv format, may be removed if client uses american format
                if (Jkeys[j] == "Fecha") {
                    jsonStr = jsonStr + '"' + Jkeys[j] + '"' + ': "' + ok + '"';
                } else {
                    jsonStr = jsonStr + '"' + Jkeys[j] + '"' + ":" + ok;
                }
                if (j < Jkeys.length - 1) {
                    jsonStr = jsonStr + ", "
                }
            }
            jsonStrtot = jsonStrtot + "{" + jsonStr + "}";
            if (i < csvArray.length - 1) {
                if (csvArray[i + 1].length > 2)
                    jsonStrtot = jsonStrtot + ", "
            }
        }
    }
    jsonStrtot = jsonStrtot + "]";
    console.log(jsonStrtot)
    document.getElementById("csvtext_use").innerHTML = jsonStrtot;
    return true;
}

function fileFullcsv(arrayT) { // retrieve erroneous lines
    contentRow = [];
    let ind = 0;
    for (let i = 1; i < arrayT.length - 1; i++) {
        num = parseFloat(arrayT[i][arrayT[0].indexOf("Consumo Activa")])
        if (isNaN(num)) {
            contentRow.push(ind);
        } else if (num < 0) {
            contentRow.push(ind);
        }
        ind += 1;
    }
    if (contentRow.length != 0) {
        contentGood = false;
    }
}