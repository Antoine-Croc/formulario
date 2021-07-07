$(document).ready(function () {
    $('#File').change(function () {
        listen();
    })
    $('#test').click(function () { //put into submit later
        toSave();
        if ($('#csv').is(':checked')) {
            formatCSV_JSON(getText());
        }
        if ($('#xlsx').is(':checked')) {
            makexlsxJSON();
        }
    })
    $('#csv').change(function () {
        let val = verifyFormat();
        $(this).prop('checked', val);
    })
    $('#xlsx').change(function () {
        let val = verifyFormat();
        $(this).prop('checked', val);
    })
});

function read(input) {
    var file = document.getElementById("File");
    var fileName = file.value;
    var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
    if (extension == "CSV" || extension == "csv") {
        const csv = input.files[0];
        text = reader.readAsText(csv);
    }
}

let selectedFile;
function listen() {
    selectedFile = document.getElementById('File').files[0]
}

function toSave() {
    var val_potency = [];
    var val_type61 = true;
    var val_Horario = null;
    var val_region = document.getElementById("region_client").value;
    var val_contador = document.getElementById("counter-type").value

    if (!$("input[type=checkbox]").is(":checked")) {
        val_type61 = false;
    };

    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        val_potency.push($(`#Value_${i}`).val());
    }

    if ($('#flexRadioDefault1').is(':checked')) {
        val_Horario = "Horario";
        //makeHourlyCSV();
    }
    else if ($('#flexRadioDefault2').is(':checked')) {
        val_Horario = "Cuarto";
        //makeQuarterlyCSV();
    }
    else {
        val_Horario = null;
    }
    console.log(val_region);
    console.log(val_contador);
    console.log(val_type61);
    console.log(val_potency);
    console.log(val_Horario);
}

function verifyFormat() {
    if ($('#csv').is(':checked')) {
        var file = document.getElementById("File");
        var fileName = file.value;
        var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
        if (extension == "CSV" || extension == "csv") {
            return true;
        }
        else {
            $(this).checked = false;
            alert("El archivo no corresponde al tipe .csv");
            return false;
        }
    }
    if ($('#xlsx').is(':checked')) {
        var file = document.getElementById("File");
        var fileName = file.value;
        var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
        if (extension == "XLSX" || extension == "xlsx") {
            return true;
        }
        else {
            $(this).checked = false;
            alert("El archivo no corresponde al tipe .xlsx");
            return false;
        }
    }
}
//--------------------------------------------------------------------------------
var regionL = ['Andalucia', 'Canarias_1', 'Canarias_2']; //replace with list from MongoDB 
var contadorL = ['Tipo 1', 'Tipo 2', 'Tipo 3', 'Tipo 4', 'Tipo 5']; //replace with list from MongoDB
//----------------------------------------------------------------------------------------------
function populateList(listMDB, dataId) { // create options from inserted lists (MongoDB calls)
    var list = document.getElementById(dataId);
    listMDB.forEach(function (item) {
        let flag_double = true;
        for (let i = 0; i < document.getElementById(dataId).options.length; i++) { //verify option isn't already in the list
            if (document.getElementById(dataId).options[i].value == item) { // compare added option to existing options
                flag_double = false;
            }
        }
        if (flag_double) { // add new element
            let option = document.createElement('option');
            option.value = item;
            option.label = item;
            list.appendChild(option);
        }
    });
}

function validateForm() { //verify all elements are conform to the required format
    //test on the region
    var flag_reg = false;
    var reg = document.forms["formulario"]["region_elec"].value;
    for (let i = 0; i < document.getElementById("region_elec").options.length; i++) {
        if (reg == document.getElementById("region_elec").options[i].value) { //compare written value with available regions
            flag_reg = true;
        }
    }
    if (!flag_reg) {
        alert("Seleccionar una region");
        return false;
    }
    //test on the counter type



    //test on the potency values
    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        let val = document.forms["formulario"][`Value_${i}`].value; //grab value enterd by client
        if (val == "") {
            alert("Todos los valores de potencia deben de ser rellenados");
            return false;
        }
        console.log(val);
        if (isNumeric(val) == false) {
            alert("Todos los valores deben de ser numericos");
            return false;
        }
    }
    //verify format button is checked
    if ($('#xlsx').is(':checked')) {
        var format_xlsx = true;
    }
    else {
        var format_xlsx = false;
    }
    if ($('#csv').is(':checked')) {
        var format_csv = true;
    }
    else {
        var format_csv = false;
    }
    if (!format_csv && !format_xlsx) {
        alert("Elije un tipo de documento (csv/xlsx)")
        return false;
    }
}

function isNumeric(str) { //verify string is numeric (float or int)
    if (typeof str != "string") {
        return false // verify string type (not necessary considering input type is str)
    }
    return !isNaN(str) && // use type coersion to parse the _entirety_ of the string
        !isNaN(parseFloat(str)) //ensure strings of whitespace fail
}