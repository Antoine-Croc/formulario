# /////////////////////// FUNCIONES IMPORTADAS //////////////////////

import sys
import os
from pathlib import Path
import json

if os.path.exists('C:/'):
    sys.path.insert(0, 'C:\xampp\htdocs\ingebau\formulario\excel_python')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph

import pandas as pd
import potencias_OT
import potencias_NT
import energias_OT
import energias_NT

import winsound

# ^^^^^^^^^^^^ DATOS DE ENTRADA ^^^^^^^^^^#
inputN = sys.argv[1] #filename

txt = Path(inputN).read_text()
JsonF = json.loads(txt)

arch = JsonF['arch']  
cuartoHor = JsonF['cuartoHor']  
flag = JsonF['flag']  
tipoCont = JsonF['tipoCont']  
tar = JsonF['tar']  
reg = JsonF['reg']  
potCont = JsonF["potCont"]  

# arch = 'curvaFinal_PR_Desaladora_6_1_A_CH'  # Curva de potencias comnsumidas del cliente
# cuartoHor = True  # Si el archivo de curvas de consumos es cuartohorario
# flag = False  # Dejar true si la tarifa antigua es distinta de 6.1 A
# tipoCont = 2  # Contador de medida del cliente
# tar = '6.1A'  # Tarifa antigua del cliente
# reg = 'canarias'  # Region de tarificación del cliente
# potCont = [810, 810, 810, 810, 810, 880]  # Potencia contratada por el cliente en MW

# ^^^^^^^^^^^^ FUNCION SONORA PARA INDICAR QUE SE HA ALCANZADO LAS POTENCIAS OPTIMAS ^^^^^^^^^^#
def make_noise():
    duration = 1000  # milisegundos
    freq = 440  # Hz
    winsound.Beep(freq, duration)

if __name__ == '__main__':
    # Creamos el excel de escritura, donde rellenaremos las hojas con los datos necesarios
    writer = pd.ExcelWriter(f'{ph.path_actualizacionNT_clientes}resultadoScript_{arch}.xlsx', engine='xlsxwriter')

    # Primero: consumos de energia --------------------------------------------------------------------------------
    consumos_Energias_NEWTAR, _, consumos_Energias_NEWTAR_excel = energias_NT.df_enerConsumida_NEWTAR(arch, tar, reg,
                                                                                                      cuartoHor)
    consumos_Energias_OLDTAR, consumos_Energias_OLDTAR_excel = energias_OT.df_enerConsumida_OLDTAR(arch, tar, reg,
                                                                                                   cuartoHor)
    consumos_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Consumos Energia')
    consumos_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Consumos Energia', startrow=15)

    # Segundo: ATRs energía ---------------------------------------------------------------------------------------
    atr_Energias_NEWTAR, atr_Energias_NEWTAR_excel = energias_NT.df_terminoFijoEner_NEWTAR(arch, tar, reg, cuartoHor)
    atr_Energias_OLDTAR, atr_Energias_OLDTAR_excel = energias_OT.df_terminoFijoEner_OLDTAR(arch, tar, reg, cuartoHor)
    atr_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Atr Energia')
    atr_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Atr Energia', startrow=4)

    # Tercero: pagos por capacidad + perdidas ----------------------------------------------------------------------
    PCmasPERDIDAS_Energias_NEWTAR, PCmasPERDIDAS_Energias_NEWTAR_excel = energias_NT.df_pagoCapacidadPerdidasEner_NEWTAR(
        arch, tar, reg, cuartoHor)
    PCmasPERDIDAS_Energias_OLDTAR, PCmasPERDIDAS_Energias_OLDTAR_excel = energias_OT.df_pagoCapacidadPerdidasEner_OLDTAR(
        arch, tar, reg, cuartoHor)
    PCmasPERDIDAS_Energias_NEWTAR_excel.to_excel(writer, sheet_name='Pagos Capacidad + Perdidas')
    PCmasPERDIDAS_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Pagos Capacidad + Perdidas', startrow=4)

    # Cuarto: termino fijo potencias ------------------------------------------------------------------------------
    terminoFijo_Potencias_NEWTAR, terminoFijo_potencias_NEWTAR_excel = potencias_NT.df_terminoFijoPot_NEWTAR(tar,
                                                                                                             potCont,
                                                                                                             flag)
    terminoFijo_Potencias_OLDTAR, terminoFijo_Potencias_OLDTAR_excel = potencias_OT.df_terminoFijoPot_OLDTAR(tar,
                                                                                                             potCont)
    terminoFijo_potencias_NEWTAR_excel.to_excel(writer, sheet_name='Termino Fijo Potencias')
    terminoFijo_Potencias_OLDTAR_excel.to_excel(writer, sheet_name='Termino Fijo Potencias', startrow=4)

    # Quinto: excesos potencias -----------------------------------------------------------------------------------
    excesos_Potencias_NEWTAR, excesos_Potencias_NEWTAR_excel, cantidadExcesos_NEWTAR, maximosExcesos_NEWTAR = potencias_NT.df_excPotencia_NEWTAR(
        arch, tar, reg,
        potCont,
        tipoCont,
        cuartoHor, flag)
    excesos_Potencias_OLDTAR, excesos_Potencias_OLDTAR_excel = potencias_OT.df_excPotencia_OLDTAR(arch, tar, reg,
                                                                                                  potCont,
                                                                                                  tipoCont,
                                                                                                  cuartoHor)
    excesos_Potencias_NEWTAR_excel.to_excel(writer, sheet_name='Excesos Potencias')
    excesos_Potencias_OLDTAR_excel.to_excel(writer, sheet_name='Excesos Potencias', startrow=15)

    # EXTRA: optimizacion de las potencias contratadas ------------------------------------------------------------
    print('Cantidad de excesos de potencias por periodo y mes en el último año:')
    print(cantidadExcesos_NEWTAR)
    print('')
    print('Maximas potencias de exceso por periodo y mes en el último año:')
    print(maximosExcesos_NEWTAR)
    print('')

    potCalculoOpt = potencias_NT.optimizacionPotencias(arch, tar, reg, potCont, tipoCont, cuartoHor, flag)
    print(f'{potCalculoOpt}')
    make_noise()

    input_string = input('Introduce las potencias optimas que se quieran, separadas por espacios: ')
    print("\n")
    potOpt = input_string.split()
    # print list
    print('list: ', potOpt)

    # convert each item to int type
    for i in range(len(potOpt)):
        # convert each item to int type
        potOpt[i] = float(potOpt[i])
    flag = False

    terminoFijo_Potencias_Optima, terminoFijo_potencias_Optima_excel = potencias_NT.df_terminoFijoPot_NEWTAR(tar,
                                                                                                             potOpt,
                                                                                                             flag)
    terminoFijo_potencias_Optima_excel.to_excel(writer, sheet_name='Termino Fijo Potencias', startrow=8)

    excesos_Potencias_Optima, excesos_Potencias_Optima_excel, _, _ = potencias_NT.df_excPotencia_NEWTAR(arch, tar, reg,
                                                                                                        potOpt,
                                                                                                        tipoCont,
                                                                                                        cuartoHor, flag)
    excesos_Potencias_Optima_excel.to_excel(writer, sheet_name='Excesos Potencias', startrow=30)

    writer.save()