import warnings
warnings.filterwarnings("ignore")
import json
from dateutil.parser import parse
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
import sqlite3
import numpy as np
import pickle
import csv
from dateutil.relativedelta import relativedelta
from copy import deepcopy
import requests
import urllib
import fnmatch
import calendar
from requests_oauthlib import OAuth1
from utiles import create_doc_apuntamiento, appen_Doc_apuntamiento, seasonZone, get_period, create_doc_apuntamiento_Peninsula, read_sips, sort_begin
from clean import clean
from parse_PERFF import create_filePERFF
if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as path
from utils import is_change_hour, create_list_date, scrap_matriz_horaria, type_day, sum_on_period, create_forecast_between
from parse_hourly import transform_in_hourly_SIPS
from parse_MEFF import scrap_MEFF, parse_MEFF


def main(pricing_config, indice_estimation):

	Apuntamientos = sqlite3.connect(path.LiquidacionesComunREE)
	Pricing = sqlite3.connect(path.Pricing)
	LiquidacionesComunREE = Apuntamientos.cursor()
	Pricing_Totales = sqlite3.connect('Pricing_Totales.db')
	Futuros_OMIE = sqlite3.connect(path.FUTUROS_OMIE)

	#create_doc_apuntamiento_Peninsula(LiquidacionesComunREE, Pricing_Totales)
	#appen_Doc_apuntamiento(Pricing_Totales, Pricing)

	Canarias = pd.DataFrame.from_records(Pricing_Totales.cursor().execute('SELECT * FROM ' + '"Total_Pricing_Canarias"').fetchall())
	Peninsula = pd.DataFrame.from_records(Pricing_Totales.cursor().execute('SELECT * FROM ' + '"Total_Pricing_Peninsula"').fetchall())

	Peninsula[0] = [datetime.strptime(item, '%Y-%m-%d %H:%M:%S') for item in Peninsula[0]]
	Canarias[0] = [datetime.strptime(item, '%Y-%m-%d %H:%M:%S') for item in Canarias[0]]

	Canarias.sort_values(by=0, inplace=True)
	Peninsula.sort_values(by=0, inplace=True)

	data_file_path = 'O:/INGEBAU/Becarios/Antoine/Ficheros_Pruebas.xlsx'

	Canarias = pd.read_excel(data_file_path, sheet_name=0, header=0, index_col=0, keep_default_na=True)
	Peninsula = pd.read_excel(data_file_path, sheet_name=1, header=0, index_col=0, keep_default_na=True)

	ajusteP1 = float(0.277988254984164)
	ajusteP2 = float(0.257508520554874)
	ajusteP3 = 1 - (ajusteP1 + ajusteP2)
	percentP1 = float(0.1)
	percentP2 = float(0.05)
	percentP3 = percentP1 - percentP2

	dict_contract = {
		"2.0A": "2_0TD",
		"2.0DHA": "2_0TD",
		"2.0DHS": "2_0TD",
		"2.1A": "2_0TD",
		"2.1DHA": "2_0TD",
		"2.1DHS": "2_0TD",
		"3.0A": "3_0TD",
		"3.1A": "6_1TD",
		"6.1A": "6_1TD",
		"6.2": "6_2TD",
		"6.3": "6_3TD",
		"6.4": "6_4TD",
		"2.0TD": "2_0TD",
		"3.0TD": "3_0TD",
		"6.1TD": "6_1TD",
		"6.2TD": "6_2TD",
		"6.3TD": "6_3TD",
		"6.4TD": "6_4TD"
	}

	dict_month = {1: 'JAN',
				2: 'FEB',
				3: 'MAR',
				4: 'APR',
				5: 'MAY',
				6: 'JUN',
				7: 'JUL',
				8: 'AUG',
				9: 'SEP',
				10: 'OCT',
				11: 'NOV',
				12: 'DEC'}

	with open(path.path_tables) as f:
		config_table = json.load(f)

	if indice_estimation == 'T':
		Listado_CUPS = pd.read_excel('Pricing_Datos_General.xlsx')
	elif indice_estimation == 'C':
		Listado_CUPS = pd.read_excel('Pricing_Datos.xlsx')
	else:
		Listado_CUPS = pd.read_json(js)

	for i in range(len(Listado_CUPS)):
            CUPS = Listado_CUPS.Cups[i]
            Tarifa = Listado_CUPS.tarifa[i]

            Tarifax = dict_contract[Tarifa]

            if Tarifax[0] == '6':
                Tarifa = '6_XTD'
            else:
                Tarifa = Tarifax

            with open(path.path_periodos_nuevasTarifas + f"{Tarifa}" + '.json') as f:
                config = json.load(f)
            Perfilado = Listado_CUPS.Perfilado[i]
            BooleanCUPS = any(x == CUPS for x in [item[2:-9] for item in os.listdir(path.path_data_hour_Guille)])
            tarifa = Tarifa.replace('_', '')

            Start_Historico = Listado_CUPS.Start_Historico[i]
            End_Historico =  Listado_CUPS.End_Historico[i]

            Start = Listado_CUPS.Start_Analysis[i]
            End = Listado_CUPS.End_Analysis[i]
            DSV = Listado_CUPS.DSV[i]
            region_tnp = Listado_CUPS.region_tnp[i]
            apuntamiento = Listado_CUPS['apuntamiento'][i]
            historicoSSAA = Listado_CUPS.historicoSSAA[i]
            riesgoSSAA = Listado_CUPS.riesgoSSAA[i]

            OMIE_analisis = Listado_CUPS.MEFF_analisis[i] # or format [year-month-day]

            FondoEE = Listado_CUPS.FONDO_EFIC_ENERG[i]

            BonoSocial = Listado_CUPS.BONO_SOCIAL[i]

            Beneficio = Listado_CUPS.Beneficio[i]

            if region_tnp == 'peninsula':
                REGION = Peninsula
            elif region_tnp == 'canarias':
                REGION = Canarias

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#                             main
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

JSON_test = {"Perfilado": "perf", "tarifa": "3.0TD", "Cups": "ES1234567890123456ES0F", "Start_Historico": "1/1/2017", "End_Historico": "1/1/2021", "Start_Analysis": "1/1/2022", "End_Analysis": "1/1/2023", "DSV": 2, "region_tnp": "peninsula", "apuntamiento": "minimo", "historicoSSAA": [2017, 2018, 2020], "riesgoSSAA": "minimo", "MEFF_analisis": "today", "FONDO_EFIC_ENERG" : 0.30, "BONO_SOCIAL" : 0, "Beneficio" : 0}
js = json.dumps(JSON_test, indent = 4)

if __name__ == '__main__':
    A = datetime.now()
    with open('pricing_settings.json') as f:
        pricing_config = json.load(f)
    boolean = False
    while not boolean:
        factura = input('Análisis a Realizar, T: Pricing_Datos_General, C: Cups específicos:, X: Testing_Json')
        try:
            indice_estimation = factura
            boolean = True
        except:
            print('Not good shape of date')
    main(pricing_config, indice_estimation)