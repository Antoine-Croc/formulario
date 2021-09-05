$(document).ready(function() {
    $.ajax({ //recuperar las regiones de la bdd Mongodb
        type: "GET",
        url: "php/mongoDB.php",
    }).done(function(data) {
        try {
            //console.log(JSON.parse(data))
            regionL = JSON.parse(data).regions
            tarifaL = JSON.parse(data).tarifsold
        } catch (err) {
            console.log("FAIL")
            alert("Error en la informacion saliendo de la base de datos")
        }
    }).fail(function(jqXHR, exception) {
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
        } else if (jqXHR.status == 404) {
            msg = 'Requested page not found. [404]';
        } else if (jqXHR.status == 500) {
            msg = 'Internal Server Error [500].';
        } else if (exception === 'parsererror') {
            msg = 'Requested JSON parse failed.';
        } else if (exception === 'timeout') {
            msg = 'Time out error.';
        } else if (exception === 'abort') {
            msg = 'Ajax request aborted.';
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
        }
    });

    document.getElementById('progress__contour').style.display = "none"; //hiding of progress bar
    myProgressBar = document.querySelector(".progress__bar");
    updateProgressBar(myProgressBar, 0);

    $('#file').change(function() {
        selectedFile = this.files[0]
        formD.append("file", selectedFile)
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
        var f = validateForm();
        if (f) {
            $.ajax({
                type: "POST",
                url: "php/uploadfile.php",
                cache: false,
                contentType: false,
                processData: false,
                async: false,
                data: formD,
            }).done(function(response) {
                console.log(response)
            });
            $.ajax({ //enviar los datos en php para cargarlos en un archivo .txt
                type: "POST",
                url: "php/makefile.php",
                data: dataP,
                async: false
            }).done(function(data, status) {
                fname = data.split('.')[0]; // recuperar el nombre del archive sin el .txt
                fnameJ = { "name": fname }; // aqui tiene el .txt
                console.log(status);
            }).fail(function(jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
            });
            $.ajax({ // //enviar el nombre del archivo al python
                type: "POST",
                url: "php/sendname.php",
                data: fnameJ,
            }).done(function(res) {
                console.log(res)
            }).fail(function(jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
            });
        }
    });

    $('#button').on('click', function(e) {
        e.preventDefault();
        var f = validateForm();
        if (f) {
            $.ajax({
                type: "POST",
                url: "php/uploadfile.php",
                cache: false,
                contentType: false,
                processData: false,
                data: formD,
            }).done(function(response) {
                console.log(response)
            }).fail(function(jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
            });
            $.ajax({ //enviar la potencia y nombre del archivo al python
                type: "POST",
                url: "../form_opt/php/sendlistb.php",
                data: { "list": dataP["potCont"].toLocaleString(), "name": dataP["arch"].split('.')[0], "tipoCont": dataP["tipoCont"], "tar": dataP["tar"], "reg": dataP["reg"], 'cuartoHor': dataP["cuartoHor"].toLocaleString(), "flag": dataP["flag"].toLocaleString() }
            }).done(function(response) {
                if (response.split("\r")[0] == "ok") {
                    intflag = true;
                }
            }).fail(function(jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
            });
            document.getElementById('progress__contour').style.display = "block";
            var i = 0
            var thisInt = setInterval(function() {
                    updateProgressBar(myProgressBar, i);
                    i++;
                    if (intflag == true) {
                        i = 101;
                    }
                    if (i == 101) {
                        clearInterval(thisInt)
                        param = '?param=' + JSON.stringify(dataP)
                        alert("Job done");
                        window.location.href = "../form_opt/index.html" + param
                    }
                }, 200) //include dependency on FileSize

        }
    })
});

//-------------------------------Iniciar variables globales
var selectedFile;
var formD = new FormData;
var text = '';
var dataP = null;
var dataStr = null;
var csvTested = false;
var regionL = [];
var contadorL = ["1", "2", "3", "4", "5"];
var tarifaL = []
var fname = '';
var filename = '';
//-------------------------------

function read(input) { // select file for csv parsing
    var file = document.getElementById("file");
    fileName = file.value;
    var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //grab extension string value
    if (extension == "CSV" || extension == "csv") { //secondary verification of file extension
        const csv = input.files[0];
        text = reader.readAsText(csv);
    }
}

function toSave() { //recuperate values to be sent
    var val_potency = [];
    var val_tarifaantigua = document.getElementById("rate-type").value;
    var val_Ntarifa61 = null;
    var val_cuartHorario = false;
    var val_region = document.getElementById("region_client").value;
    var val_contador = parseInt(document.getElementById("counter-type").value);
    var val_Narchivo = fileName.split('\\')[2];

    val_Ntarifa61 = (val_tarifaantigua != "6.1A");

    val_cuartHorario = (xlCuarto || csvCuarto)

    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        val_potency.push(parseFloat($(`#Value_${i}`).val()));
    }
    return postData(val_Narchivo, val_cuartHorario, val_Ntarifa61, val_contador, val_tarifaantigua, val_region, val_potency)
}

function postData(Arch, CuartoHor, Flag, TipoCont, Tar, Reg, PotCont) { //preparar la forma json para el archivo
    dataP = { "arch": Arch, "cuartoHor": CuartoHor, "flag": Flag, "tipoCont": TipoCont, "tar": Tar, "reg": Reg, "potCont": PotCont };
    return true;
}

function verifyFileFormat() { //does what it's called
    if ($('#csv').is(':checked')) {
        var file = document.getElementById("file");
        fileName = file.value;
        var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //extension string value
        if (extension == "CSV" || extension == "csv") {
            return true;
        } else {
            $(this).checked = false;
            alert("El archivo no corresponde al tipo .csv");
            return false;
        }
    }
    if ($('#xlsx').is(':checked')) {
        var file = document.getElementById("file");
        fileName = file.value;
        var extension = fileName.substring(fileName.lastIndexOf('.') + 1); //extension string value
        if (extension == "XLSX" || extension == "xlsx") {
            return true;
        } else {
            $(this).checked = false;
            alert("El archivo no corresponde al tipo .xlsx");
            return false;
        }
    }
}

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

    //test on the old rate
    if (document.getElementById('rate-type').value == "null") {
        alert('Elije un tarifua antiguo');
        return false;
    }
    //test on the potency values
    for (let i = 1; i < document.getElementById("potency_input").elements.length + 1; i++) {
        let val = parseFloat(document.forms["formulario"][`Value_${i}`].value); //grab value enterd by client
        let valb = null;
        if (i > 1) {
            valb = parseFloat(document.forms["formulario"][`Value_${i-1}`].value);
            if (val < valb) {
                alert("Los valores de Px deben de ser superior o iguales a Px-1");
                return false;
            }
        }
        if (val == "") {
            alert("Todos los valores de potencia deben de ser rellenados correctamente");
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
        alert("Elije un tipo de archivo (csv/xlsx)")
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
//-------------Progress-bar-----------------------
var myProgressBar = null;
var fileSize = null;
var intflag = false;
//------------------------------------------------

function validateSize(input) {
    fileSize = input.files[0].size / 1024 / 1024; // in MiB = b / 1024^2
}

function updateProgressBar(progressBar, value) { //update progressbar's advancement
    value = Math.round(value);
    progressBar.querySelector(".progress__fill").style.width = `${value}%`;
    progressBar.querySelector(".progress__text").textContent = `${value}%`;
}