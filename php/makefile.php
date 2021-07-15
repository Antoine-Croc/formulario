<?php
$Jdata = ($_REQUEST);

//echo 'request received';

for ($i = 0; $i < count($Jdata["potCont"]); $i++) {
    $Jdata["potCont"][$i] = intval($Jdata["potCont"][$i]);
}
$Jdata["tipoCont"] = intval($Jdata["tipoCont"]);

//echo 'Integers re-typed';

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

$when = date("h;i;s_d-m-Y");

$name = ($Jdata["reg"].'_'.$when.'.txt');

//echo 'file named';

file_put_contents($name, json_encode($Jdata));

//echo 'data written in file';

//sleep(3);

echo $name;