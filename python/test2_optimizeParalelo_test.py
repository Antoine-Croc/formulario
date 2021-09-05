# ======================== IMPORTS ========================
import sys
import os
import time

if os.path.exists('O:/'):
    sys.path.insert(0, 'O:/INGEBAU/Becarios/Data_Utils')
elif os.path.exists('/home'):
    sys.path.insert(0, '/home/ec2-user/Scripts/data_utils')
import path as ph
import pandas as pd
import numpy as np

from entradas import arch as curva
from entradas import cuartoHor as ch
from entradas import tar as antigua_tarifa
from entradas import reg as region
from entradas import potCont
from entradas import tipoCont
from entradas import ant_tar3pot

import potencias_OT_proyectoWEB
import potencias_NT_proyectoWEB
import energias_OT_proyectoWEB_test
import energias_NT_proyectoWEB_test

from scipy.optimize import minimize

from builtins import float

from concurrent.futures import ThreadPoolExecutor

# ===========================================================

global writer


# ======================== FUNCIONES ========================
def s1_oldTar():
    # Consumo de energia
    consumos_Energias_OLDTAR, consumos_Energias_OLDTAR_excel = energias_OT_proyectoWEB_test.df_enerConsumida_OLDTAR(curva,
                                                                                                               antigua_tarifa,
                                                                                                               region,
                                                                                                               ch)
    # ATR de energía
    atr_Energias_OLDTAR, atr_Energias_OLDTAR_excel = energias_OT_proyectoWEB_test.df_terminoFijoEner_OLDTAR(curva,
                                                                                                       antigua_tarifa,
                                                                                                       region, ch)
    # Pagos por capacidad + perdidas
    PCmasPERDIDAS_Energias_OLDTAR, PCmasPERDIDAS_Energias_OLDTAR_excel = energias_OT_proyectoWEB_test.df_pagoCapacidadPerdidasEner_OLDTAR(
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
    consumos_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Consumos Energia OT')
    atr_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Atr Energia OT')
    PCmasPERDIDAS_Energias_OLDTAR_excel.to_excel(writer, sheet_name='Pagos Capacidad + Perdidas OT')
    terminoFijo_Potencias_OLDTAR_excel.to_excel(writer, sheet_name='Termino Fijo Potencias OT')
    excesos_Potencias_OLDTAR_excel.to_excel(writer, sheet_name='Excesos Potencias OT')

    # writer.save()


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

    # writer.save()

    return terminoFijo_Potencias_NEWTAR, excesos_Potencias_NEWTAR


def s3_optimizeNT(tf_pot_NT, exc_pot_NT):
    # Valores iniciales de partida para la optimización
    df_EP_ini = exc_pot_NT
    df_TF_ini = tf_pot_NT
    x0 = np.zeros(6)
    pot = potCont

    if antigua_tarifa in ['3.0A', '3.1A']:
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
        df_EP_opt, _, _, _ = potencias_NT_proyectoWEB.df_excPotencia_NEWTAR(curva, antigua_tarifa, region, x, tipoCont,
                                                                            ch, False)
        df_TF_opt, _ = potencias_NT_proyectoWEB.df_terminoFijoPot_NEWTAR(antigua_tarifa, x, False)

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
                   callback=None, options={'maxiter': 200, 'ftol': 1e-3, 'iprint': 1, 'disp': True,
                                           'eps': 1.4901161193847656e-08, 'finite_diff_rel_step': None})

    # REDONDEO A LA UNIDAD DE LOS VALORES DE POTENCIA OPTIMIZADOS
    potOpt = [0, 0, 0, 0, 0, 0]
    for i in range(0, 6):
        potOpt[i] = round(sol.x[i], 1)
    return potOpt

#  ===========================================================

# //////////////////////// MAIN //////////////////////////////


curva = 'curva_prueba'  # Curva de potencias comnsumidas del cliente
ch = True  # Si el archivo de curvas de consumos es cuartohorario
ant_tar3pot = False  # Dejar true si la tarifa antigua es distinta de 6.1 A
tipoCont = 2  # Contador de medida del cliente
antigua_tarifa = '6.1A'  # Tarifa antigua del cliente
region = 'canarias'  # Region de tarificación del cliente
potCont = [10, 50, 100, 150, 200, 250]  # Potencia contratada por el cliente en M


if __name__ == '__main__':
    start = time.time()
    
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

    # Creamos el archivo de EXCEL donde vamos a trabajar
    writer = pd.ExcelWriter(
        f'C:\\xampp\\htdocs\\ingebau\\formulario\\excel\\resultadoScript_{curva}.xlsx',
        engine='xlsxwriter')

    # Realizamos la ejecución en paralelos de antiguas y nuevas tarifas
    with ThreadPoolExecutor(max_workers=3) as executor:
        results_oldTar = executor.submit(s1_oldTar)
        results_newTar = executor.submit(s2_newTar)

        while True:
            if results_oldTar.running():
                print("Creando archivo de ANTIGUAS tarifas")
            if results_newTar.running():
                print("Creando archivo de NUEVAS tarifas")
            if results_oldTar.done() and results_newTar.done():
                writer.save()
                print('Archivo de ANTIGUAS y NUEVAS tarifas creado, inicio proceso de OPTIMIZACIÓN')
                break

        in1_opt, in2_opt = results_newTar.result()
        print('La combinacion de potencias optimas es: ', s3_optimizeNT(in1_opt, in2_opt))
    end = time.time()
    print(end - start)
