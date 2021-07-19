<?php
$Jdata = ($_REQUEST); 

//aqui todo sale como string, hay que transformar los datos que se necesitan en int con intval()

for ($i = 0; $i < count($Jdata["potCont"]); $i++) {
    $Jdata["potCont"][$i] = intval($Jdata["potCont"][$i]);
}
$Jdata["tipoCont"] = intval($Jdata["tipoCont"]);
   
// var_dump($Jdata["arch"]);
// var_dump($Jdata["cuartoHor"]);;  
// var_dump($Jdata["flag"]);
// var_dump($Jdata["potCont"]);
// var_dump($Jdata["reg"]);
// var_dump($Jdata["tar"]);
// var_dump($Jdata["tipoCont"]);
// var_dump($Jdata);

$when = date("his_dmY");

$name = ($Jdata["reg"].'_'.$when.'.txt');

file_put_contents('../jsonfiles/'.$name, json_encode($Jdata)); //crear el archivo y cargar los datos adentro 

echo $name;
?>