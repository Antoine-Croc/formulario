<head>
    <title>run my python files</title>
    <meta charset="UTF-8" />
</head>

<body>
    <?PHP

    function is_json($string, $return_data = false)
    {
        $data = json_decode($string, true);
        return (json_last_error() == JSON_ERROR_NONE) ? ($return_data ? $data : TRUE) : FALSE;
    }
    $dataP = '{
        "arch": "Fecha,Hora,Consumo Activa\n7/6/2021,0,1\n7/6/2021,1,1\n7/6/2021,2,1\n7/6/2021,3,1\n7/6/2021,4,2\n7/6/2021,5,2\n7/6/2021,6,2\n7/6/2021,7,2\n7/6/2021,8,3\n7/6/2021,9,3\n7/6/2021,10,3\n7/6/2021,11,3\n7/6/2021,12,4\n7/6/2021,13,4\n7/6/2021,14,4\n7/6/2021,15,4\n7/6/2021,16,4.5\n7/6/2021,17,4.735294118\n7/6/2021,18,4.970588235\n7/6/2021,19,5.205882353\n7/6/2021,20,5.441176471\n7/6/2021,21,5.676470588\n7/6/2021,22,5.911764706\n7/6/2021,23,6.147058824\n",
        "cuartoHor": false,
        "flag": true,
        "potCont": [0, 0, 0, 0, 0, 0],
        "reg": "Andalucia",
        "tar": "3.0",
        "tipoCont": 1
    }';

    // $dataArray = json_decode($dataP,true);
    // $archivo = $dataArray["arch"];
    // $cuarto = $dataArray["cuartoHor"];
    // $flag = $dataArray["flag"];
    // $potCont = $dataArray["potCont"];
    // $region = $dataArray["reg"];
    // $tarifa = $dataArray["tar"];
    // $tipoCont = $dataArray["tipoCont"];

    // var_dump($archivo1);
    // var_dump($cuarto1);
    // var_dump($flag1);
    // var_dump($potCont1);
    // var_dump($region1);
    // var_dump($tarifa1);
    // var_dump($tipoCont1);

    echo "--------------------------------------- \n";

    $Jdata = ($_REQUEST);
    var_dump($Jdata);  



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
    
    var_dump($archivo);
    var_dump($cuarto);
    var_dump($flag);
    var_dump($potCont);
    var_dump($region);
    var_dump($tarifa);
    var_dump($tipoCont);

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