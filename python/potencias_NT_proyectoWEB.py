# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ IMPORTS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
# Imports de los paths para las direcciones de la NAS
import sys
import os

if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph

# Imports de las librerias de PANDAS (para los dataframes) y NUMPY (para trabajo matricial)
import pandas as pd
import numpy as np

# Imports de librerias JSON (diccionarios de configuraciones) y DATETIME (para trabajo con fechas)
import json as js
from datetime import datetime as dt

#  Import de libreria de optimizacion SCIPY
from scipy.optimize import minimize

# Otros imports
from builtins import float


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES CLASIFICACION DE DIAS Y OBTENCIÓN DE PERIODOS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# Función que me asigna la temporada correspodiente a un dia segun la tarifa y la region
def seasonZone(day, zone, tar):  # Para saber la temporada en funcion del dia y la región
    temp = 0
    if tar != '2_0TD':  # or '6_XTD' or '6_1TD' or '6_2TD' or '6_3TD' or '6_4TD':
        if zone == 'peninsula':
            if day.month in [1, 2, 7, 12]:
                temp = 'Alta'
            elif day.month in [3, 11]:
                temp = 'MediaAlta'
            elif day.month in [6, 8, 9]:
                temp = 'Media'
            else:
                temp = 'Baja'

        elif zone == 'canarias':
            if day.month in [7, 8, 9, 10]:
                temp = 'Alta'
            elif day.month in [11, 12]:
                temp = 'MediaAlta'
            elif day.month in [1, 2, 3]:
                temp = 'Media'
            else:
                temp = 'Baja'

        elif zone == 'baleares':
            if day.month == 6 or day.month == 7 or day.month == 8 or day.month == 9:
                temp = 'Alta'
            elif day.month == 5 or day.month == 10:
                temp = 'MediaAlta'
            elif day.month == 1 or day.month == 2 or day.month == 12:
                temp = 'Media'
            else:
                temp = 'Baja'

        elif zone == 'ceuta':
            if day.month == 1 or day.month == 2 or day.month == 8 or day.month == 9:
                temp = 'Alta'
            elif day.month == 7 or day.month == 10:
                temp = 'MediaAlta'
            elif day.month == 3 or day.month == 11 or day.month == 12:
                temp = 'Media'
            else:
                temp = 'Baja'

        elif zone == 'melilla':
            if day.month == 1 or day.month == 7 or day.month == 8 or day.month == 9:
                temp = 'Alta'
            elif day.month == 2 or day.month == 12:
                temp = 'MediaAlta'
            elif day.month == 6 or day.month == 10 or day.month == 11:
                temp = 'Media'
            else:
                temp = 'Baja'
    elif tar == '2_0TD':
        temp = 'Alta'
    else:
        print('ERROR EN LA ACTUALIZACIÓN DE TARIFAS')
    return temp


# Función que me identifica si el dia de estudio es laboral
def is_working_day(date):
    """
    Test if the date is a working date
    """
    out = True
    day_off = [(1, 1), (6, 1), (1, 5), (15, 8), (12, 10), (1, 11), (6, 12), (8, 12), (25, 12)]
    if date.weekday() == 5 or date.weekday() == 6:
        out = False
    elif (date.day, date.month) in day_off:
        out = False
    return out


# Función que me devuelve si la hora está dentro del periodo tarifario de estudio
def in_period(d, per):
    """
    Test if d is in a list of periods od hours with [begin_period1, end_period1, begin_period2, end_period2, ...]
    """
    h = d.hour
    for i in range(0, len(per), 2):
        if per[i] <= h <= per[i + 1]:
            return True
    return False


# Función que me devuelve el periodo tarifario de POTENCIAS del dia y sus horas
def get_period_NEWTARp(config, d, s, zone, tar):  # Para obteneer el periodo en función del dia, la tarifa y la zona
    periods_config = config[s][zone]
    try:
        if is_working_day(d):
            periods_config = periods_config["Semana"]
        else:
            periods_config = periods_config["Finde"]
    except:
        pass

    if tar == '2_0TD':
        perPot = [item for item in periods_config if
                  item[-1] == 'P']  # Para que solo me coja los dos terminos de potencia de las tarifas 2.0TD
        for period in perPot:
            if in_period(d, periods_config[period]):
                return config["Periodo"][period]
            elif in_period(d, periods_config[period]):
                return config["Perido"][period]
    else:
        for period in periods_config:
            if in_period(d, periods_config[period]):
                return config["Periodo"][period]
            elif in_period(d, periods_config[period]):
                return config["Perido"][period]


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES PRINCIPALES DE CÁLCULOS PEDIDOS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

