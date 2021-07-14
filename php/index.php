    <?PHP
    $name = $_REQUEST["name"];
   // var_dump($name);

//---------------------PIPE-----------------------

    $argument = "please_work i beg";

    $descriptorspec = array(
        0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
        1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
        2 => array("file", "error-output.txt", "a") // stderr is a file to write to
    );

    $cmd = "python ../python/test.py $name";

    $process = exec($cmd);
    
    ?>