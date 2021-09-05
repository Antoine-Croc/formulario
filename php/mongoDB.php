   <?PHP //database call to recuperate available regions/tariffs
    try {
        $mng = new MongoDB\Driver\Manager("mongodb://ingebau:ingebau@ec2-35-180-208-115.eu-west-3.compute.amazonaws.com:27017/gdc");        

        $query = new MongoDB\Driver\Query([]);

        $cursor = $mng->executeQuery('gdc.dictionaries', $query);

        foreach ( $cursor as $doc) {
            $newObj= (Object)[
                "tarifsold" => $doc -> tarifsold,
                "regions" => $doc -> regions
            ];
          }
           echo json_encode($newObj);
    } catch (MongoDB\Driver\Exception\Exception $e) {
            //TODO
        }
    ?>