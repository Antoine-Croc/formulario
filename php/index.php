    <?PHP
    $name = $_REQUEST["name"];
   // var_dump($name);
//---------------------PIPE----------------------------------

    $argument = "please_work i beg";

    $descriptorspec = array(
        0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
        1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
        2 => array("file", "error-output.txt", "a") // stderr is a file to write to
    );

    $cmd = "python ../python/test.py $name";

    $process = proc_open($cmd, $descriptorspec, $pipes);

    stream_set_read_buffer($pipes[1], 0);
    stream_set_blocking($pipes[0], false);
    stream_set_blocking($pipes[1], false);

    if (is_resource($process)) {
        //  $pipes now looks like this:
        //  0 => writeable handle connected to child stdin
        //  1 => readable handle connected to child stdout
        //  Any error output will be appended to /tmp/error-output.txt

        fwrite($pipes[0], '');
        fwrite($pipes[0], $argument);
        fclose($pipes[0]);

        echo stream_get_contents($pipes[1]); //print what python prints
        fclose($pipes[1]);

        //  It is important that you close any pipes before calling
        //  proc_close in order to avoid a deadlock
        $return_value = proc_close($process);

        echo "command returned $return_value\n";
    }
    ?>