   <?PHP
    try {
        $mng = new MongoDB\Driver\Manager("mongodb://ingebau:ingebau@ec2-35-180-97-236.eu-west-3.compute.amazonaws.com:27017/gdc");        
//        echo 'manager ok';

        $query = new MongoDB\Driver\Query([]);
//        echo 'query ok';

        $cursor = $mng->executeQuery('gdc.dictionaries', $query);
//        echo 'cursor ok';

//        var_dump($cursor);
        foreach ( $cursor as $array) {
            echo(json_encode((array) $array));
         //   $please = json_decode(json_encode($array));
        //   echo $please ;
           }

    } catch (MongoDB\Driver\Exception\Exception $e) {
        //TODO
    }
    // phptest
    // $region = ['Andalucia', 'Canarias_1', 'Canarias_2']; //replace with list from MongoDB 
    // echo json_encode($region);

    ?>