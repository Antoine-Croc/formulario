<?php

    if ( 0 < $_FILES['file']['error'] ) {
        echo 'Error: ' . $_FILES['file']['error'] . '<br>';
    }
    else {
        move_uploaded_file($_FILES['file']['tmp_name'], '../curvas/' . $_FILES['file']['name']);
        $path = '../curvas/';
        $filename = $_FILES['file']['name'];
        $filepath = $path . $filename;
        echo $filepath;
    }

?>