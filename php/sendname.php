    <?PHP
    $name = $_REQUEST["name"];
//---------------------PIPE-----------------------
    $cmd = "python ../python/simulatereceive.py $name";
    $process = exec($cmd);
    ?>