# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ IMPORTS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
import sys
import os

if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph

# Imports de las librerias de PANDAS (para los dataframes) y NUMPY (para trabajo matricial)
import pandas as pd

# Imports de librerias JSON (diccionarios de configuraciones) y DATETIME (para trabajo con fechas)
import json as js
from datetime import datetime as dt

# Otros imports
from builtins import float


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES AUXILIARES ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

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
def get_period_OLDTARe(config, d, season):
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

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FUNCIONES PRINCIPALES ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

def df_enerConsumida_OLDTAR(archivo, tarifa, region, cuartahoraria):
    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    tar_periods = tarifa_to_type_tarifa(tarifa)

    if region == 'peninsula':
        with open(f'{ph.path_config_perdidas}/{tar_periods}.json') as config:
            config_perLOAD = js.load(config)
    else:
        with open(f'{ph.path_config_perdidas_canarias}/{tar_periods}.json') as config:
            config_perLOAD = js.load(config)

        # Extracción de los datos de las curvas de cosnumos dependiendo del formato de entrada de la misma ----------------
    list_Date = []  # Lugar de volcado de las fechas del archivo de curva de consummo de entrada
    list_EnerConsum = []  # Lugar de volcado de los consumos del archivo de curva de consummo de entrada

    try:  # Intento abrir un archivo de formato ".xlsx"
        data = pd.read_csv(f'C:/xampp/htdocs/ingebau/formulario/curvas/{archivo}.csv', sep=';')
        for i in range(len(data)):
            dateCSV = f'{str(data["Fecha"][i])} {str(data["Hora"][i])}'
            try:
                list_Date.append(dt.strptime(dateCSV, '%Y-%m-%d %H,00'))
            except:
                list_Date.append(dt.strptime(dateCSV, '%d/%m/%Y %H'))
            try:
                enerConsum = data["Consumo Activa"][i].replace('.', '')
            except:
                enerConsum = data["Consumption"][i].replace('.', '')
            list_EnerConsum.append(enerConsum.replace(',', '.'))
    except:  # Si no funciona, intento abrir un archivo de formato ".csv"
        data = pd.read_excel(f'C:/xampp/htdocs/ingebau/formulario/curvas/{archivo}.xlsx', sheet_name='Hoja1')
        for i in range(len(data)):
            dateXLSX = dt.strptime(f'{str(data["Fecha"][i])}', '%Y-%m-%d %H:%M:%S')
            dateXLSX = dateXLSX.replace(hour=data["Hora"][i])
            list_Date.append(dateXLSX)
            enerConsum = data["Consumo Activa"][i]
            list_EnerConsum.append(enerConsum)

    # Creacion de un dataframe para facilidad de calculos y agrupaciones
    period = []
    fecha = []
    mes = []
    tempor = []
    eConsum = []

    for j in range(len(data)):
        period.append(get_period_OLDTARe(config_perLOAD, list_Date[j], type_day(list_Date[j])))
        fecha.append(list_Date[j])
        mes.append(list_Date[j].month)
        tempor.append(type_day(list_Date[j]))
        eConsum.append(float(list_EnerConsum[j]))

    df_listaEnerConsum = pd.DataFrame(
        {
            "Periodo": period,
            "Fecha": fecha,
            "Mes": mes,
            "Temporada": tempor,
            "Energia Consumida": eConsum
        }
    )

    # Agrupamos las potencias por periodos
    try:
        ener_ConsumP1 = df_listaEnerConsum.groupby('Periodo').get_group(1).reset_index(drop=True)
    except:
        ener_ConsumP1 = 0

    try:
        ener_ConsumP2 = df_listaEnerConsum.groupby('Periodo').get_group(2).reset_index(drop=True)
    except:
        ener_ConsumP2 = 0

    try:
        ener_ConsumP3 = df_listaEnerConsum.groupby('Periodo').get_group(3).reset_index(drop=True)
    except:
        ener_ConsumP3 = 0

    try:
        ener_ConsumP4 = df_listaEnerConsum.groupby('Periodo').get_group(4).reset_index(drop=True)
    except:
        ener_ConsumP4 = 0

    try:
        ener_ConsumP5 = df_listaEnerConsum.groupby('Periodo').get_group(5).reset_index(drop=True)
    except:
        ener_ConsumP5 = 0

    try:
        ener_ConsumP6 = df_listaEnerConsum.groupby('Periodo').get_group(6).reset_index(drop=True)
    except:
        ener_ConsumP6 = 0

    # Calculamos el consumo total de potencias por periodo y mes
    suma_enerConsum_P1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_enerConsum_P2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_enerConsum_P3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_enerConsum_P4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_enerConsum_P5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    suma_enerConsum_P6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(1, 13):
        try:
            ener_ConsumP1_mes = ener_ConsumP1.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP1_mes = [0]

        try:
            ener_ConsumP2_mes = ener_ConsumP2.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP2_mes = [0]

        try:
            ener_ConsumP3_mes = ener_ConsumP3.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP3_mes = [0]

        try:
            ener_ConsumP4_mes = ener_ConsumP4.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP4_mes = [0]

        try:
            ener_ConsumP5_mes = ener_ConsumP5.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP5_mes = [0]

        try:
            ener_ConsumP6_mes = ener_ConsumP6.groupby('Mes').get_group(i)['Energia Consumida'].reset_index(drop=True)
        except:
            ener_ConsumP6_mes = [0]

        for h in range(len(ener_ConsumP1_mes)):
            suma_enerConsum_P1[i - 1] += ener_ConsumP1_mes[h]

        for j in range(len(ener_ConsumP2_mes)):
            suma_enerConsum_P2[i - 1] += ener_ConsumP2_mes[j]

        for k in range(len(ener_ConsumP3_mes)):
            suma_enerConsum_P3[i - 1] += ener_ConsumP3_mes[k]

        for p in range(len(ener_ConsumP4_mes)):
            suma_enerConsum_P4[i - 1] += ener_ConsumP4_mes[p]

        for m in range(len(ener_ConsumP5_mes)):
            suma_enerConsum_P5[i - 1] += ener_ConsumP5_mes[m]

        for n in range(len(ener_ConsumP6_mes)):
            suma_enerConsum_P6[i - 1] += ener_ConsumP6_mes[n]

    if cuartahoraria:
        for i in range(1, 13):
            suma_enerConsum_P1[i - 1] = suma_enerConsum_P1[i - 1] / 4
            suma_enerConsum_P2[i - 1] = suma_enerConsum_P2[i - 1] / 4
            suma_enerConsum_P3[i - 1] = suma_enerConsum_P3[i - 1] / 4
            suma_enerConsum_P4[i - 1] = suma_enerConsum_P4[i - 1] / 4
            suma_enerConsum_P5[i - 1] = suma_enerConsum_P5[i - 1] / 4
            suma_enerConsum_P6[i - 1] = suma_enerConsum_P6[i - 1] / 4
    else:
        pass

    suma_enerConsum_P1.append(sum(suma_enerConsum_P1))
    suma_enerConsum_P2.append(sum(suma_enerConsum_P2))
    suma_enerConsum_P3.append(sum(suma_enerConsum_P3))
    suma_enerConsum_P4.append(sum(suma_enerConsum_P4))
    suma_enerConsum_P5.append(sum(suma_enerConsum_P5))
    suma_enerConsum_P6.append(sum(suma_enerConsum_P6))

    df_enerConsumidaMesPer = pd.DataFrame(
        {
            'Periodo_1': suma_enerConsum_P1,
            'Periodo_2': suma_enerConsum_P2,
            'Periodo_3': suma_enerConsum_P3,
            'Periodo_4': suma_enerConsum_P4,
            'Periodo_5': suma_enerConsum_P5,
            'Periodo_6': suma_enerConsum_P6
        }, index=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                  'Noviembre', 'Diciembre', 'TOTAL']
    )

    # Adaptacion de los resultados para exportar a excel
    df_enerConsumidaMesPer_excel = pd.DataFrame(
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
        df_enerConsumidaMesPer_excel['P1'][aux] = str(df_enerConsumidaMesPer['Periodo_1'][aux]).replace(
            '.', ',')
        df_enerConsumidaMesPer_excel['P2'][aux] = str(df_enerConsumidaMesPer['Periodo_2'][aux]).replace(
            '.', ',')
        df_enerConsumidaMesPer_excel['P3'][aux] = str(df_enerConsumidaMesPer['Periodo_3'][aux]).replace(
            '.', ',')
        df_enerConsumidaMesPer_excel['P4'][aux] = str(df_enerConsumidaMesPer['Periodo_4'][aux]).replace(
            '.', ',')
        df_enerConsumidaMesPer_excel['P5'][aux] = str(df_enerConsumidaMesPer['Periodo_5'][aux]).replace(
            '.', ',')
        df_enerConsumidaMesPer_excel['P6'][aux] = str(df_enerConsumidaMesPer['Periodo_6'][aux]).replace(
            '.', ',')

    return df_enerConsumidaMesPer, df_enerConsumidaMesPer_excel


def df_terminoFijoEner_OLDTAR(archivo, tarifa, region, cuartahoraria):
    # Tablas para las distintas configuraciones y propiedades tarifarias ----------------------------------------------
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    # Cargamos el dataframe de consumos de energia
    df_ener, _ = df_enerConsumida_OLDTAR(archivo, tarifa, region, cuartahoraria)

    IE = 1.051127
    terminoFijo = [0, 0, 0, 0, 0, 0]

    for i in range(1, 7):
        terminoFijo[i - 1] = df_ener[f'Periodo_{i}'][-1] * tablesLOAD['ATRenergia_OT'][tarifa][f'period{i}']

    df_costeFijoEner = pd.DataFrame(
        {
            'Periodo_1': terminoFijo[0],
            'Periodo_2': terminoFijo[1],
            'Periodo_3': terminoFijo[2],
            'Periodo_4': terminoFijo[3],
            'Periodo_5': terminoFijo[4],
            'Periodo_6': terminoFijo[5]
        }, index=['TOTAL']
    )

    df_costeFijoEner = df_costeFijoEner * IE

    # Adaptacion de los resultados para exportar a excel
    df_costeFijoEner_excel = pd.DataFrame(
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
        df_costeFijoEner_excel['P1'][0] = str(df_costeFijoEner['Periodo_1'][0]).replace('.', ',')
        df_costeFijoEner_excel['P2'][0] = str(df_costeFijoEner['Periodo_2'][0]).replace('.', ',')
        df_costeFijoEner_excel['P3'][0] = str(df_costeFijoEner['Periodo_3'][0]).replace('.', ',')
        df_costeFijoEner_excel['P4'][0] = str(df_costeFijoEner['Periodo_4'][0]).replace('.', ',')
        df_costeFijoEner_excel['P5'][0] = str(df_costeFijoEner['Periodo_5'][0]).replace('.', ',')
        df_costeFijoEner_excel['P6'][0] = str(df_costeFijoEner['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los terminos fijos de potencia')

    return df_costeFijoEner, df_costeFijoEner_excel


def df_pagoCapacidadPerdidasEner_OLDTAR(archivo, tarifa, region, cuartahoraria):
    with open(f'{ph.path_tables}') as tables:
        tablesLOAD = js.load(tables)

    consumoEner_mesPeriod, _ = df_enerConsumida_OLDTAR(archivo, tarifa, region, cuartahoraria)

    IE = 1.051127
    pagoCapaMasPerd = [0, 0, 0, 0, 0, 0]

    for i in range(1, 7):
        pagoCapaMasPerd[i - 1] = consumoEner_mesPeriod[f'Periodo_{i}'][-1] * tablesLOAD['PCmasPer_OT'][tarifa][
            f'period{i}']

    df_pagoCapYperd = pd.DataFrame(
        {
            'Periodo_1': pagoCapaMasPerd[0],
            'Periodo_2': pagoCapaMasPerd[1],
            'Periodo_3': pagoCapaMasPerd[2],
            'Periodo_4': pagoCapaMasPerd[3],
            'Periodo_5': pagoCapaMasPerd[4],
            'Periodo_6': pagoCapaMasPerd[5]
        }, index=['TOTAL']
    )

    df_pagoCapYperd = df_pagoCapYperd * IE

    # Adaptacion de los resultados para exportar a excel
    df_pagoCapYperd_excel = pd.DataFrame(
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
        df_pagoCapYperd_excel['P1'][0] = str(df_pagoCapYperd['Periodo_1'][0]).replace('.', ',')
        df_pagoCapYperd_excel['P2'][0] = str(df_pagoCapYperd['Periodo_2'][0]).replace('.', ',')
        df_pagoCapYperd_excel['P3'][0] = str(df_pagoCapYperd['Periodo_3'][0]).replace('.', ',')
        df_pagoCapYperd_excel['P4'][0] = str(df_pagoCapYperd['Periodo_4'][0]).replace('.', ',')
        df_pagoCapYperd_excel['P5'][0] = str(df_pagoCapYperd['Periodo_5'][0]).replace('.', ',')
        df_pagoCapYperd_excel['P6'][0] = str(df_pagoCapYperd['Periodo_6'][0]).replace('.', ',')
    except:
        print('Error creando dataframe apto para excel de los terminos fijos de potencia')

    return df_pagoCapYperd, df_pagoCapYperd_excel
