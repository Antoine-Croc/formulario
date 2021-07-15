<?php
$when = date("h:i:s_d-m-Y");
$hour = date("h:i:s");
$name = ('Andalucia'.'_'.$when);

$namehour = "{'name':$name,'hour':$hour}";
echo ($namehour);
?>