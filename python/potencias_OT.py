# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ IMPORTS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
# Imports de los paths para las direcciones de la NAS
import sys
import os

if os.path.exists('C:/'):
    sys.path.insert(0, 'C:\xampp\htdocs\ingebau\formulario\excel_python')
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

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES CLASIFICACIÓN DE DIAS Y OBTENCIÓN DE PERIODOS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#


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


# Función que me devuelve si el dia pertenece a la temporada de verano/invierno de las antiguas tarifas
def type_day(day):
    """
    Return the type of the day (0 for invierno, 1 for Verano)
    """
    list_change_hour = [
        dt(2015, 3, 29, 2),
        dt(2015, 10, 25, 2),
        dt(2016, 3, 27, 2),
        dt(2016, 10, 30, 2),
        dt(2017, 3, 26, 2),
        dt(2017, 10, 29, 2),
        dt(2018, 3, 25, 2),
        dt(2018, 10, 28, 2),
        dt(2019, 3, 31, 2),
        dt(2019, 10, 27, 2),
        dt(2020, 3, 29, 2),
        dt(2020, 10, 25, 2),
        dt(2021, 3, 28, 2),
        dt(2021, 10, 31, 2),
        dt(2022, 3, 27, 2),
        dt(2022, 10, 30, 2)
    ]
    for i in range(len(list_change_hour) - 1):
        if day >= list_change_hour[i] and day < list_change_hour[i + 1]:
            if list_change_hour[i].month == 3:
                return 1
            else:
                return 0

    return 1


# Funcion que me devuelve el nombre del mes para su uso en las configuraciones y propiedades
def which_month(d):
    """
    Return the name of the month
    """
    if d.month == 1:
        return 'Enero'
    elif d.month == 2:
        return 'Febrero'
    elif d.month == 3:
        return 'Marzo'
    elif d.month == 4:
        return 'Abril'
    elif d.month == 5:
        return 'Mayo'
    elif d.month == 6:
        return 'Junio'
    elif d.month == 7:
        return 'Julio'
    elif d.month == 8:
        return 'Agosto'
    elif d.month == 9:
        return 'Septiembre'
    elif d.month == 10:
        return 'Octubre'
    elif d.month == 11:
        return 'Noviembre'
    elif d.month == 12:
        return 'Diciembre'


# Función que me devuelve el periodo tarifario de POTENCIAS del dia y sus horas
def get_period_OLDTARp(config, d, season):
    if config["tarifas"][0] == '6':
        month = which_month(d)
        if month == 'Junio':
            if d.day < 15:
                month = 'Junio_deb'
            else:
                month = 'Junio_end'
        periods_config = config[month]
    else:
        if season == 1:
            periods_config = config['Verano']
        else:
            periods_config = config['Invierno']
    try:
        if is_working_day(d):
            periods_config = periods_config["Semana"]
        else:
            periods_config = periods_config["Finde"]
    except:
        pass
    for period in periods_config:
        if in_period(d, periods_config[period]):
            return config["Periodo"][period]
        elif in_period(d, periods_config[period]):
            return config["Perido"][period]


# Funcon que me devuelve un string para usar en configuraciones de tarifas
def tarifa_to_type_tarifa(tarifa):
    """
    Transform the tarifa to the type of tarifa
    """
    if tarifa == '2.0A':
        type_tarifa = '2X_A'
    elif tarifa == '2.0DHA':
        type_tarifa = '2X_DHA'
    elif tarifa == '2.1A':
        type_tarifa = '2X_A'
    elif tarifa == '2.1DHA':
        type_tarifa = '2X_DHA'
    elif tarifa == '2.0DHS':
        type_tarifa = '2X_DHS'
    elif tarifa == '2.1DHS':
        type_tarifa = '2X_DHS'
    elif tarifa == '3.0A':
        type_tarifa = '3_0A'
    elif tarifa == '3.1A':
        type_tarifa = '3_1A'
    elif tarifa == '6.1A':
        type_tarifa = '6_1'
    elif tarifa == '6.2':
        type_tarifa = '6_2'
    elif tarifa == '6.3':
        type_tarifa = '6_3'
    elif tarifa == '6.4':
        type_tarifa = '6_4'
    elif tarifa == '6.1B':
        type_tarifa = '6_1'
    else:
        raise Exception(f'Tarifa {tarifa} does not exist')

    return type_tarifa


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES PRINCIPALES DE CÁLCULOS PEDIDOS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

