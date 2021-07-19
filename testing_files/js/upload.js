$(document).ready(function() {
    $('#file').change(function() {
        selectedFile = this.files[0]
        formD.append("file", selectedFile)
        alert(formD);
    })
    $("#btn_uploadfile").on('click', function(e) {
        $.ajax({
            type: "POST",
            url: "js/uploadfile.php",
            cache: false,
            contentType: false,
            processData: false,
            data: formD,
        }).done(function(response) {
            console.log(response)
        });
    });
});
var formD = new FormData();
var selectedFile;