def df_potConsumida_NEWTAR(archivo, tarifa, region):
    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    # Actualizacion de la tarifa antigua a las nuevas tarifas ---------------------------------------------------------
    newTar = tablesLOAD['CambioTarifa'][tarifa]
    if newTar == '2.0TD':
        newTar_periods = '2_0TD'  # Para trabajar con las configuraciones de tarifas
    elif newTar == '3.0TD':
        newTar_periods = '3_0TD'  # Para trabajar con las configuraciones de tarifas
    else:
        newTar_periods = '6_XTD'  # Para trabajar con las configuraciones de tarifas

    # Cargamos configuraciones para la tarifa de entrada --------------------------------------------------------------
    with open(f'{ph.path_periodos_nuevasTarifas}{newTar_periods}.json') as config:
        config_perLOAD = js.load(config)

    # Extracción de los datos de las curvas de cosnumos dependiendo del formato de entrada de la misma ----------------
    list_Date = []  # Lugar de volcado de las fechas del archivo de curva de consummo de entrada
    list_PotConsum = []  # Lugar de volcado de los consumos del archivo de curva de consummo de entrada

    try:  # Intento abrir un archivo de formato ".csv"
        data = pd.read_csv(f'{ph.path_actualizacionNT_clientes}{archivo}.csv', sep=';')
        for i in range(len(data)):
            dateCSV = f'{str(data["Fecha"][i])} {str(data["Hora"][i])}'
            try:
                list_Date.append(dt.strptime(dateCSV, '%Y-%m-%d %H,00'))
            except:
                list_Date.append(dt.strptime(dateCSV, '%d/%m/%Y %H'))
            try:
                potConsum = data["Consumo Activa"][i].replace('.', '')
            except:
                potConsum = data["Consumption"][i].replace('.', '')
            list_PotConsum.append(potConsum.replace(',', '.'))
    except:  # Si no funciona, intento abrir un archivo de formato ".xlsx"
        data = pd.read_excel(f'{ph.path_actualizacionNT_clientes}{archivo}.xlsx', sheet_name='Hoja1')
        for i in range(len(data)):
            dateXLSX = dt.strptime(f'{str(data["Fecha"][i])}', '%Y-%m-%d %H:%M:%S')
            dateXLSX = dateXLSX.replace(hour=data["Hora"][i])
            list_Date.append(dateXLSX)
            potConsum = data["Consumo Activa"][i]
            list_PotConsum.append(potConsum)

    # Creacion de un dataframe para facilidad de calculos y agrupaciones
    period = []
    fecha = []
    mes = []
    tempor = []
    potenConsum = []

    for j in range(len(data)):
        period.append(
            get_period_NEWTARp(config_perLOAD, list_Date[j], seasonZone(list_Date[j], region, newTar_periods), region,
                               newTar_periods))
        fecha.append(list_Date[j])
        mes.append(list_Date[j].month)
        tempor.append(seasonZone(list_Date[j], region, newTar_periods))
        potenConsum.append(float(list_PotConsum[j]))

    df_listaPotConsum = pd.DataFrame(
        {
            "Periodo": period,
            "Fecha": fecha,
            "Mes": mes,
            "Temporada": tempor,
            "Potencia Consumida": potenConsum
        }
    )

    # Agrupamos las potencias por periodos
    try:
        pot_ConsumP1 = df_listaPotConsum.groupby('Periodo').get_group(1).reset_index(drop=True)
    except:
        pot_ConsumP1 = 0

    try:
        pot_ConsumP2 = df_listaPotConsum.groupby('Periodo').get_group(2).reset_index(drop=True)
    except:
        pot_ConsumP2 = 0

    try:
        pot_ConsumP3 = df_listaPotConsum.groupby('Periodo').get_group(3).reset_index(drop=True)
    except:
        pot_ConsumP3 = 0

    try:
        pot_ConsumP4 = df_listaPotConsum.groupby('Periodo').get_group(4).reset_index(drop=True)
    except:
        pot_ConsumP4 = 0

    try:
        pot_ConsumP5 = df_listaPotConsum.groupby('Periodo').get_group(5).reset_index(drop=True)
    except:
        pot_ConsumP5 = 0

    try:
        pot_ConsumP6 = df_listaPotConsum.groupby('Periodo').get_group(6).reset_index(drop=True)
    except:
        pot_ConsumP6 = 0

    # Calculamos el consumo total de potencias por periodo y mes
    suma_potConsum_P1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_potConsum_P2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_potConsum_P3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_potConsum_P4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_potConsum_P5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_potConsum_P6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(1, 13):
        try:
            pot_ConsumP1_mes = pot_ConsumP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP1_mes = [0]

        try:
            pot_ConsumP2_mes = pot_ConsumP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP2_mes = [0]

        try:
            pot_ConsumP3_mes = pot_ConsumP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP3_mes = [0]

        try:
            pot_ConsumP4_mes = pot_ConsumP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP4_mes = [0]

        try:
            pot_ConsumP5_mes = pot_ConsumP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP5_mes = [0]

        try:
            pot_ConsumP6_mes = pot_ConsumP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
        except:
            pot_ConsumP6_mes = [0]

        for h in range(len(pot_ConsumP1_mes)):
            suma_potConsum_P1[i - 1] += pot_ConsumP1_mes[h]

        for j in range(len(pot_ConsumP2_mes)):
            suma_potConsum_P2[i - 1] += pot_ConsumP2_mes[j]

        for k in range(len(pot_ConsumP3_mes)):
            suma_potConsum_P3[i - 1] += pot_ConsumP3_mes[k]

        for p in range(len(pot_ConsumP4_mes)):
            suma_potConsum_P4[i - 1] += pot_ConsumP4_mes[p]

        for m in range(len(pot_ConsumP5_mes)):
            suma_potConsum_P5[i - 1] += pot_ConsumP5_mes[m]

        for n in range(len(pot_ConsumP6_mes)):
            suma_potConsum_P6[i - 1] += pot_ConsumP6_mes[n]

    suma_potConsum_P1.append(sum(suma_potConsum_P1))
    suma_potConsum_P2.append(sum(suma_potConsum_P2))
    suma_potConsum_P3.append(sum(suma_potConsum_P3))
    suma_potConsum_P4.append(sum(suma_potConsum_P4))
    suma_potConsum_P5.append(sum(suma_potConsum_P5))
    suma_potConsum_P6.append(sum(suma_potConsum_P6))

    df_potConsumidaMesPer = pd.DataFrame(
        {
            'Periodo_1': suma_potConsum_P1,
            'Periodo_2': suma_potConsum_P2,
            'Periodo_3': suma_potConsum_P3,
            'Periodo_4': suma_potConsum_P4,
            'Periodo_5': suma_potConsum_P5,
            'Periodo_6': suma_potConsum_P6
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    # Adaptacion de los resultados para exportar a excel
    df_potConsumidaMesPer_excel = pd.DataFrame(
        {
            'P1': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P2': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P3': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P4': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P5': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P6': ['', '', '', '', '', '', '', '', '', '', '', '', '']
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    for aux in range(0, 13):
        df_potConsumidaMesPer_excel['P1'][aux] = str(df_potConsumidaMesPer['Periodo_1'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_excel['P2'][aux] = str(df_potConsumidaMesPer['Periodo_2'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_excel['P3'][aux] = str(df_potConsumidaMesPer['Periodo_3'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_excel['P4'][aux] = str(df_potConsumidaMesPer['Periodo_4'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_excel['P5'][aux] = str(df_potConsumidaMesPer['Periodo_5'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_excel['P6'][aux] = str(df_potConsumidaMesPer['Periodo_6'][aux]).replace(
            '.', ',')

    return df_listaPotConsum, newTar, df_potConsumidaMesPer_excel


def df_excPotencia_NEWTAR(archivo, tarifa, region, potAux, tipoContador, cuartaHoraria, flag):
    potCont = [0, 0, 0, 0, 0, 0]
    if tarifa in ['3.0A', '3.1A'] and flag:
        if potAux[0] <= potAux[1] <= potAux[2]:
            potCont[0] = potAux[0]
            potCont[1] = potAux[1]
            potCont[2] = potAux[1]
            potCont[3] = potAux[1]
            potCont[4] = potAux[1]
            potCont[5] = potAux[2]
        elif potAux[0] <= potAux[1] >= potAux[2]:
            potCont[0] = potAux[0]
            potCont[1] = potAux[1]
            potCont[2] = potAux[1]
            potCont[3] = potAux[1]
            potCont[4] = potAux[1]
            potCont[5] = potAux[1]
        else:
            potCont[0] = potAux[0]
            potCont[1] = potAux[0]
            potCont[2] = potAux[0]
            potCont[3] = potAux[0]
            potCont[4] = potAux[0]
            potCont[5] = potAux[0]
    else:
        potCont[0] = potAux[0]
        potCont[1] = potAux[1]
        potCont[2] = potAux[2]
        potCont[3] = potAux[3]
        potCont[4] = potAux[4]
        potCont[5] = potAux[5]

    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    df_listaPotConsum, newTar, _ = df_potConsumida_NEWTAR(archivo, tarifa, region)

    try:
        potP1 = df_listaPotConsum.groupby('Periodo').get_group(1).reset_index(drop=True)
    except:
        potP1 = [0]

    try:
        potP2 = df_listaPotConsum.groupby('Periodo').get_group(2).reset_index(drop=True)
    except:
        potP2 = [0]

    try:
        potP3 = df_listaPotConsum.groupby('Periodo').get_group(3).reset_index(drop=True)
    except:
        potP3 = [0]

    try:
        potP4 = df_listaPotConsum.groupby('Periodo').get_group(4).reset_index(drop=True)
    except:
        potP4 = [0]

    try:
        potP5 = df_listaPotConsum.groupby('Periodo').get_group(5).reset_index(drop=True)
    except:
        potP5 = [0]

    try:
        potP6 = df_listaPotConsum.groupby('Periodo').get_group(6).reset_index(drop=True)
    except:
        potP6 = [0]

    IE = 1.051127  # Impuesto eléctrico
    t_EP = 1.4064  # Contaste de exceso de potencias

    sum_excesoP1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_excesoP2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_excesoP3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_excesoP4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_excesoP5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum_excesoP6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    cantidadExcesosP1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidadExcesosP2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidadExcesosP3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidadExcesosP4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidadExcesosP5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidadExcesosP6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    maxExcP1 = potCont[0]
    maxExcP2 = potCont[1]
    maxExcP3 = potCont[2]
    maxExcP4 = potCont[3]
    maxExcP5 = potCont[4]
    maxExcP6 = potCont[5]

    maximoExcesosP1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximoExcesosP2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximoExcesosP3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximoExcesosP4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximoExcesosP5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximoExcesosP6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if tipoContador == (4 or 5):
        auxP1 = 0
        auxP2 = 0
        auxP3 = 0
        auxP4 = 0
        auxP5 = 0
        auxP6 = 0

        if newTar == '2.0TD':
            try:
                for i in range(1, 13):
                    potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP1)):
                        if potConsumP1[k] > auxP1:
                            auxP1 = potConsumP1[k]
                        else:
                            pass
                    if auxP1 > potCont[0]:
                        sum_excesoP1[i - 1] += auxP1 - potCont[0]
                        auxP1 = 0
                    else:
                        sum_excesoP1[i - 1] += 0
                        auxP1 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

            try:
                for i in range(1, 13):
                    potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP2)):
                        if potConsumP2[k] > auxP2:
                            auxP2 = potConsumP2[k]
                        else:
                            pass
                    if auxP2 > potCont[1]:
                        sum_excesoP2[i - 1] += auxP2 - potCont[1]
                        auxP2 = 0
                    else:
                        sum_excesoP2[i - 1] += 0
                        auxP2 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

        else:  # Para el resto de tarifas, que tienen 6 periodos de potencia
            try:
                for i in range(1, 13):
                    potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP1)):
                        if potConsumP1[k] > auxP1:
                            auxP1 = potConsumP1[k]
                        else:
                            pass
                    if auxP1 > potCont[0]:
                        sum_excesoP1[i - 1] += auxP1 - potCont[0]
                        auxP1 = 0
                    else:
                        sum_excesoP1[i - 1] += 0
                        auxP1 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

            try:
                for i in range(1, 13):
                    potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP2)):
                        if potConsumP2[k] > auxP2:
                            auxP2 = potConsumP2[k]
                        else:
                            pass
                    if auxP2 > potCont[1]:
                        sum_excesoP2[i - 1] += auxP2 - potCont[1]
                        auxP2 = 0
                    else:
                        sum_excesoP2[i - 1] += 0
                        auxP2 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

            try:
                for i in range(1, 13):
                    potConsumP3 = potP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP3)):
                        if potConsumP3[k] > auxP3:
                            auxP3 = potConsumP3[k]
                        else:
                            pass
                    if auxP3 > potCont[2]:
                        sum_excesoP3[i - 1] += auxP3 - potCont[2]
                        auxP3 = 0
                    else:
                        sum_excesoP3[i - 1] += 0
                        auxP3 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P3')

            try:
                for i in range(1, 13):
                    potConsumP4 = potP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP4)):
                        if potConsumP4[k] > auxP4:
                            auxP4 = potConsumP4[k]
                        else:
                            pass
                    if auxP4 > potCont[3]:
                        sum_excesoP4[i - 1] += auxP4 - potCont[3]
                        auxP4 = 0
                    else:
                        sum_excesoP4[i - 1] += 0
                        auxP4 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P4')

            try:
                for i in range(1, 13):
                    potConsumP5 = potP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP5)):
                        if potConsumP5[k] > auxP5:
                            auxP5 = potConsumP5[k]
                        else:
                            pass
                    if auxP5 > potCont[4]:
                        sum_excesoP5[i - 1] += auxP5 - potCont[4]
                        auxP5 = 0
                    else:
                        sum_excesoP5[i - 1] += 0
                        auxP5 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P5')

            try:
                for i in range(1, 13):
                    potConsumP6 = potP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP6)):
                        if potConsumP6[k] > auxP6:
                            auxP6 = potConsumP6[k]
                        else:
                            pass
                    if auxP6 > potCont[5]:
                        sum_excesoP6[i - 1] += auxP6 - potCont[5]
                        auxP6 = 0
                    else:
                        sum_excesoP6[i - 1] += 0
                        auxP6 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P6')

    else:  # Para contadores tipo 1, 2 y 3, cálculos con curva CUARTAHORARIA si se tiene y sino con curva HORARIA*4

        if cuartaHoraria:

            if newTar == '2.0TD':

                try:  # PERIODO 1 -----------------------------------------------------------------
                    sum_cuartoP1 = 0
                    n_excP1 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP1)):
                                if potConsumP1[k] > potCont[0]:
                                    sum_cuartoP1 += (potConsumP1[k] - potCont[0]) ** 2
                                    n_excP1 += 1
                                    if potConsumP1[k] > maxExcP1:
                                        maxExcP1 = potConsumP1[k]
                                    else:
                                        pass
                                elif potConsumP1[k] <= potCont[0]:
                                    sum_cuartoP1 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P1')
                            sum_excesoP1[i - 1] += (sum_cuartoP1 ** 0.5)
                            cantidadExcesosP1[i - 1] += n_excP1
                            maximoExcesosP1[i - 1] += maxExcP1
                            sum_cuartoP1 = 0
                            n_excP1 = 0
                            maxExcP1 = potCont[0]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

                try:  # PERIODO 2 -----------------------------------------------------------------
                    sum_cuartoP2 = 0
                    n_excP2 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP2)):
                                if potConsumP2[k] > potCont[1]:
                                    sum_cuartoP2 += (potConsumP2[k] - potCont[1]) ** 2
                                    n_excP2 += 1
                                    if potConsumP2[k] > maxExcP2:
                                        maxExcP2 = potConsumP2[k]
                                    else:
                                        pass
                                elif potConsumP2[k] <= potCont[1]:
                                    sum_cuartoP2 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P2')
                            sum_excesoP2[i - 1] += (sum_cuartoP2 ** 0.5)
                            cantidadExcesosP2[i - 1] += n_excP2
                            maximoExcesosP2[i - 1] += maxExcP2
                            sum_cuartoP2 = 0
                            n_excP2 = 0
                            maxExcP2 = potCont[1]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

            else:  # Para el resto de tarifas, que tienen 6 periodos de potencia

                try:  # PERIODO 1 -----------------------------------------------------------------
                    sum_cuartoP1 = 0
                    n_excP1 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP1)):
                                if potConsumP1[k] > potCont[0]:
                                    sum_cuartoP1 += (potConsumP1[k] - potCont[0]) ** 2
                                    n_excP1 += 1
                                    if potConsumP1[k] > maxExcP1:
                                        maxExcP1 = potConsumP1[k]
                                    else:
                                        pass
                                elif potConsumP1[k] <= potCont[0]:
                                    sum_cuartoP1 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P1')
                            sum_excesoP1[i - 1] += (sum_cuartoP1 ** 0.5)
                            cantidadExcesosP1[i - 1] += n_excP1
                            maximoExcesosP1[i - 1] += maxExcP1
                            sum_cuartoP1 = 0
                            n_excP1 = 0
                            maxExcP1 = potCont[0]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

                try:  # PERIODO 2 -----------------------------------------------------------------
                    sum_cuartoP2 = 0
                    n_excP2 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP2)):
                                if potConsumP2[k] > potCont[1]:
                                    sum_cuartoP2 += (potConsumP2[k] - potCont[1]) ** 2
                                    n_excP2 += 1
                                    if potConsumP2[k] > maxExcP2:
                                        maxExcP2 = potConsumP2[k]
                                    else:
                                        pass
                                elif potConsumP2[k] <= potCont[1]:
                                    sum_cuartoP2 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P2')
                            sum_excesoP2[i - 1] += (sum_cuartoP2 ** 0.5)
                            cantidadExcesosP2[i - 1] += n_excP2
                            maximoExcesosP2[i - 1] += maxExcP2
                            sum_cuartoP2 = 0
                            n_excP2 = 0
                            maxExcP2 = potCont[1]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

                try:  # PERIODO 3 -----------------------------------------------------------------
                    sum_cuartoP3 = 0
                    n_excP3 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP3 = potP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP3)):
                                if potConsumP3[k] > potCont[2]:
                                    sum_cuartoP3 += (potConsumP3[k] - potCont[2]) ** 2
                                    n_excP3 += 1
                                    if potConsumP3[k] > maxExcP3:
                                        maxExcP3 = potConsumP3[k]
                                    else:
                                        pass
                                elif potConsumP3[k] <= potCont[2]:
                                    sum_cuartoP3 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P3')
                            sum_excesoP3[i - 1] += (sum_cuartoP3 ** 0.5)
                            cantidadExcesosP3[i - 1] += n_excP3
                            maximoExcesosP3[i - 1] += maxExcP3
                            sum_cuartoP3 = 0
                            n_excP3 = 0
                            maxExcP3 = potCont[2]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P3')

                try:  # PERIODO 4 -----------------------------------------------------------------
                    sum_cuartoP4 = 0
                    n_excP4 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP4 = potP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP4)):
                                if potConsumP4[k] > potCont[3]:
                                    sum_cuartoP4 += (potConsumP4[k] - potCont[3]) ** 2
                                    n_excP4 += 1
                                    if potConsumP4[k] > maxExcP4:
                                        maxExcP4 = potConsumP4[k]
                                    else:
                                        pass
                                elif potConsumP4[k] <= potCont[3]:
                                    sum_cuartoP4 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P4')
                            sum_excesoP4[i - 1] += (sum_cuartoP4 ** 0.5)
                            cantidadExcesosP4[i - 1] += n_excP4
                            maximoExcesosP4[i - 1] += maxExcP4
                            sum_cuartoP4 = 0
                            n_excP4 = 0
                            maxExcP4 = potCont[3]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P4')

                try:  # PERIODO 5 -----------------------------------------------------------------
                    sum_cuartoP5 = 0
                    n_excP5 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP5 = potP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP5)):
                                if potConsumP5[k] > potCont[4]:
                                    sum_cuartoP5 += (potConsumP5[k] - potCont[4]) ** 2
                                    n_excP5 += 1
                                    if potConsumP5[k] > maxExcP5:
                                        maxExcP5 = potConsumP5[k]
                                    else:
                                        pass
                                elif potConsumP5[k] <= potCont[4]:
                                    sum_cuartoP5 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P5')
                            sum_excesoP5[i - 1] += (sum_cuartoP5 ** 0.5)
                            cantidadExcesosP5[i - 1] += n_excP5
                            maximoExcesosP5[i - 1] += maxExcP5
                            sum_cuartoP5 = 0
                            n_excP5 = 0
                            maxExcP5 = potCont[4]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P5')

                try:  # PERIODO 6 -----------------------------------------------------------------
                    sum_cuartoP6 = 0
                    n_excP6 = 0
                    for i in range(1, 13):
                        try:
                            potConsumP6 = potP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                            for k in range(len(potConsumP6)):
                                if potConsumP6[k] > potCont[5]:
                                    sum_cuartoP6 += (potConsumP6[k] - potCont[5]) ** 2
                                    n_excP6 += 1
                                    if potConsumP6[k] > maxExcP6:
                                        maxExcP6 = potConsumP6[k]
                                    else:
                                        pass
                                elif potConsumP6[k] <= potCont[5]:
                                    sum_cuartoP6 += 0
                                else:
                                    print('ERROR DE SUMATORIOS EN P6')
                            sum_excesoP6[i - 1] += (sum_cuartoP6 ** 0.5)
                            cantidadExcesosP6[i - 1] += n_excP6
                            maximoExcesosP6[i - 1] += maxExcP6
                            sum_cuartoP6 = 0
                            n_excP6 = 0
                            maxExcP6 = potCont[5]
                        except:
                            pass
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P6')

        else:  # Si tenemos curva horaria para los contadores de tipo 1, 2 y 3

            if newTar == '2.0TD':

                try:
                    sum_horP1 = 0
                    for i in range(1, 13):
                        potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP1)):
                            if potConsumP1[k] > potCont[0]:
                                sum_horP1 += (4 * (potConsumP1[k] - potCont[0])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP1[i - 1] = (sum_horP1 ** 0.5) * \
                                              tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period1']
                        sum_horP1 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

                try:
                    sum_horP2 = 0
                    for i in range(1, 13):
                        potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Demandada'].reset_index(drop=True)
                        for k in range(len(potConsumP2)):
                            if potConsumP2[k] > potCont[1]:
                                sum_horP2 += (4 * (potConsumP2[k] - potCont[1])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP2[i - 1] = (sum_horP2 ** 0.5) * \
                                              tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period2']
                        sum_horP2 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

            else:  # Para el resto de tarifas, que tienen 6 periodos de potencia

                try:
                    sum_horP1 = 0
                    for i in range(1, 13):
                        potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP1)):
                            if potConsumP1[k] > potCont[0]:
                                sum_horP1 += (4 * (potConsumP1[k] - potCont[0])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP1[i - 1] = (sum_horP1 ** 0.5)
                        sum_horP1 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

                try:
                    sum_horP2 = 0
                    for i in range(1, 13):
                        potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP2)):
                            if potConsumP2[k] > potCont[1]:
                                sum_horP2 += (4 * (potConsumP2[k] - potCont[1])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP2[i - 1] = (sum_horP2 ** 0.5)
                        sum_horP2 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

                try:
                    sum_horP3 = 0
                    for i in range(1, 13):
                        potConsumP3 = potP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP3)):
                            if potConsumP3[k] > potCont[2]:
                                sum_horP3 += (4 * (potConsumP3[k] - potCont[2])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP3[i - 1] += (sum_horP3 ** 0.5)
                        sum_horP3 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P3')

                try:
                    sum_horP4 = 0
                    for i in range(1, 13):
                        potConsumP4 = potP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP4)):
                            if potConsumP4[k] > potCont[3]:
                                sum_horP4 += (4 * (potConsumP4[k] - potCont[3])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP4[i - 1] += (sum_horP4 ** 0.5)
                        sum_horP4 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P4')

                try:
                    sum_horP5 = 0
                    for i in range(1, 13):
                        potConsumP5 = potP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP5)):
                            if potConsumP5[k] > potCont[4]:
                                sum_horP5 += (4 * (potConsumP5[k] - potCont[4])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP5[i - 1] += (sum_horP5 ** 0.5)
                        sum_horP5 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P5')

                try:
                    sum_horP6 = 0
                    for i in range(1, 13):
                        potConsumP6 = potP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP6)):
                            if potConsumP6[k] > potCont[5]:
                                sum_horP6 += (4 * (potConsumP6[k] - potCont[5])) ** 2  # Replicamos exc. en 4 cuartos
                            else:
                                pass
                        sum_excesoP6[i - 1] += (sum_horP6 ** 0.5)
                        sum_horP6 = 0
                except:
                    print('ERROR CALCULANDO EXCESO DE POTENCIA EN P6')

    # Coste excesos
    sum_excesoP1.append(sum(sum_excesoP1))
    sum_excesoP2.append(sum(sum_excesoP2))
    sum_excesoP3.append(sum(sum_excesoP3))
    sum_excesoP4.append(sum(sum_excesoP4))
    sum_excesoP5.append(sum(sum_excesoP5))
    sum_excesoP6.append(sum(sum_excesoP6))

    # Numero de veces que nos hemos pasado (excedido)
    cantidadExcesosP1.append(sum(cantidadExcesosP1))
    cantidadExcesosP2.append(sum(cantidadExcesosP2))
    cantidadExcesosP3.append(sum(cantidadExcesosP3))
    cantidadExcesosP4.append(sum(cantidadExcesosP4))
    cantidadExcesosP5.append(sum(cantidadExcesosP5))
    cantidadExcesosP6.append(sum(cantidadExcesosP6))

    # Maximos excesos
    maximoExcesosP1.append(max(maximoExcesosP1))
    maximoExcesosP2.append(max(maximoExcesosP2))
    maximoExcesosP3.append(max(maximoExcesosP3))
    maximoExcesosP4.append(max(maximoExcesosP4))
    maximoExcesosP5.append(max(maximoExcesosP5))
    maximoExcesosP6.append(max(maximoExcesosP6))

    df_cantidadExcesos = pd.DataFrame(
        {
            'P1': cantidadExcesosP1,
            'P2': cantidadExcesosP2,
            'P3': cantidadExcesosP3,
            'P4': cantidadExcesosP4,
            'P5': cantidadExcesosP5,
            'P6': cantidadExcesosP6
        }, index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'TOTAL']
    )

    df_maximosExcesos = pd.DataFrame(
        {
            'P1': maximoExcesosP1,
            'P2': maximoExcesosP2,
            'P3': maximoExcesosP3,
            'P4': maximoExcesosP4,
            'P5': maximoExcesosP5,
            'P6': maximoExcesosP6
        }, index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'MAXIMO']
    )

    df_excPot = pd.DataFrame(
        {
            'Periodo_1': np.array(sum_excesoP1) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period1']),
            'Periodo_2': np.array(sum_excesoP2) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period2']),
            'Periodo_3': np.array(sum_excesoP3) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period3']),
            'Periodo_4': np.array(sum_excesoP4) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period4']),
            'Periodo_5': np.array(sum_excesoP5) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period5']),
            'Periodo_6': np.array(sum_excesoP6) * (tablesLOAD['ExcesoPotenciaCont123_NuevasTar'][newTar]['period6'])
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    if tipoContador == (4 or 5):
        df_excPot_conCtes = IE * t_EP * 2 * df_excPot
    else:
        df_excPot_conCtes = IE * t_EP * df_excPot

    # Adaptacion de los resultados para exportar a excel
    df_excPotenciaMesPer_excel = pd.DataFrame(
        {
            'P1': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P2': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P3': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P4': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P5': ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            'P6': ['', '', '', '', '', '', '', '', '', '', '', '', '']
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    for aux in range(0, 13):
        df_excPotenciaMesPer_excel['P1'][aux] = str(df_excPot_conCtes['Periodo_1'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_excel['P2'][aux] = str(df_excPot_conCtes['Periodo_2'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_excel['P3'][aux] = str(df_excPot_conCtes['Periodo_3'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_excel['P4'][aux] = str(df_excPot_conCtes['Periodo_4'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_excel['P5'][aux] = str(df_excPot_conCtes['Periodo_5'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_excel['P6'][aux] = str(df_excPot_conCtes['Periodo_6'][aux]).replace(
            '.', ',')

    return df_excPot_conCtes, df_excPotenciaMesPer_excel, df_cantidadExcesos, df_maximosExcesos


def df_terminoFijoPot_NEWTAR(tarifa, potAux, flag):
    potCont = [0, 0, 0, 0, 0, 0]
    if tarifa in ['3.0A', '3.1A'] and flag:
        if potAux[0] <= potAux[1] <= potAux[2]:
            potCont[0] = potAux[0]
            potCont[1] = potAux[1]
            potCont[2] = potAux[1]
            potCont[3] = potAux[1]
            potCont[4] = potAux[1]
            potCont[5] = potAux[2]
        elif potAux[0] <= potAux[1] >= potAux[2]:
            potCont[0] = potAux[0]
            potCont[1] = potAux[1]
            potCont[2] = potAux[1]
            potCont[3] = potAux[1]
            potCont[4] = potAux[1]
            potCont[5] = potAux[1]
        else:
            potCont[0] = potAux[0]
            potCont[1] = potAux[0]
            potCont[2] = potAux[0]
            potCont[3] = potAux[0]
            potCont[4] = potAux[0]
            potCont[5] = potAux[0]
    else:
        potCont[0] = potAux[0]
        potCont[1] = potAux[1]
        potCont[2] = potAux[2]
        potCont[3] = potAux[3]
        potCont[4] = potAux[4]
        potCont[5] = potAux[5]

    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    # Actualizacion de la tarifa antigua a las nuevas tarifas ---------------------------------------------------------
    newTar = tablesLOAD['CambioTarifa'][tarifa]
    if newTar == '2.0TD':
        newTar_periods = '2_0TD'  # Para trabajar con las configuraciones de tarifas
    elif newTar == '3.0TD':
        newTar_periods = '3_0TD'  # Para trabajar con las configuraciones de tarifas
    else:
        newTar_periods = '6_XTD'  # Para trabajar con las configuraciones de tarifas

    IE = 1.051127
    costeFijo = [0, 0, 0, 0, 0, 0]

    if newTar == '2.0TD':
        for i in range(len(potCont)):
            if i < 2:
                costeFijo[i] += potCont[i] * tablesLOAD['ATRpotencia_NT'][newTar][f'period{i + 1}']
            else:
                costeFijo[i] += 0
        df_costeFijo = pd.DataFrame(
            {
                'Periodo_1': costeFijo[0],
                'Periodo_2': costeFijo[1],
                'Periodo_3': costeFijo[2],
                'Periodo_4': costeFijo[3],
                'Periodo_5': costeFijo[4],
                'Periodo_6': costeFijo[5]
            }
            , index=['Coste Fijo']
        )
    else:
        for i in range(len(potCont)):
            costeFijo[i] += potCont[i] * tablesLOAD['ATRpotencia_NT'][newTar][f'period{i + 1}']
        df_costeFijo = pd.DataFrame(
            {
                'Periodo_1': costeFijo[0],
                'Periodo_2': costeFijo[1],
                'Periodo_3': costeFijo[2],
                'Periodo_4': costeFijo[3],
                'Periodo_5': costeFijo[4],
                'Periodo_6': costeFijo[5]
            }
            , index=['Coste Fijo']
        )

    df_costeFijo = df_costeFijo * IE

    # Adaptacion de los resultados para exportar a excel
    df_costeFijo_excel = pd.DataFrame(
        {
            'P1': [''],
            'P2': [''],
            'P3': [''],
            'P4': [''],
            'P5': [''],
            'P6': ['']
        }, index=['TOTAL']
    )

    try:
        df_costeFijo_excel['P1'][0] = str(df_costeFijo['Periodo_1'][0]).replace('.', ',')
        df_costeFijo_excel['P2'][0] = str(df_costeFijo['Periodo_2'][0]).replace('.', ',')
        df_costeFijo_excel['P3'][0] = str(df_costeFijo['Periodo_3'][0]).replace('.', ',')
        df_costeFijo_excel['P4'][0] = str(df_costeFijo['Periodo_4'][0]).replace('.', ',')
        df_costeFijo_excel['P5'][0] = str(df_costeFijo['Periodo_5'][0]).replace('.', ',')
        df_costeFijo_excel['P6'][0] = str(df_costeFijo['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los terminos fijos de potencia')

    return df_costeFijo, df_costeFijo_excel


def totalCostePotencia_NEWTAR(archivo, tarifa, region, pot, tipoContador, cuartaHoraria, flag):
    # Cargamos las diferentes funciones desarrolladas para calcular los costes totales y despues poder optimizar
    df_termFijo_calc, _ = df_terminoFijoPot_NEWTAR(tarifa, pot, flag)
    df_excPot_calc, _ = df_excPotencia_NEWTAR(archivo, tarifa, region, pot, tipoContador, cuartaHoraria, flag)

    df_COSTE_TOTAL = pd.DataFrame(
        {
            'Periodo_1': df_excPot_calc['Periodo_1'][-1] + df_termFijo_calc['Periodo_1'][0],
            'Periodo_2': df_excPot_calc['Periodo_2'][-1] + df_termFijo_calc['Periodo_2'][0],
            'Periodo_3': df_excPot_calc['Periodo_3'][-1] + df_termFijo_calc['Periodo_3'][0],
            'Periodo_4': df_excPot_calc['Periodo_4'][-1] + df_termFijo_calc['Periodo_4'][0],
            'Periodo_5': df_excPot_calc['Periodo_5'][-1] + df_termFijo_calc['Periodo_5'][0],
            'Periodo_6': df_excPot_calc['Periodo_6'][-1] + df_termFijo_calc['Periodo_6'][0]
        }, index=['TOTAL']
    )

    df_COSTE_TOTAL = df_COSTE_TOTAL.round(2)

    df_COSTE_TOTAL_excel = pd.DataFrame(
        {
            'P1': [''],
            'P2': [''],
            'P3': [''],
            'P4': [''],
            'P5': [''],
            'P6': ['']
        }, index=['TOTAL']
    )

    try:
        df_COSTE_TOTAL_excel['P1'][0] = str(df_COSTE_TOTAL['Periodo_1'][0]).replace('.', ',')
        df_COSTE_TOTAL_excel['P2'][0] = str(df_COSTE_TOTAL['Periodo_2'][0]).replace('.', ',')
        df_COSTE_TOTAL_excel['P3'][0] = str(df_COSTE_TOTAL['Periodo_3'][0]).replace('.', ',')
        df_COSTE_TOTAL_excel['P4'][0] = str(df_COSTE_TOTAL['Periodo_4'][0]).replace('.', ',')
        df_COSTE_TOTAL_excel['P5'][0] = str(df_COSTE_TOTAL['Periodo_5'][0]).replace('.', ',')
        df_COSTE_TOTAL_excel['P6'][0] = str(df_COSTE_TOTAL['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los costes totales de potencia nuevas tarifas')

    return df_COSTE_TOTAL, df_COSTE_TOTAL_excel


def optimizacionPotencias(archivo, tarifa, region, pot, tipoContador, cuartaHoraria, flag):
    # VALORES INICIALES
    df_EP_ini, _, _, _ = df_excPotencia_NEWTAR(archivo, tarifa, region, pot, tipoContador, cuartaHoraria, flag)
    df_TF_ini, _ = df_terminoFijoPot_NEWTAR(tarifa, pot, flag)

    x0 = np.zeros(6)

    if tarifa in ['3.0A', '3.1A']:
        if pot[0] <= pot[1] <= pot[2]:
            x0[0] = pot[0]
            x0[1] = pot[1]
            x0[2] = pot[1]
            x0[3] = pot[1]
            x0[4] = pot[1]
            x0[5] = pot[2]
        elif pot[0] <= pot[1] >= pot[2]:
            x0[0] = pot[0]
            x0[1] = pot[1]
            x0[2] = pot[1]
            x0[3] = pot[1]
            x0[4] = pot[1]
            x0[5] = pot[1]
        else:
            x0[0] = pot[0]
            x0[1] = pot[0]
            x0[2] = pot[0]
            x0[3] = pot[0]
            x0[4] = pot[0]
            x0[5] = pot[0]
    else:
        x0[0] = pot[0]
        x0[1] = pot[1]
        x0[2] = pot[2]
        x0[3] = pot[3]
        x0[4] = pot[4]
        x0[5] = pot[5]

    EP0_p1 = df_EP_ini['Periodo_1'][-1]
    EP0_p2 = df_EP_ini['Periodo_2'][-1]
    EP0_p3 = df_EP_ini['Periodo_3'][-1]
    EP0_p4 = df_EP_ini['Periodo_4'][-1]
    EP0_p5 = df_EP_ini['Periodo_5'][-1]
    EP0_p6 = df_EP_ini['Periodo_6'][-1]
    EP0_total = EP0_p1 + EP0_p2 + EP0_p3 + EP0_p4 + EP0_p5 + EP0_p6

    TF0_p1 = df_TF_ini['Periodo_1'][-1]
    TF0_p2 = df_TF_ini['Periodo_2'][-1]
    TF0_p3 = df_TF_ini['Periodo_3'][-1]
    TF0_p4 = df_TF_ini['Periodo_4'][-1]
    TF0_p5 = df_TF_ini['Periodo_5'][-1]
    TF0_p6 = df_TF_ini['Periodo_6'][-1]
    TF0_total = TF0_p1 + TF0_p2 + TF0_p3 + TF0_p4 + TF0_p5 + TF0_p6

    f0 = EP0_total + TF0_total

    # FUNCION A MINIMIZAR
    def objetivo(x):
        df_EP_opt, _, _, _ = df_excPotencia_NEWTAR(archivo, tarifa, region, x, tipoContador, cuartaHoraria, False)
        df_TF_opt, _ = df_terminoFijoPot_NEWTAR(tarifa, x, False)

        EP_opt_p1 = df_EP_opt['Periodo_1'][-1]
        EP_opt_p2 = df_EP_opt['Periodo_2'][-1]
        EP_opt_p3 = df_EP_opt['Periodo_3'][-1]
        EP_opt_p4 = df_EP_opt['Periodo_4'][-1]
        EP_opt_p5 = df_EP_opt['Periodo_5'][-1]
        EP_opt_p6 = df_EP_opt['Periodo_6'][-1]
        EP_opt_total = EP_opt_p1 + EP_opt_p2 + EP_opt_p3 + EP_opt_p4 + EP_opt_p5 + EP_opt_p6

        TF_opt_p1 = df_TF_opt['Periodo_1'][-1]
        TF_opt_p2 = df_TF_opt['Periodo_2'][-1]
        TF_opt_p3 = df_TF_opt['Periodo_3'][-1]
        TF_opt_p4 = df_TF_opt['Periodo_4'][-1]
        TF_opt_p5 = df_TF_opt['Periodo_5'][-1]
        TF_opt_p6 = df_TF_opt['Periodo_6'][-1]
        TF_opt_total = TF_opt_p1 + TF_opt_p2 + TF_opt_p3 + TF_opt_p4 + TF_opt_p5 + TF_opt_p6

        f_opt = EP_opt_total + TF_opt_total

        return f_opt

    # RESTRICCIONES DE INECUACIONES A TENER EN CUENTA
    def constraint1_ineq(x):
        return x[1] - x[0]

    con1_ineq = {'type': 'ineq', 'fun': constraint1_ineq}

    def constraint2_ineq(x):
        return x[2] - x[1]

    con2_ineq = {'type': 'ineq', 'fun': constraint2_ineq}

    def constraint3_ineq(x):
        return x[3] - x[2]

    con3_ineq = {'type': 'ineq', 'fun': constraint3_ineq}

    def constraint4_ineq(x):
        return x[4] - x[3]

    con4_ineq = {'type': 'ineq', 'fun': constraint4_ineq}

    def constraint5_ineq(x):
        return x[5] - x[4]

    con5_ineq = {'type': 'ineq', 'fun': constraint5_ineq}

    def constraint6_ineq(x):
        return f0 - objetivo(x)

    con6_ineq = {'type': 'ineq', 'fun': constraint6_ineq}

    cons = ([con1_ineq, con2_ineq, con3_ineq, con4_ineq, con5_ineq, con6_ineq])

    # RESTRICCIONES DE LIMITES A TENER EN CUENTA
    b = (0.0, None)
    bnds = (b, b, b, b, b, b)

    # OPTIMIZACIÓN
    sol = minimize(objetivo, x0, args=(), method='SLSQP', jac=None, bounds=bnds, constraints=cons, tol=None,
                   callback=None, options={'maxiter': 200, 'ftol': 1e-10, 'iprint': 1, 'disp': True,
                                           'eps': 1.4901161193847656e-08, 'finite_diff_rel_step': None})

    # REDONDEO A LA UNIDAD DE LOS VALORES DE POTENCIA OPTIMIZADOS
    potOpt = [0, 0, 0, 0, 0, 0]
    for i in range(0, 6):
        potOpt[i] = round(sol.x[i], 1)
    return potOpt

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
