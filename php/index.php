<head>
<title>run my python files</title>
<?PHP
$json = file_get_contents('php://input'); 
$obj = json_decode($json);
///echo $obj['tar'];
$data = json_decode(file_get_contents('php://input'), true);
echo $data;
?>
</head>
<body>
<legend class="Title">--Titulo--</legend>
</body>
