   <?PHP
    try {
        $mng = new MongoDB\Driver\Manager("mongodb://ingebau:ingebau@ec2-35-180-97-236.eu-west-3.compute.amazonaws.com:27017/gdc");        

        $query = new MongoDB\Driver\Query([]);

        $cursor = $mng->executeQuery('gdc.dictionaries', $query);

        foreach ( $cursor as $array) {
            echo(json_encode((array) $array));
           }

    } catch (MongoDB\Driver\Exception\Exception $e) {
            //TODO
        }
    ?>