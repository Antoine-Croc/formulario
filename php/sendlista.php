<?PHP //sends list to python script
    //var_dump($_REQUEST);
    $list = $_REQUEST["list"];
    $name = $_REQUEST["name"];
    $cuartoH = $_REQUEST["cuartoHor"];
    $flag = $_REQUEST["flag"];
    $tipoC = $_REQUEST["tipoCont"];
    $tar = $_REQUEST["tar"];
    $reg = $_REQUEST["reg"];
//---------------------PIPE-----------------------
    
$argument="";

$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("file", "error-output.txt", "a") // stderr is a file to write to
);

$cwd = null;
$env = null;

$cmd = "python ../python/test2_optimizeParalelo_test.py $name $cuartoH $flag $tipoC $tar $reg $list";
$process = proc_open($cmd, $descriptorspec, $pipes, $cwd, $env);

if (is_resource($process)) {
    // $pipes now looks like this:
    // 0 => writeable handle connected to child stdin
    // 1 => readable handle connected to child stdout
    // Any error output will be appended to /tmp/error-output.txt

    fwrite($pipes[0], '2');
    fwrite($pipes[0], $argument);   
    fclose($pipes[0]);

    echo stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    // It is important that you close any pipes before calling
    // proc_close in order to avoid a deadlock
    $return_value = proc_close($process);

    //echo "command returned $return_value\n";
}
    
?>