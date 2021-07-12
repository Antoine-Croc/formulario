<head>
    <title>run my python files</title>
    <meta charset="UTF-8" />
</head>

<body>
    <?PHP
    $Jdata = ($_REQUEST);
    //var_dump($Jdata);  



    $archivo = $Jdata["arch"];
    $cuarto = $Jdata["cuartoHor"];
    $flag = $Jdata["flag"];
    $potCont = $Jdata["potCont"];
    $region = $Jdata["reg"];
    $tarifa = $Jdata["tar"];
    $tipoCont = $Jdata["tipoCont"];

    for ($i = 0; $i < count($potCont); $i++) {
        $potCont[$i] = intval($potCont[$i]);
    }
    
    $tipoCont = intval($tipoCont);
    
    // var_dump($archivo);
    // var_dump($cuarto);
    // var_dump($flag);
    // var_dump($potCont);
    // var_dump($region);
    // var_dump($tarifa);
    // var_dump($tipoCont);

    $data = base64_encode(json_encode($dataP));

    $argument = "please_work i beg";

    $descriptorspec = array(
        0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
        1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
        2 => array("file", "error-output.txt", "a") // stderr is a file to write to
    );

    $cwd = null;
    $env = null;
    $cmd = "python ../python/test.py $data";

    $process = proc_open($cmd, $descriptorspec, $pipes, $cwd, $env);

    if (is_resource($process)) {
        //  $pipes now looks like this:
        //  0 => writeable handle connected to child stdin
        //  1 => readable handle connected to child stdout
        //  Any error output will be appended to /tmp/error-output.txt

        fwrite($pipes[0], '2');
        fwrite($pipes[0], $argument);
        fclose($pipes[0]);

        echo stream_get_contents($pipes[1]);
        fclose($pipes[1]);

        //  It is important that you close any pipes before calling
        //  proc_close in order to avoid a deadlock
        $return_value = proc_close($process);

        echo "command returned $return_value\n";
    }
    ?>
</body>