def df_potConsumida_OLDTAR(archivo, tarifa, region):
    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    tar_periods = tarifa_to_type_tarifa(tarifa)

    # Cargamos configuraciones para la tarifa de entrada --------------------------------------------------------------
    if region == 'peninsula':
        with open(f'{ph.path_config_perdidas}/{tar_periods}.json') as config:
            config_perLOAD = js.load(config)
    else:
        with open(f'{ph.path_config_perdidas_canarias}/{tar_periods}.json') as config:
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
        period.append(get_period_OLDTARp(config_perLOAD, list_Date[j], type_day(list_Date[j])))
        fecha.append(list_Date[j])
        mes.append(list_Date[j].month)
        tempor.append(type_day(list_Date[j]))
        potenConsum.append(float(list_PotConsum[j]))

    df_listaPotConsum_oldTar = pd.DataFrame(
        {
            "Periodo": period,
            "Fecha": fecha,
            "Mes": mes,
            "Temporada": tempor,
            "Potencia Consumida": potenConsum
        }
    )

    try:
        pot_ConsumP1 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(1).reset_index(drop=True)
    except:
        pot_ConsumP1 = 0

    try:
        pot_ConsumP2 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(2).reset_index(drop=True)
    except:
        pot_ConsumP2 = 0

    try:
        pot_ConsumP3 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(3).reset_index(drop=True)
    except:
        pot_ConsumP3 = 0

    try:
        pot_ConsumP4 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(4).reset_index(drop=True)
    except:
        pot_ConsumP4 = 0

    try:
        pot_ConsumP5 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(5).reset_index(drop=True)
    except:
        pot_ConsumP5 = 0

    try:
        pot_ConsumP6 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(6).reset_index(drop=True)
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
    df_potConsumidaMesPer_oldTar_EXCEL = pd.DataFrame(
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
        df_potConsumidaMesPer_oldTar_EXCEL['P1'][aux] = str(
            df_potConsumidaMesPer['Periodo_1'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_oldTar_EXCEL['P2'][aux] = str(
            df_potConsumidaMesPer['Periodo_2'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_oldTar_EXCEL['P3'][aux] = str(
            df_potConsumidaMesPer['Periodo_3'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_oldTar_EXCEL['P4'][aux] = str(
            df_potConsumidaMesPer['Periodo_4'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_oldTar_EXCEL['P5'][aux] = str(
            df_potConsumidaMesPer['Periodo_5'][aux]).replace(
            '.', ',')
        df_potConsumidaMesPer_oldTar_EXCEL['P6'][aux] = str(
            df_potConsumidaMesPer['Periodo_6'][aux]).replace(
            '.', ',')

    return df_listaPotConsum_oldTar, tar_periods, df_potConsumidaMesPer_oldTar_EXCEL


def df_excPotencia_OLDTAR(archivo, tarifa, region, potCont, tipoContador, cuartaHoraria):
    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    df_listaPotConsum_oldTar, oldTar, _ = df_potConsumida_OLDTAR(archivo, tarifa, region)

    try:
        potP1 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(1).reset_index(drop=True)
    except:
        potP1 = [0]

    try:
        potP2 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(2).reset_index(drop=True)
    except:
        potP2 = [0]

    try:
        potP3 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(3).reset_index(drop=True)
    except:
        potP3 = [0]

    try:
        potP4 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(4).reset_index(drop=True)
    except:
        potP4 = [0]

    try:
        potP5 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(5).reset_index(drop=True)
    except:
        potP5 = [0]

    try:
        potP6 = df_listaPotConsum_oldTar.groupby('Periodo').get_group(6).reset_index(drop=True)
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

    if oldTar in ['2X_A', '2X_DHA', '2X_DHS', '3_0A', '3_1A']:
        auxP1 = 0
        auxP2 = 0
        auxP3 = 0
        auxP4 = 0
        auxP5 = 0
        auxP6 = 0

        ATR_oldTar_P1 = tablesLOAD['ATRpotencia_OT'][tarifa]['period1']    #59.173468
        ATR_oldTar_P2 = tablesLOAD['ATRpotencia_OT'][tarifa]['period2']    #36.490689
        ATR_oldTar_P3 = tablesLOAD['ATRpotencia_OT'][tarifa]['period3']    #8.367731

        try:
            for i in range(1, 13):
                try:
                    potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)

                    if cuartaHoraria:
                        numeroDiasP1 = len(potConsumP1) / (24 * 4)
                    else:
                        numeroDiasP1 = len(potConsumP1) / 24

                    cteP1 = ATR_oldTar_P1 #* (numeroDiasP1 / 365)

                    for k in range(len(potConsumP1)):
                        if potConsumP1[k] > auxP1:
                            auxP1 = potConsumP1[k]  # Maximo consumo cuartohorario
                        else:
                            pass
                    if auxP1 <= 0.85 * potCont[0]:
                        potCobrarP1_caso1 = 0.85 * potCont[0]
                        sum_excesoP1[i - 1] += (potCobrarP1_caso1 - potCont[0]) * cteP1
                        auxP1 = 0

                    elif 0.85 * potCont[0] < auxP1 <= 1.05 * potCont[0]:
                        potCobrarP1_caso2 = auxP1
                        sum_excesoP1[i - 1] += (potCobrarP1_caso2 - potCont[0]) * cteP1
                        auxP1 = 0
                    else:
                        potCobrarP1_caso3 = auxP1 + 2 * (auxP1 - 1.05 * potCont[0])
                        sum_excesoP1[i - 1] += (potCobrarP1_caso3 - potCont[0]) * cteP1
                        auxP1 = 0
                except:
                    sum_excesoP1[i - 1] = 0

                try:
                    potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)

                    if cuartaHoraria:
                        numeroDiasP2 = len(potConsumP2) / (24 * 4)
                    else:
                        numeroDiasP2 = len(potConsumP2) / 24

                    cteP2 = ATR_oldTar_P2 #* numeroDiasP2 / 365

                    for k in range(len(potConsumP2)):
                        if potConsumP2[k] > auxP2:
                            auxP2 = potConsumP2[k]
                        else:
                            pass
                    if auxP2 <= 0.85 * potCont[1]:
                        potCobrarP2_caso1 = 0.85 * potCont[1]
                        sum_excesoP2[i - 1] += (potCobrarP2_caso1 - potCont[1]) * cteP2
                        auxP2 = 0

                    elif 0.85 * potCont[1] < auxP2 <= 1.05 * potCont[1]:
                        potCobrarP2_caso2 = auxP2
                        sum_excesoP2[i - 1] += (potCobrarP2_caso2 - potCont[1]) * cteP2
                        auxP2 = 0
                    else:
                        potCobrarP2_caso3 = auxP2 + 2 * (auxP2 - 1.05 * potCont[1])
                        sum_excesoP2[i - 1] += (potCobrarP2_caso3 - potCont[1]) * cteP2
                        auxP2 = 0
                except:
                    sum_excesoP2[i - 1] = 0

                try:
                    potConsumP3 = potP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)

                    if cuartaHoraria:
                        numeroDiasP3 = len(potConsumP3) / (23 * 4)
                    else:
                        numeroDiasP3 = len(potConsumP3) / 23

                    cteP3 = ATR_oldTar_P3 #* numeroDiasP3 / 365

                    for k in range(len(potConsumP3)):
                        if potConsumP3[k] > auxP3:
                            auxP3 = potConsumP3[k]
                        else:
                            pass
                    if auxP3 <= 0.85 * potCont[2]:
                        potCobrarP3_caso1 = 0.85 * potCont[2]
                        sum_excesoP3[i - 1] += (potCobrarP3_caso1 - potCont[2]) * cteP3
                        auxP3 = 0

                    elif 0.85 * potCont[2] < auxP3 <= 1.05 * potCont[2]:
                        potCobrarP3_caso2 = auxP3
                        sum_excesoP3[i - 1] += (potCobrarP3_caso2 - potCont[2]) * cteP3
                        auxP3 = 0
                    else:
                        potCobrarP3_caso3 = auxP3 + 2 * (auxP3 - 1.05 * potCont[2])
                        sum_excesoP3[i - 1] += (potCobrarP3_caso3 - potCont[2]) * cteP3
                        auxP3 = 0
                except:
                    sum_excesoP3[i - 1] = 0

                try:
                    potConsumP4 = potP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP4)):
                        if potConsumP4[k] > auxP4:
                            auxP4 = potConsumP4[k]
                        else:
                            pass
                    if auxP4 <= 0.85 * potCont[3]:
                        sum_excesoP4[i - 1] -= 0.15 * potCont[3]
                        auxP4 = 0

                    elif 0.85 * potCont[3] < auxP4 <= 1.05 * potCont[3]:
                        sum_excesoP4[i - 1] -= abs(auxP4 - potCont[3])
                        auxP4 = 0
                    else:
                        sum_excesoP4[i - 1] += abs(auxP4 - potCont[3]) + 2 * abs(auxP4 - 1.05 * potCont[3])
                        auxP4 = 0
                except:
                    sum_excesoP4[i - 1] = 0

                try:
                    potConsumP5 = potP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP5)):
                        if potConsumP5[k] > auxP5:
                            auxP5 = potConsumP5[k]
                        else:
                            pass
                    if auxP5 <= 0.85 * potCont[4]:
                        sum_excesoP5[i - 1] -= 0.15 * potCont[4]
                        auxP5 = 0

                    elif 0.85 * potCont[4] < auxP5 <= 1.05 * potCont[4]:
                        sum_excesoP5[i - 1] -= abs(auxP5 - potCont[4])
                        auxP5 = 0
                    else:
                        sum_excesoP5[i - 1] += abs(auxP5 - potCont[4]) + 2 * abs(auxP5 - 1.05 * potCont[4])
                        auxP5 = 0
                except:
                    sum_excesoP5[i - 1] = 0

                try:
                    potConsumP6 = potP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP6)):
                        if potConsumP6[k] > auxP6:
                            auxP6 = potConsumP6[k]
                        else:
                            pass
                    if auxP6 <= 0.85 * potCont[5]:
                        sum_excesoP6[i - 1] -= 0.15 * potCont[5]
                        auxP6 = 0

                    elif 0.85 * potCont[5] < auxP6 <= 1.05 * potCont[5]:
                        sum_excesoP6[i - 1] -= abs(auxP6 - potCont[5])
                        auxP6 = 0
                    else:
                        sum_excesoP6[i - 1] += abs(auxP6 - potCont[5]) + 2 * abs(auxP6 - 1.05 * potCont[5])
                        auxP6 = 0
                except:
                    sum_excesoP6[i - 1] = 0
        except:
            print('ERROR CALCULANDO EXCESOS DE POTENCIAS PARA LAS TARIFAS ANTIGUAS')
    else:
        if cuartaHoraria:
            try:  # PERIODO 1 -----------------------------------------------------------------
                sum_cuartoP1 = 0
                # numP1 = 0
                for i in range(1, 13):
                    try:
                        potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP1)):
                            if potConsumP1[k] > potCont[0]:
                                sum_cuartoP1 += (potConsumP1[k] - potCont[0]) ** 2
                                # numP1 += 1
                            elif potConsumP1[k] <= potCont[0]:
                                sum_cuartoP1 += 0
                                # numP1 += 1
                            else:
                                print('ERROR DE SUMATORIOS EN P1')
                        sum_excesoP1[i - 1] += (sum_cuartoP1 ** 0.5) * 1.406 * 1
                        sum_cuartoP1 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P1')

            try:  # PERIODO 2 -----------------------------------------------------------------
                sum_cuartoP2 = 0
                # numP2 = 0
                for i in range(1, 13):
                    try:
                        potConsumP2 = potP2.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP2)):
                            if potConsumP2[k] > potCont[1]:  # and numP2 < 4
                                sum_cuartoP2 += (potConsumP2[k] - potCont[1]) ** 2
                                # numP2 += 1
                            elif potConsumP2[k] <= potCont[1]:  # and numP2 < 4
                                sum_cuartoP2 += 0
                                # numP2 += 1
                            else:
                                print('ERROR DE SUMATORIOS EN P2')
                        sum_excesoP2[i - 1] += (sum_cuartoP2 ** 0.5) * 1.406 * 0.5
                        sum_cuartoP2 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P2')

            try:  # PERIODO 3 -----------------------------------------------------------------
                sum_cuartoP3 = 0
                for i in range(1, 13):
                    try:
                        potConsumP3 = potP3.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP3)):
                            if potConsumP3[k] > potCont[2]:
                                sum_cuartoP3 += (potConsumP3[k] - potCont[2]) ** 2
                            elif potConsumP3[k] <= potCont[2]:
                                sum_cuartoP3 += 0
                            else:
                                print('ERROR DE SUMATORIOS EN P3')
                        sum_excesoP3[i - 1] += (sum_cuartoP3 ** 0.5) * 1.406 * 0.37
                        sum_cuartoP3 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P3')

            try:  # PERIODO 4 -----------------------------------------------------------------
                sum_cuartoP4 = 0
                for i in range(1, 13):
                    try:
                        potConsumP4 = potP4.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP4)):
                            if potConsumP4[k] > potCont[3]:
                                sum_cuartoP4 += (potConsumP4[k] - potCont[3]) ** 2
                            elif potConsumP4[k] <= potCont[3]:
                                sum_cuartoP4 += 0
                            else:
                                print('ERROR DE SUMATORIOS EN P4')
                        sum_excesoP4[i - 1] += (sum_cuartoP4 ** 0.5) * 1.406 * 0.37
                        sum_cuartoP4 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P4')

            try:  # PERIODO 5 -----------------------------------------------------------------
                sum_cuartoP5 = 0
                for i in range(1, 13):
                    try:
                        potConsumP5 = potP5.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP5)):
                            if potConsumP5[k] > potCont[4]:
                                sum_cuartoP5 += (potConsumP5[k] - potCont[4]) ** 2
                            elif potConsumP5[k] <= potCont[4]:
                                sum_cuartoP5 += 0
                            else:
                                print('ERROR DE SUMATORIOS EN P5')
                        sum_excesoP5[i - 1] += (sum_cuartoP5 ** 0.5) * 1.406 * 0.37
                        sum_cuartoP5 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P5')

            try:  # PERIODO 6 -----------------------------------------------------------------
                sum_cuartoP6 = 0
                for i in range(1, 13):
                    try:
                        potConsumP6 = potP6.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                        for k in range(len(potConsumP6)):
                            if potConsumP6[k] > potCont[5]:
                                sum_cuartoP6 += (potConsumP6[k] - potCont[5]) ** 2
                            elif potConsumP6[k] <= potCont[5]:
                                sum_cuartoP6 += 0
                            else:
                                print('ERROR DE SUMATORIOS EN P6')
                        sum_excesoP6[i - 1] += (sum_cuartoP6 ** 0.5) * 1.406 * 0.17
                        sum_cuartoP6 = 0
                    except:
                        pass
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P6')

        else:
            try:
                sum_horP1 = 0
                for i in range(1, 13):
                    potConsumP1 = potP1.groupby('Mes').get_group(i)['Potencia Consumida'].reset_index(drop=True)
                    for k in range(len(potConsumP1)):
                        if potConsumP1[k] > potCont[0]:
                            sum_horP1 += (4 * (potConsumP1[k] - potCont[0])) ** 2  # Replicamos exc. en 4 cuartos
                        else:
                            pass
                    sum_excesoP1[i - 1] = (sum_horP1 ** 0.5) * 1.406368 * 1
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
                    sum_excesoP2[i - 1] = (sum_horP2 ** 0.5) * 1.406368 * 0.5
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
                    sum_excesoP3[i - 1] += (sum_horP3 ** 0.5) * 1.406368 * 0.37
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
                    sum_excesoP4[i - 1] += (sum_horP4 ** 0.5) * 1.406368 * 0.37
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
                    sum_excesoP5[i - 1] += (sum_horP5 ** 0.5) * 1.406368 * 0.37
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
                    sum_excesoP6[i - 1] += (sum_horP6 ** 0.5) * 1.406368 * 0.17
                    sum_horP6 = 0
            except:
                print('ERROR CALCULANDO EXCESO DE POTENCIA EN P6')

    sum_excesoP1.append(sum(sum_excesoP1))
    sum_excesoP2.append(sum(sum_excesoP2))
    sum_excesoP3.append(sum(sum_excesoP3))
    sum_excesoP4.append(sum(sum_excesoP4))
    sum_excesoP5.append(sum(sum_excesoP5))
    sum_excesoP6.append(sum(sum_excesoP6))

    IE = 1.051127

    df_excPotMesPer_oldTar = pd.DataFrame(
        {
            'Periodo_1': sum_excesoP1,
            'Periodo_2': sum_excesoP2,
            'Periodo_3': sum_excesoP3,
            'Periodo_4': sum_excesoP4,
            'Periodo_5': sum_excesoP5,
            'Periodo_6': sum_excesoP6
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    if oldTar in ['2X_A', '2X_DHA', '2X_DHS', '3_0A', '3_1A']:
        df_excPotMesPer_oldTar = df_excPotMesPer_oldTar * IE / 12
    else:
        df_excPotMesPer_oldTar = df_excPotMesPer_oldTar * IE

    # Adaptacion de los resultados para exportar a excel
    df_excPotenciaMesPer_oldTar_EXCEL = pd.DataFrame(
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
        df_excPotenciaMesPer_oldTar_EXCEL['P1'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_1'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_oldTar_EXCEL['P2'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_2'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_oldTar_EXCEL['P3'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_3'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_oldTar_EXCEL['P4'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_4'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_oldTar_EXCEL['P5'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_5'][aux]).replace(
            '.', ',')
        df_excPotenciaMesPer_oldTar_EXCEL['P6'][aux] = str(
            df_excPotMesPer_oldTar['Periodo_6'][aux]).replace(
            '.', ',')

    return df_excPotMesPer_oldTar, df_excPotenciaMesPer_oldTar_EXCEL


def df_terminoFijoPot_OLDTAR(tarifa, potCont):
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    IE = 1.051127
    costeFijo = [0, 0, 0, 0, 0, 0]

    for i in range(len(potCont)):
        costeFijo[i] += potCont[i] * tablesLOAD['ATRpotencia_OT'][tarifa][f'period{i + 1}']

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

    df_costeFijo_oldTar = df_costeFijo * IE

    # Adaptacion de los resultados para exportar a excel
    df_costeFijo_oldTar_EXCEL = pd.DataFrame(
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
        df_costeFijo_oldTar_EXCEL['P1'][0] = str(df_costeFijo_oldTar['Periodo_1'][0]).replace('.', ',')
        df_costeFijo_oldTar_EXCEL['P2'][0] = str(df_costeFijo_oldTar['Periodo_2'][0]).replace('.', ',')
        df_costeFijo_oldTar_EXCEL['P3'][0] = str(df_costeFijo_oldTar['Periodo_3'][0]).replace('.', ',')
        df_costeFijo_oldTar_EXCEL['P4'][0] = str(df_costeFijo_oldTar['Periodo_4'][0]).replace('.', ',')
        df_costeFijo_oldTar_EXCEL['P5'][0] = str(df_costeFijo_oldTar['Periodo_5'][0]).replace('.', ',')
        df_costeFijo_oldTar_EXCEL['P6'][0] = str(df_costeFijo_oldTar['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los terminos fijos de potencia')

    return df_costeFijo_oldTar, df_costeFijo_oldTar_EXCEL


def totalCostePotencia_OLDTAR(archivo, tarifa, region, potCont, tipoContador, cuartaHoraria):
    # CARGAMOS LOS COSTES DE EXCESOS DE POTENCIA PARA LAS TARIFAS ANTIGUAS
    df_excPotMesPer_oldTar, _ = df_excPotencia_OLDTAR(archivo, tarifa, region, potCont, tipoContador, cuartaHoraria)
    # CARGAMOS LOS COSTES DEL TERMINO FIJO DE POTENCIA
    df_costeFijo_oldTar, _ = df_terminoFijoPot_OLDTAR(tarifa, potCont)

    df_COSTE_TOTAL = pd.DataFrame(
        {
            'Periodo_1': df_excPotMesPer_oldTar['Periodo_1'][-1] + df_costeFijo_oldTar['Periodo_1'][0],
            'Periodo_2': df_excPotMesPer_oldTar['Periodo_2'][-1] + df_costeFijo_oldTar['Periodo_2'][0],
            'Periodo_3': df_excPotMesPer_oldTar['Periodo_3'][-1] + df_costeFijo_oldTar['Periodo_3'][0],
            'Periodo_4': df_excPotMesPer_oldTar['Periodo_4'][-1] + df_costeFijo_oldTar['Periodo_4'][0],
            'Periodo_5': df_excPotMesPer_oldTar['Periodo_5'][-1] + df_costeFijo_oldTar['Periodo_5'][0],
            'Periodo_6': df_excPotMesPer_oldTar['Periodo_6'][-1] + df_costeFijo_oldTar['Periodo_6'][0]
        }, index=['TOTAL']
    )

    df_COSTE_TOTAL_oldTar = df_COSTE_TOTAL.round(2)

    df_COSTE_TOTAL_oldTar_EXCEL = pd.DataFrame(
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
        df_COSTE_TOTAL_oldTar_EXCEL['P1'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_1'][0]).replace('.', ',')
        df_COSTE_TOTAL_oldTar_EXCEL['P2'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_2'][0]).replace('.', ',')
        df_COSTE_TOTAL_oldTar_EXCEL['P3'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_3'][0]).replace('.', ',')
        df_COSTE_TOTAL_oldTar_EXCEL['P4'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_4'][0]).replace('.', ',')
        df_COSTE_TOTAL_oldTar_EXCEL['P5'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_5'][0]).replace('.', ',')
        df_COSTE_TOTAL_oldTar_EXCEL['P6'][0] = str(df_COSTE_TOTAL_oldTar['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los costes totales de potencia antiguas tarifas')

    return df_COSTE_TOTAL_oldTar, df_COSTE_TOTAL_oldTar_EXCEL
