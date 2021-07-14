<head>
    <title>run my python files</title>
    <meta charset="UTF-8" />
</head>

<body>
    <?PHP
    $Jdata = ($_REQUEST);


    for ($i = 0; $i < count($Jdata["potCont"]); $i++) {
        $Jdata["potCont"][$i] = intval($Jdata["potCont"][$i]);
    }
    
    $Jdata["tipoCont"] = intval($Jdata["tipoCont"]);
  
    // $archivo = $Jdata["arch"];
    // $cuarto = $Jdata["cuartoHor"];
    // $flag = $Jdata["flag"];
    // $potCont = $Jdata["potCont"];
    // $region = $Jdata["reg"];
    // $tarifa = $Jdata["tar"];
    // $tipoCont = $Jdata["tipoCont"];    
    // var_dump($archivo);
    // var_dump($cuarto);
    // var_dump($flag);
    // var_dump($potCont);
    // var_dump($region);
    // var_dump($tarifa);
    // var_dump($tipoCont);

    //var_dump($Jdata);
    
    $Jdata = json_encode($Jdata);

    $data = base64_encode(json_encode($Jdata));

    var_dump($data);
    
    $argument = "please_work i beg";

    $descriptorspec = array(
        0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
        1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
        2 => array("file", "error-output.txt", "a") // stderr is a file to write to
    );

    $cmd = "python ../python/test.py $data";

    $process = proc_open($cmd, $descriptorspec, $pipes);

    stream_set_read_buffer($pipes[1], 0);
    stream_set_blocking($pipes[0], false);
    stream_set_blocking($pipes[1], false);

    if (is_resource($process)) {
        //  $pipes now looks like this:
        //  0 => writeable handle connected to child stdin
        //  1 => readable handle connected to child stdout
        //  Any error output will be appended to /tmp/error-output.txt

        fwrite($pipes[0], $data);
        fwrite($pipes[0], $argument);
        fclose($pipes[0]);

        echo stream_get_contents($pipes[1]); //print what python prints
        while (!feof($pipes[1])) {
            $out .= fgets($pipes[1], 1024);
        }
        fclose($pipes[1]);

        //  It is important that you close any pipes before calling
        //  proc_close in order to avoid a deadlock
        $return_value = proc_close($process);

        echo "command returned $return_value\n";
    }
    ?>
</body>