# ======================== IMPORTS ========================
import sys
import os

if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph
import pandas as pd
import numpy as np

import potencias_NT_proyectoWEB
import energias_NT_proyectoWEB_test

from scipy.optimize import minimize

from builtins import float

from concurrent.futures import ThreadPoolExecutor

# ===========================================================

global writer


def s2_newTar():
    # Consumo de energia
    consumos_Energias_NEWTAR, _, consumos_Energias_NEWTAR_excel = energias_NT_proyectoWEB_test.df_enerConsumida_NEWTAR(curva,
                                                                                                                  antigua_tarifa,
                                                                                                                  region,
                                                                                                                  ch)
    # ATR de energía
    atr_Energias_NEWTAR, atr_Energias_NEWTAR_excel = energias_NT_proyectoWEB_test.df_terminoFijoEner_NEWTAR(curva,
                                                                                                       antigua_tarifa,
                                                                                                       region, ch)
    # Pagos por capacidad + perdidas
    PPCmasPERDIDAS_Energias_NEWTAR, PCmasPERDIDAS_Energias_NEWTAR_excel = energias_NT_proyectoWEB_test.df_pagoCapacidadPerdidasEner_NEWTAR(
        curva, antigua_tarifa, region, ch)

    # Termino fijo de potencia
    terminoFijo_Potencias_NEWTAR, terminoFijo_potencias_NEWTAR_excel = potencias_NT_proyectoWEB.df_terminoFijoPot_NEWTAR(
        antigua_tarifa,
        potCont,
        ant_tar3pot)

    # Excesos de potencia
    excesos_Potencias_NEWTAR, excesos_Potencias_NEWTAR_excel, cantidadExcesos_NEWTAR, maximosExcesos_NEWTAR = potencias_NT_proyectoWEB.df_excPotencia_NEWTAR(
        curva,
        antigua_tarifa,
        region,
        potCont,
        tipoCont,
        ch,
        ant_tar3pot)

    # ==== ESCRITURA EN EXCEL ==== #
    consumos_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Consumos Energia NT')
    atr_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Atr Energia NT')
    PCmasPERDIDAS_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Pagos Capacidad + Perdidas NT')
    terminoFijo_potencias_NEWTAR_excel.to_excel(writer, sheet_name='Termino Fijo Potencias NT')
    excesos_Potencias_NEWTAR_excel.to_excel(writer, sheet_name='Excesos Potencias NT')

    writer.save()
    print("ok")
    return terminoFijo_Potencias_NEWTAR, excesos_Potencias_NEWTAR

curva = 'curva_prueba'  # Curva de potencias comnsumidas del cliente
ch = True  # Si el archivo de curvas de consumos es cuartohorario
ant_tar3pot = False  # Dejar true si la tarifa antigua es distinta de 6.1 A
tipoCont = 2  # Contador de medida del cliente
antigua_tarifa = '6.1A'  # Tarifa antigua del cliente
region = 'canarias'  # Region de tarificación del cliente
potCont = [280, 280, 280, 280, 280, 280]  # Potencia contratada por el cliente en M

if __name__ == '__main__':

    if len(sys.argv)>1:
        curva = sys.argv[1]
        ch = sys.argv[2]
        ant_tar3pot = sys.argv[3]
        tipoCont = sys.argv[4]
        antigua_tarifa = sys.argv[5]
        region = sys.argv[6]
        potCont = sys.argv[7].split(",")

        for i in range(len(potCont)):
            potCont[i] = float(potCont[i])

    # Escribimos el id del cliente
    # Creamos el archivo de EXCEL donde vamos a trabajar
    writer = pd.ExcelWriter(
        f'C:\\xampp\\htdocs\\ingebau\\form_opt\\results\\resultadoScript_{curva}.xlsx',
        engine='xlsxwriter')

    results_costos = s2_newTar()