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

import potencias_OT_proyectoWEB
import energias_OT_proyectoWEB

# ================================== #

id_cliente_ot = input("Id de cliente: ")
excel_antiguasTar = pd.ExcelWriter(
    f'{ph.path_actualizacionNT_clientes}resultadoScript_antiguaTarifa{id_cliente_ot}.xlsx', engine='xlsxwriter')

# Consumo de energia
consumos_Energias_OLDTAR, consumos_Energias_OLDTAR_excel = energias_OT_proyectoWEB.df_enerConsumida_OLDTAR(curva,
                                                                                                           antigua_tarifa,
                                                                                                           region,
                                                                                                           ch)
# ATR de energía
atr_Energias_OLDTAR, atr_Energias_OLDTAR_excel = energias_OT_proyectoWEB.df_terminoFijoEner_OLDTAR(curva,
                                                                                                   antigua_tarifa,
                                                                                                   region, ch)
# Pagos por capacidad + perdidas
PCmasPERDIDAS_Energias_OLDTAR, PCmasPERDIDAS_Energias_OLDTAR_excel = energias_OT_proyectoWEB.df_pagoCapacidadPerdidasEner_OLDTAR(
    curva, antigua_tarifa, region, ch)

# Termino fijo de potencia
terminoFijo_Potencias_OLDTAR, terminoFijo_Potencias_OLDTAR_excel = potencias_OT_proyectoWEB.df_terminoFijoPot_OLDTAR(
    antigua_tarifa,
    potCont)
# Excesos de potencia
excesos_Potencias_OLDTAR, excesos_Potencias_OLDTAR_excel = potencias_OT_proyectoWEB.df_excPotencia_OLDTAR(curva,
                                                                                                          antigua_tarifa,
                                                                                                          region,
                                                                                                          potCont,
                                                                                                          tipoCont,
                                                                                                          ch)
# ==== ESCRITURA EN EXCEL ==== #
consumos_Energias_OLDTAR_excel.to_excel(excel_antiguasTar, sheet_name='Consumos Energia OT')
atr_Energias_OLDTAR_excel.to_excel(excel_antiguasTar, sheet_name='Atr Energia OT')
PCmasPERDIDAS_Energias_OLDTAR_excel.to_excel(excel_antiguasTar, sheet_name='Pagos Capacidad + Perdidas OT')
terminoFijo_Potencias_OLDTAR_excel.to_excel(excel_antiguasTar, sheet_name='Termino Fijo Potencias OT')
excesos_Potencias_OLDTAR_excel.to_excel(excel_antiguasTar, sheet_name='Excesos Potencias OT')

excel_antiguasTar.save()
