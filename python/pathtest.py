######################################## READ ME #######################################
# Para importar los paths de este script de python es necesario
# poner en la cabezera de nuestros scripts las siguientes lineas
########################################################################################
# import sys
# if os.path.exists('O:/'): sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
# elif os.path.exists('/home'): sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
# import path
####################################### FIN READ ME ####################################

import os

###DIRECTORIOS SERVIDOR Y NAS
if os.path.exists('O:/'): ##Comprobar si existe el disco O: para la NAS
    root = 'O:/'
    root_2 = 'D:/Pierre/' ##ruta dedicada al Servidor
    root_3 = 'C:/Users/Administrador/' ##ruta dedicada al Servidor
    root_4 = 'C:/' ##ruta dedicada al Servidor
###DIRECTORIOS AWS
elif os.path.exists('/home'):
    root = "/home/ec2-user/ingebauBucket/Almacenamiento/"
    root_2 = "/home/ec2-user/Scripts/"
    root_3 = "/home/ec2-user/"
    root_4 = "/home/ec2-user/Scripts/"

path_config_perdidas = f'{root}Data_Utils/config_perdidas'
path_config_perdidas_canarias = f'{root}Data_Utils/config_perdidas_Canarias'

path_tables = f'{root}Data_Utils/tables.json'
path_periodos_nuevasTarifas = f'{root}Data_Utils/NuevasTarifas_Configuraciones/'
path_actualizacionNT_clientes = f'{root}Data_Utils/Actualizacion_NT_Clientes/'

