    <?PHP
    $name = $_REQUEST["name"];
   // var_dump($name);
//---------------------PIPE-----------------------
    $argument = "please_work i beg";

    $cmd = "python ../python/test.py $name";

    $process = exec($cmd);
    ?>