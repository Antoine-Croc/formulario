import json

jsonF = {
        "arch": "Fecha,Hora,Consumo Activa\n7/6/2021,0,1\n7/6/2021,1,1\n7/6/2021,2,1\n7/6/2021,3,1\n7/6/2021,4,2\n7/6/2021,5,2\n7/6/2021,6,2\n7/6/2021,7,2\n7/6/2021,8,3\n7/6/2021,9,3\n7/6/2021,10,3\n7/6/2021,11,3\n7/6/2021,12,4\n7/6/2021,13,4\n7/6/2021,14,4\n7/6/2021,15,4\n7/6/2021,16,4.5\n7/6/2021,17,4.735294118\n7/6/2021,18,4.970588235\n7/6/2021,19,5.205882353\n7/6/2021,20,5.441176471\n7/6/2021,21,5.676470588\n7/6/2021,22,5.911764706\n7/6/2021,23,6.147058824\n",
        "cuartoHor": "false",
        "flag": "true",
        "potCont": [0, 0, 0, 0, 0, 0],
        "reg": "Andalucia",
        "tar": "3.0",
        "tipoCont": 1
    }

def fixJson(jf):
    if jf["flag"] == "true":
        jf["flag"] = True
    elif jf["flag"] == "false":
        jf["flag"] = False
    else :
        jf["flag"] = None
    
    if jf["cuartoHor"] == "true":
        jf["cuartoHor"] = True
    elif jf["cuartoHor"] == "false":
        jf["cuartoHor"] = False
    else : 
        jf["cuartoHor"] = None