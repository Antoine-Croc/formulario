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
           }

    } catch (MongoDB\Driver\Exception\Exception $e) {
        echo 'send help';
        $filename = basename(__FILE__);
        
        echo "The $filename script has experienced an error.\n"; 
        echo "It failed with the following exception:\n";
         
        echo "Exception:", $e->getMessage(), "\n";
        echo "In file:", $e->getFile(), "\n";
        echo "On line:", $e->getLine(), "\n";       
    }

    // $region = ['Andalucia', 'Canarias_1', 'Canarias_2']; //replace with list from MongoDB 
    // echo json_encode($region);
    
    ?>