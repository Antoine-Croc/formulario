$(document).ready(function() {
    $('#File').change(function() {
        listen();
        csvTested = false;
        text = '';
        $('#csv').prop('checked', false);
        $('#xlsx').prop('checked', false);
    })

    $('#csv').change(function() {
        let val = verifyFileFormat();
        $(this).prop('checked', val);
        if ($('#csv').is(':checked')) {
            let x = formatCSV_JSON(getText());
            if (!x) {
                if (!csvTested) {
                    $('#csv').prop('checked', false);
                }
            } else {
                csvTested = true;
            }
        }
    })

    $('#xlsx').change(function() {
        let val = verifyFileFormat();
        $(this).prop('checked', val);
        if ($('#xlsx').is(':checked')) {
            makexlsxJSON();
        }
    })
    $('#submit').on('click', function(e) {
        e.preventDefault();
        validateForm();
        $.ajax({
            type: "POST",
            url: "php/index.php",
            data: dataP,
            async: false
        }).done(function(data, status) {
            console.log(data);
            console.log(status);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            //TODO errorFunctions(); 
        });
    });
    $('#button').on('click', function(e) {
        dataP = {
                arch: "Fecha,Hora,Consumo Activa\n7/6/2021,0,1\n7/6/2021,1,1\n7/6/2021,2,1\n7/6/2021,3,1\n7/6/2021,4,2\n7/6/2021,5,2\n7/6/2021,6,2\n7/6/2021,7,2\n7/6/2021,8,3\n7/6/2021,9,3\n7/6/2021,10,3\n7/6/2021,11,3\n7/6/2021,12,4\n7/6/2021,13,4\n7/6/2021,14,4\n7/6/2021,15,4\n7/6/2021,16,4.5\n7/6/2021,17,4.735294118\n7/6/2021,18,4.970588235\n7/6/2021,19,5.205882353\n7/6/2021,20,5.441176471\n7/6/2021,21,5.676470588\n7/6/2021,22,5.911764706\n7/6/2021,23,6.147058824\n",
                cuartoHor: false,
                flag: true,
                potCont: [0, 0, 0, 0, 0, 0],
                reg: "Andalucia",
                tar: "3.0",
                tipoCont: 1
            }
            // $.post("php/index.php", dataP, function(data, status) {
            //     // Display the recieved data in browser
            //     console.log(data);
            //     console.log(status);
            // });
        $.ajax({
            type: "POST",
            url: "php/index.php",
            data: dataP,
            async: false
        }).done(function(data, status) {
            console.log(data);
            console.log(status);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            //TODO errorFunctions(); 
        });
    })
});

//-------------------------------
var selectedFile;
var text = '';
var dataP = null;
var dataStr = null;
var csvTested = false;
//-------------------------------

function read(input) { // select file for csv parsing
    var file = document.getElementById("File");
    var fileName = file.value;
    var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
    if (extension == "CSV" || extension == "csv") { //secondary verification of file extension
        const csv = input.files[0];
        text = reader.readAsText(csv);
    }
}

function listen() { //select file for xlsx parsing, different method from csv due to encoding
    selectedFile = document.getElementById('File').files[0]
}

function toSave() { //recuperate values to be sent
    var val_potency = [];
    var val_tarifaantigua = document.getElementById("rate-type").value;
    var val_Ntarifa61 = null;
    var val_cuartHorario = false;
    var val_region = document.getElementById("region_client").value;
    var val_contador = parseInt(document.getElementById("counter-type").value);
    var val_archivoJSON = document.getElementById("csvtext_use").innerText;

    val_Ntarifa61 = (val_tarifaantigua != "6.1A");

    val_cuartHorario = (xlCuarto || csvCuarto)

    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        val_potency.push(parseInt($(`#Value_${i}`).val()));
    }

    return postData(val_archivoJSON, val_cuartHorario, val_Ntarifa61, val_contador, val_tarifaantigua, val_region, val_potency)
}

function postData(Arch, CuartoHor, Flag, TipoCont, Tar, Reg, PotCont) {
    dataP = { "arch": Arch, "cuartoHor": CuartoHor, "flag": Flag, "tipoCont": TipoCont, "tar": Tar, "reg": Reg, "potCont": PotCont };
    console.log(dataP);
    //dataStr = JSON.stringify(dataP)
    return true;
}

function verifyFileFormat() { //does what it's called
    if ($('#csv').is(':checked')) {
        var file = document.getElementById("File");
        var fileName = file.value;
        var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
        if (extension == "CSV" || extension == "csv") {
            return true;
        } else {
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
        } else {
            $(this).checked = false;
            alert("El archivo no corresponde al tipe .xlsx");
            return false;
        }
    }
}
//--------------------------------------------------------------------------------
var regionL = ['Andalucia', 'Canarias_1', 'Canarias_2']; //replace with list from MongoDB 
var contadorL = ['1', '2', '3', '4', '5']; //replace with list from MongoDB
//----------------------------------------------------------------------------------------------
function populateList(listMDB, dataId) { // create options from inserted lists (MongoDB calls)
    var list = document.getElementById(dataId);
    listMDB.forEach(function(item) {
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
    if (document.getElementById("counter-type").value == "null") {
        alert('Elije un tipo de contador');
        return false;
    }

    //TODO test on the old rate
    if (document.getElementById('rate-type').value == "null") {
        alert('Elije un tarifua antiguo');
        return false;
    }
    //test on the potency values
    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        let val = document.forms["formulario"][`Value_${i}`].value; //grab value enterd by client
        if (val == "") {
            alert("Todos los valores de potencia deben de ser rellenados");
            return false;
        }
        if (isNumeric(val) == false) {
            alert("Todos los valores deben de ser numericos");
            return false;
        }
    }
    //verify format button is checked
    if ($('#xlsx').is(':checked')) {
        var format_xlsx = true;
    } else {
        var format_xlsx = false;
    }
    if ($('#csv').is(':checked')) {
        var format_csv = true;
    } else {
        var format_csv = false;
    }
    if (!format_csv && !format_xlsx) {
        alert("Elije un tipo de documento (csv/xlsx)")
        return false;
    }

    if (!contentGood) {
        alertmsg = "La columna de Consumo tiene [wrong values] en la(s) linea(s) siguiente:"
        contentRow.forEach(e => alertmsg = alertmsg + " - " + e)
        alert(alertmsg);
        return false;
    }

    return toSave();
}

function isNumeric(str) { //verify string is numeric (float or int)
    if (typeof str != "string") {
        return false // verify string type (not necessary considering input type is str)
    }
    return !isNaN(str) && // use type coersion to parse the _entirety_ of the string
        !isNaN(parseFloat(str)) //ensure strings of whitespace fail
}