<head>
    <title>run my python files</title>
    <meta charset="UTF-8" />
</head>
<body>
<?php

$dataP = '{
    "arch": ""[{\"Fecha\": \"7/14/2021\", \"Hora\":0, \"Cuarto\":1, \"Consumo Activa\":4}, {\"Fecha\": \"7/14/2021\", \"Hora\":0, \"Cuarto\":2, \"Consumo Activa\":4.01}, {\"Fecha\": \"7/14/2021\", \"Hora\":0, \"Cuarto\":3, \"Consumo Activa\":4.02}, {\"Fecha\": \"7/14/2021\", \"Hora\":0, \"Cuarto\":4, \"Consumo Activa\":4.03}, {\"Fecha\": \"7/14/2021\", \"Hora\":1, \"Cuarto\":1, \"Consumo Activa\":4.04}, {\"Fecha\": \"7/14/2021\", \"Hora\":1, \"Cuarto\":2, \"Consumo Activa\":4.05}, {\"Fecha\": \"7/14/2021\", \"Hora\":1, \"Cuarto\":3, \"Consumo Activa\":4.06}, {\"Fecha\": \"7/14/2021\", \"Hora\":1, \"Cuarto\":4, \"Consumo Activa\":4.07}, {\"Fecha\": \"7/14/2021\", \"Hora\":2, \"Cuarto\":1, \"Consumo Activa\":4.08}, {\"Fecha\": \"7/14/2021\", \"Hora\":2, \"Cuarto\":2, \"Consumo Activa\":4.09}, {\"Fecha\": \"7/14/2021\", \"Hora\":2, \"Cuarto\":3, \"Consumo Activa\":4.1}, {\"Fecha\": \"7/14/2021\", \"Hora\":2, \"Cuarto\":4, \"Consumo Activa\":4.11}, {\"Fecha\": \"7/14/2021\", \"Hora\":3, \"Cuarto\":1, \"Consumo Activa\":4.12}, {\"Fecha\": \"7/14/2021\", \"Hora\":3, \"Cuarto\":2, \"Consumo Activa\":4.13}, {\"Fecha\": \"7/14/2021\", \"Hora\":3, \"Cuarto\":3, \"Consumo Activa\":4.14}, {\"Fecha\": \"7/14/2021\", \"Hora\":3, \"Cuarto\":4, \"Consumo Activa\":4.15}, {\"Fecha\": \"7/14/2021\", \"Hora\":4, \"Cuarto\":1, \"Consumo Activa\":4.16}, {\"Fecha\": \"7/14/2021\", \"Hora\":4, \"Cuarto\":2, \"Consumo Activa\":4.17}, {\"Fecha\": \"7/14/2021\", \"Hora\":4, \"Cuarto\":3, \"Consumo Activa\":4.18}, {\"Fecha\": \"7/14/2021\", \"Hora\":4, \"Cuarto\":4, \"Consumo Activa\":4.19}, {\"Fecha\": \"7/14/2021\", \"Hora\":5, \"Cuarto\":1, \"Consumo Activa\":4.2}, {\"Fecha\": \"7/14/2021\", \"Hora\":5, \"Cuarto\":2, \"Consumo Activa\":4.21}, {\"Fecha\": \"7/14/2021\", \"Hora\":5, \"Cuarto\":3, \"Consumo Activa\":4.22}, {\"Fecha\": \"7/14/2021\", \"Hora\":5, \"Cuarto\":4, \"Consumo Activa\":4.23}, {\"Fecha\": \"7/14/2021\", \"Hora\":6, \"Cuarto\":1, \"Consumo Activa\":4.24}, {\"Fecha\": \"7/14/2021\", \"Hora\":6, \"Cuarto\":2, \"Consumo Activa\":4.25}, {\"Fecha\": \"7/14/2021\", \"Hora\":6, \"Cuarto\":3, \"Consumo Activa\":4.26}, {\"Fecha\": \"7/14/2021\", \"Hora\":6, \"Cuarto\":4, \"Consumo Activa\":4.27}, {\"Fecha\": \"7/14/2021\", \"Hora\":7, \"Cuarto\":1, \"Consumo Activa\":4.28}, {\"Fecha\": \"7/14/2021\", \"Hora\":7, \"Cuarto\":2, \"Consumo Activa\":4.29}, {\"Fecha\": \"7/14/2021\", \"Hora\":7, \"Cuarto\":3, \"Consumo Activa\":4.3}, {\"Fecha\": \"7/14/2021\", \"Hora\":7, \"Cuarto\":4, \"Consumo Activa\":4.31}, {\"Fecha\": \"7/14/2021\", \"Hora\":8, \"Cuarto\":1, \"Consumo Activa\":4.32}, {\"Fecha\": \"7/14/2021\", \"Hora\":8, \"Cuarto\":2, \"Consumo Activa\":4.33}, {\"Fecha\": \"7/14/2021\", \"Hora\":8, \"Cuarto\":3, \"Consumo Activa\":4.34}, {\"Fecha\": \"7/14/2021\", \"Hora\":8, \"Cuarto\":4, \"Consumo Activa\":4.35}, {\"Fecha\": \"7/14/2021\", \"Hora\":9, \"Cuarto\":1, \"Consumo Activa\":4.36}, {\"Fecha\": \"7/14/2021\", \"Hora\":9, \"Cuarto\":2, \"Consumo Activa\":4.37}, {\"Fecha\": \"7/14/2021\", \"Hora\":9, \"Cuarto\":3, \"Consumo Activa\":4.38}, {\"Fecha\": \"7/14/2021\", \"Hora\":9, \"Cuarto\":4, \"Consumo Activa\":4.39}, {\"Fecha\": \"7/14/2021\", \"Hora\":10, \"Cuarto\":1, \"Consumo Activa\":4.4}, {\"Fecha\": \"7/14/2021\", \"Hora\":10, \"Cuarto\":2, \"Consumo Activa\":4.41}, {\"Fecha\": \"7/14/2021\", \"Hora\":10, \"Cuarto\":3, \"Consumo Activa\":4.42}, {\"Fecha\": \"7/14/2021\", \"Hora\":10, \"Cuarto\":4, \"Consumo Activa\":4.43}, {\"Fecha\": \"7/14/2021\", \"Hora\":11, \"Cuarto\":1, \"Consumo Activa\":4.44}, {\"Fecha\": \"7/14/2021\", \"Hora\":11, \"Cuarto\":2, \"Consumo Activa\":4.45}, {\"Fecha\": \"7/14/2021\", \"Hora\":11, \"Cuarto\":3, \"Consumo Activa\":4.46}, {\"Fecha\": \"7/14/2021\", \"Hora\":11, \"Cuarto\":4, \"Consumo Activa\":4.47}, {\"Fecha\": \"7/14/2021\", \"Hora\":12, \"Cuarto\":1, \"Consumo Activa\":4.48}, {\"Fecha\": \"7/14/2021\", \"Hora\":12, \"Cuarto\":2, \"Consumo Activa\":4.49}, {\"Fecha\": \"7/14/2021\", \"Hora\":12, \"Cuarto\":3, \"Consumo Activa\":4.5}, {\"Fecha\": \"7/14/2021\", \"Hora\":12, \"Cuarto\":4, \"Consumo Activa\":4.51}, {\"Fecha\": \"7/14/2021\", \"Hora\":13, \"Cuarto\":1, \"Consumo Activa\":4.52}, {\"Fecha\": \"7/14/2021\", \"Hora\":13, \"Cuarto\":2, \"Consumo Activa\":4.53}, {\"Fecha\": \"7/14/2021\", \"Hora\":13, \"Cuarto\":3, \"Consumo Activa\":4.54}, {\"Fecha\": \"7/14/2021\", \"Hora\":13, \"Cuarto\":4, \"Consumo Activa\":4.55}, {\"Fecha\": \"7/14/2021\", \"Hora\":14, \"Cuarto\":1, \"Consumo Activa\":4.56}, {\"Fecha\": \"7/14/2021\", \"Hora\":14, \"Cuarto\":2, \"Consumo Activa\":4.57}, {\"Fecha\": \"7/14/2021\", \"Hora\":14, \"Cuarto\":3, \"Consumo Activa\":4.58}, {\"Fecha\": \"7/14/2021\", \"Hora\":14, \"Cuarto\":4, \"Consumo Activa\":4.59}, {\"Fecha\": \"7/14/2021\", \"Hora\":15, \"Cuarto\":1, \"Consumo Activa\":4.6}, {\"Fecha\": \"7/14/2021\", \"Hora\":15, \"Cuarto\":2, \"Consumo Activa\":4.61}, {\"Fecha\": \"7/14/2021\", \"Hora\":15, \"Cuarto\":3, \"Consumo Activa\":4.62}, {\"Fecha\": \"7/14/2021\", \"Hora\":15, \"Cuarto\":4, \"Consumo Activa\":4.63}, {\"Fecha\": \"7/14/2021\", \"Hora\":16, \"Cuarto\":1, \"Consumo Activa\":4.64}, {\"Fecha\": \"7/14/2021\", \"Hora\":16, \"Cuarto\":2, \"Consumo Activa\":4.65}, {\"Fecha\": \"7/14/2021\", \"Hora\":16, \"Cuarto\":3, \"Consumo Activa\":4.66}, {\"Fecha\": \"7/14/2021\", \"Hora\":16, \"Cuarto\":4, \"Consumo Activa\":4.67}, {\"Fecha\": \"7/14/2021\", \"Hora\":17, \"Cuarto\":1, \"Consumo Activa\":4.68}, {\"Fecha\": \"7/14/2021\", \"Hora\":17, \"Cuarto\":2, \"Consumo Activa\":4.69}, {\"Fecha\": \"7/14/2021\", \"Hora\":17, \"Cuarto\":3, \"Consumo Activa\":4.7}, {\"Fecha\": \"7/14/2021\", \"Hora\":17, \"Cuarto\":4, \"Consumo Activa\":4.71}, {\"Fecha\": \"7/14/2021\", \"Hora\":18, \"Cuarto\":1, \"Consumo Activa\":4.72}, {\"Fecha\": \"7/14/2021\", \"Hora\":18, \"Cuarto\":2, \"Consumo Activa\":4.73}, {\"Fecha\": \"7/14/2021\", \"Hora\":18, \"Cuarto\":3, \"Consumo Activa\":4.74}, {\"Fecha\": \"7/14/2021\", \"Hora\":18, \"Cuarto\":4, \"Consumo Activa\":4.75}, {\"Fecha\": \"7/14/2021\", \"Hora\":19, \"Cuarto\":1, \"Consumo Activa\":4.76}, {\"Fecha\": \"7/14/2021\", \"Hora\":19, \"Cuarto\":2, \"Consumo Activa\":4.77}, {\"Fecha\": \"7/14/2021\", \"Hora\":19, \"Cuarto\":3, \"Consumo Activa\":4.78}, {\"Fecha\": \"7/14/2021\", \"Hora\":19, \"Cuarto\":4, \"Consumo Activa\":4.79}, {\"Fecha\": \"7/14/2021\", \"Hora\":20, \"Cuarto\":1, \"Consumo Activa\":4.8}, {\"Fecha\": \"7/14/2021\", \"Hora\":20, \"Cuarto\":2, \"Consumo Activa\":4.81}, {\"Fecha\": \"7/14/2021\", \"Hora\":20, \"Cuarto\":3, \"Consumo Activa\":4.82}, {\"Fecha\": \"7/14/2021\", \"Hora\":20, \"Cuarto\":4, \"Consumo Activa\":4.83}, {\"Fecha\": \"7/14/2021\", \"Hora\":21, \"Cuarto\":1, \"Consumo Activa\":4.84}, {\"Fecha\": \"7/14/2021\", \"Hora\":21, \"Cuarto\":2, \"Consumo Activa\":4.85}, {\"Fecha\": \"7/14/2021\", \"Hora\":21, \"Cuarto\":3, \"Consumo Activa\":4.86}, {\"Fecha\": \"7/14/2021\", \"Hora\":21, \"Cuarto\":4, \"Consumo Activa\":4.87}, {\"Fecha\": \"7/14/2021\", \"Hora\":22, \"Cuarto\":1, \"Consumo Activa\":4.88}, {\"Fecha\": \"7/14/2021\", \"Hora\":22, \"Cuarto\":2, \"Consumo Activa\":4.89}, {\"Fecha\": \"7/14/2021\", \"Hora\":22, \"Cuarto\":3, \"Consumo Activa\":4.9}, {\"Fecha\": \"7/14/2021\", \"Hora\":22, \"Cuarto\":4, \"Consumo Activa\":4.91}, {\"Fecha\": \"7/14/2021\", \"Hora\":23, \"Cuarto\":1, \"Consumo Activa\":4.92}, {\"Fecha\": \"7/14/2021\", \"Hora\":23, \"Cuarto\":2, \"Consumo Activa\":4.93}, {\"Fecha\": \"7/14/2021\", \"Hora\":23, \"Cuarto\":3, \"Consumo Activa\":4.94}, {\"Fecha\": \"7/14/2021\", \"Hora\":23, \"Cuarto\":4, \"Consumo Activa\":4.95}]"",
    "cuartoHor": false,
    "flag": true,
    "potCont": [0, 0, 0, 0, 0, 0],
    "reg": "Andalucia",
    "tar": "3.0",
    "tipoCont": 1
}';

var_dump($dataP);

$name ="filetoreadname.txt";

$argument="please_work i beg";

$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("file", "error-output.txt", "a") // stderr is a file to write to
);

$cwd = null;
$env = null;
$cmd ="python ../python/test.py $name";

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

    echo "command returned $return_value\n";
}
?>
</body>