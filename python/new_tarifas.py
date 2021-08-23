# IMPORTS #
import sys
import os

if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph
import pandas as pd

from entradas import arch as curva
from entradas import cuartoHor as ch
from entradas import tar as antigua_tarifa
from entradas import reg as region
from entradas import potCont
from entradas import tipoCont
from entradas import ant_tar3pot

import potencias_NT_proyectoWEB
import energias_NT_proyectoWEB

# ================================== #
def calculos_NT(id_cliente):
    id_cliente_nt = id_cliente
    excel_nuevasTar = pd.ExcelWriter(
        f'C:/Users/Usuario\Desktop\Python/8_PROYECTO_WEB_OPT/resultadoScript_nuevaTarifa{id_cliente_nt}.xlsx',
        engine='xlsxwriter')

    # Consumo de energia
    consumos_Energias_NEWTAR, _, consumos_Energias_NEWTAR_excel = energias_NT_proyectoWEB.df_enerConsumida_NEWTAR(curva,
                                                                                                                  antigua_tarifa,
                                                                                                                  region,
                                                                                                                  ch)
    # ATR de energía
    atr_Energias_NEWTAR, atr_Energias_NEWTAR_excel = energias_NT_proyectoWEB.df_terminoFijoEner_NEWTAR(curva,
                                                                                                       antigua_tarifa,
                                                                                                       region, ch)
    # Pagos por capacidad + perdidas
    PPCmasPERDIDAS_Energias_NEWTAR, PCmasPERDIDAS_Energias_NEWTAR_excel = energias_NT_proyectoWEB.df_pagoCapacidadPerdidasEner_NEWTAR(
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
    consumos_Energias_NEWTAR_excel.to_excel(excel_nuevasTar, sheet_name='Consumos Energia NT')
    atr_Energias_NEWTAR_excel.to_excel(excel_nuevasTar, sheet_name='Atr Energia NT')
    PCmasPERDIDAS_Energias_NEWTAR_excel.to_excel(excel_nuevasTar, sheet_name='Pagos Capacidad + Perdidas NT')
    terminoFijo_potencias_NEWTAR_excel.to_excel(excel_nuevasTar, sheet_name='Termino Fijo Potencias NT')
    excesos_Potencias_NEWTAR_excel.to_excel(excel_nuevasTar, sheet_name='Excesos Potencias NT')

    excel_nuevasTar.save()

    return
