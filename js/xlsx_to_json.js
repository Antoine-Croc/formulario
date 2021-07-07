let data = [{ "key": "jay" }]
var test = null;
var index = 0;
var xlsxJSON = null;
var xlCuarto = false;
//--------------------------------------------
function makexlsxJSON() {
    XLSX.utils.json_to_sheet(data, 'out.xlsx');
    if (selectedFile) {
        let fileReader = new FileReader();
        fileReader.readAsBinaryString(selectedFile);
        fileReader.onload = (event) => {
            let data = event.target.result;
            let workbook = XLSX.read(data, { type: "binary", cellDates: true }); // read through excel encoding + change date format from binary(?) to normal
            if (workbook.SheetNames.length == 1) { //verify sheet length = 1
                workbook.SheetNames.forEach(sheet => { // only way to recuperate sheet values 
                    let rowObject = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheet]); //transform into array
                    for (let i = 0; i < rowObject.length; i++) {
                        index += 1;
                        rowObject[i]["Fecha"] = rowObject[i]["Fecha"].toLocaleDateString(); // set a useable date format (remove time)
                    }
                    xlsxJSON = rowObject; //apply local var to global var   
                    xlCuarto = xlsxJSON[0].hasOwnProperty("Cuarto");
                    fileFullxlsx(xlsxJSON);
                    document.getElementById("csvtext_use").innerHTML = JSON.stringify(rowObject, undefined, 4)
                });
            } else {
                alert('El archivo debe contener una solo pajina')
            }
        }
    }
};

function fileFullxlsx(arrayT) { // retrieve erroneous lines
    contentRow = [];
    let ind = 0

    for (let i = 1; i < arrayT.length - 1; i++) {
        num = parseFloat(arrayT[i]["Consumo Activa"])
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