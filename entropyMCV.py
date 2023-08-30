#---------------------------------------------------------------------------------------------------------------------------#
# Script para el calculo de la entropia minima de un sistema siguiendo el esquema de ejecucion de NIST SP800-90B
# Seguiremos la estructura indicada en el grafico de ejecucion del paper
# Autor: [Christian Bustelo] - [HPCNOW!]
# Fecha: [24/08/20023]
#---------------------------------------------------------------------------------------------------------------------------#
import numpy as np
import sys
import math
from scipy.stats import binom
from scipy.stats import chi2
from collections import Counter
import random

from testPermutacion import (
    calculate_directional_runs,
    calculate_length_of_longest_directional_run,
    calculate_number_of_increases_decreases,
    calculate_number_of_runs_median,
    calculate_length_of_runs_median,
    calculate_average_collision,
    calculate_max_collision
)


#----------------------------------#
# Seccion 1 : Recoleccion de datos #
#----------------------------------#

def data_collection():

    print("\r")
    print("-----------------------------------------------")
    print("[Stage 1] Recoleccion de datos inicial")
    print("-----------------------------------------------")

    ######################################
    # PETICION DE 1000000 de entradas
    ######################################

    # Seccion mockeada #
    file_path = "/home/cbustelo/Desktop/Proyectos/Cesga_QRNG/800_90B/cesga-qrng/small_output.txt" #Salida de pruebas validas
    with open(file_path, "r") as file:
        lines = file.readlines()
        data = [int(line.strip()) for line in lines] 

    print("\033[92m[Stage 1] Done\033[0m")
    print("-----------------------------------------------")

    return data

#-------------------------#
# Seccion 2 : Test de IID #
#-------------------------#

# Ejecion de los test
def perform_test(data):
    print("\r")
    print("-----------------------------------------------")
    print("[Stage 2] Test de IID")
    print("-----------------------------------------------")

    resultado = testIID(data)

    if not resultado:
        print("\033[91m[Stage 2] Los datos no son de tipo IID, datos no aptos\033[0m")
        print("------------------------------------------------------")
        sys.exit()
    else:
        print("\033[92m[Stage 2] Los datos son de tipo IID\033[0m")
        print("---------------------------------------------------------------")

# Implementacion del metodo de Test de permutacion para la validacion de los IID
def testIID(original_data):
    test_statistics_original = [
        calculate_directional_runs(original_data),
        calculate_length_of_longest_directional_run(original_data),
        calculate_number_of_increases_decreases(original_data),
        calculate_number_of_runs_median(original_data),
        calculate_length_of_runs_median(original_data),
        calculate_average_collision(original_data),
        calculate_max_collision(original_data)
    ]

    Ci_0 = [0] * len(test_statistics_original)
    Ci_1 = [0] * len(test_statistics_original)  

    num_permutations = 10000

    for _ in range(num_permutations):
        permuted_data = original_data.copy()  # Realiza una copia para no modificar los datos originales
        fisher_yates_shuffle(permuted_data)  # Permuta los datos utilizando el algoritmo Fisher-Yates

        for i, test_statistic_original in enumerate(test_statistics_original):
            test_statistic_permuted = [
                calculate_directional_runs(permuted_data),
                calculate_length_of_longest_directional_run(permuted_data),
                calculate_number_of_increases_decreases(permuted_data),
                calculate_number_of_runs_median(permuted_data),
                calculate_length_of_runs_median(permuted_data),
                calculate_average_collision(permuted_data),
                calculate_max_collision(permuted_data)
            ][i]

            if test_statistic_permuted > test_statistic_original:
                Ci_0[i] += 1
            elif test_statistic_permuted == test_statistic_original:
                Ci_1[i] += 1

    reject_iid_assumption = False

    for i in range(len(test_statistics_original)):
        if (Ci_0[i] + Ci_1[i] <= 5) or (Ci_0[i] >= 9995):
            reject_iid_assumption = True
            break

    if reject_iid_assumption:
        return False
    else:
        return True

#---------------------------------#
# Seccion 3 : Estimacion entropia #
#---------------------------------#

def estimate_entropy(data):

    print("\r")
    print("-------------------------------------------------------------------")
    print("[Stage 3] Cáluclo de la entropia inicial")
    print("-------------------------------------------------------------------")

    maxima = most_common_value_estimate(data, True)
    estimate = most_common_value_estimate(data, False)

    if maxima==estimate :
        print("\033[92m[Stage 3] Entropia inicial calculada y coincidente con el pico teórico\033[0m")
        print("-------------------------------------------------------------------")
    else:
        print("\033[92m[Stage 3] Entropia inicial calculada y menor al pico teórico\033[0m")
        print("-------------------------------------------------------------------")

    if verbose:
        print("\r")
        print("*****************************************")
        print("- Entropias -")
        print("*****************************************")
        print("Max-entropy teorica:", maxima)
        print("\r")

    return estimate

# Funcion para el calculo de la entropia minima #
def most_common_value_estimate(dataset, teorica):
    # Step 1: Find the proportion of the most common value
    value_counts = {}
    for value in dataset:
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1

    # Si la flag de entropia teorica es True entonces calculamos el maximo teorico por la formula
    if (teorica):
        max_count = 1
    else:
        max_count = max(value_counts.values())

    p_hat = max_count / len(dataset)

    # Step 2: Calculate an upper bound on the probability of the most common value
    z_value = 2.576  # Z-score for 99.5% confidence interval
    p_upper_bound = min(1, p_hat + z_value * math.sqrt(p_hat * (1 - p_hat) / (len(dataset) - 1)))
    
    # Step 3: Calculate the estimated min-entropy
    min_entropy_estimate = -math.log2(p_upper_bound)
    
    return min_entropy_estimate


#------------------------------#
# Seccion 4 : Test de reinicio #
#------------------------------#
def restart_test(h_i):
    x_count = y_count = 1000

    ##################################################
    # Construimos la matriz con las peticiones de datos
    ##################################################
    # Pseudo:
    # matrix = np.zeros((x_count, y_count), dtype=np.int32)
    # for i in range(y_count):
    #   open conexion con la maquina
    #   valores = tu_funcion()
    #   matrix[i, :] = valores 
    #   close de la conexion
    #   pasar los valores de la matriz a 8 bits
    #   tiempo de espera de para otra conexion

    # Mockeo    
    matrix = np.random.randint(0, 2**8, size=(x_count, y_count), dtype=np.uint8)

    ##################################################

    # Ejecutamos el test de sanidad
    san_chek, prob_sum, xmm = perform_sanity_check(matrix,h_i)
    if san_chek==False:
        print("\033[91m[Stage 4] Test de reinicio fallido \033[0m")
        print("-------------------------------------------------------------------")
        if verbose:
            print("\r")
            print("*****************************************")
            print("- Sanity Check: False -")
            print("*****************************************")
            print("Prob_sum:", prob_sum)
            print("Xmm: ", xmm)
            print("\r")
            sys.exit()
        return False,0 

    # Ejecutamos MVCE test sobre las filas y columnas

    # Construir el row dataset concatenando las filas
    row_dataset = matrix.flatten()
    estimate_rows = most_common_value_estimate(row_dataset, False)

    # Construir el column dataset concatenando las columnas
    column_dataset = matrix.T.flatten()
    estimate_cols = most_common_value_estimate(column_dataset, False)
    
    validator_entropy = min(estimate_cols,estimate_rows)
    if (h_i/2) > validator_entropy:
        print("\033[91m[Stage 4] Test de reinicio fallido \033[0m")
        print("-------------------------------------------------------------------")
        if verbose:
            print("\r")
            print("*****************************************")
            print("- Data restart test: False -")
            print("*****************************************")
            print("Mitad de entropia inicial:", h_i/2)
            print("estimate_cols:", estimate_cols)
            print("estimate_rows:", estimate_rows)
        return False,0
    else:
        print("\033[92m[Stage 4] Test de reinicio pasado \033[0m")
        print("-------------------------------------------------------------------")
        if verbose:
            print("\r")
            print("*****************************************")
            print("- Data restart test: Passed -")
            print("*****************************************")
            print("Mitad de entropia inicial:", h_i/2)
            print("estimate_cols:", estimate_cols)
            print("estimate_rows:", estimate_rows)
        return True, min(validator_entropy,h_i)

# Ejecuta el sanity check para la matriz
def perform_sanity_check(matrix,h_i):
    p = 2 ** -h_i
    alpha = 0.000005

    xr = 0
    xc = 0

    # Calculate highest count values for rows 
    for row in matrix:
        row_counts = {}
        for sample in row:
            if sample in row_counts:
                row_counts[sample] += 1
            else:
                row_counts[sample] = 1
        highest_count = max(row_counts.values())
        xr = max(xr, highest_count)

    # Calculate highest count values for columns 
    for col in range(len(matrix)):
        col_counts = {}
        for row in matrix:
            sample = row[col]
            if sample in col_counts:
                col_counts[sample] += 1
            else:
                col_counts[sample] = 1
        highest_count = max(col_counts.values())
        xc = max(xc, highest_count)

    # Max value
    xmm = max(xc, xr)

    # Calculate the probability using binomial distribution
    prob_sum = 0
    for j in range(xmm, 1001):
        prob_sum += binom.pmf(j, 1000, p)

    if prob_sum < alpha:
        return False, prob_sum, xmm
    else:
        return True, prob_sum, xmm


#------------------------------------#
# Seccion Extra : Funciones de apoyo #
#------------------------------------#

# Transformacion a numeros de 8 bits toamando los menos significativos
def transform_to_8_bits(data):
    transformed_data = [(x >> 24) & 0xFF for x in data]
    return transformed_data

# Calcula la entropia de bitstring binario
def calculate_entropy_bitstring(sequence, n, max_bits=1000000):
    # Considerar solo los primeros max_bits bits en total
    truncated_sequence = sequence[:max_bits]
    
    # Crear "n" contadores para cada posición de bit
    bit_counters = [Counter() for _ in range(n)]
    
    # Llenar los contadores de bits para cada posición
    for num in truncated_sequence:
        for i in range(n):
            bit = (num >> i) & 1
            bit_counters[i][bit] += 1
    
    # Calcular la entropía por bit en cada posición
    entropy_per_bit = []
    for counter in bit_counters:
        total_bits = sum(counter.values())
        probabilities = [count / total_bits for count in counter.values()]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        entropy_per_bit.append(entropy)
    
    # Calcular la entropía promedio por bit para todas las posiciones
    avg_entropy_per_bit = sum(entropy_per_bit) / n
    
    # Devolvemos el valor de la entropia por bit multipicado por el numero de bits
    return avg_entropy_per_bit * n

def fisher_yates_shuffle(arr):
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


# ************************************************************************************ #

#--------------#
# Funcion main #
#--------------#
if __name__ == "__main__":

    h_fabricante = "unknowk"

    # Paso 0: Checkeo de argumentos
    verbose = "-v" in sys.argv
    skip_test = "--no-test" in sys.argv

    # Paso 1: recoleccion de datos y formateo a 8 bit
    data = data_collection()
    data_8b = transform_to_8_bits(data)

    #Paso 2: Test de IID
    perform_test(data_8b)

    # Paso 3: Calculo de la entropia inicial y teorica maxima
    h_estimada = estimate_entropy(data_8b)
    num_bits_per_sample = 8 
    h_binary_addicional = calculate_entropy_bitstring(data_8b,num_bits_per_sample)

    if verbose:
        print("Entropia estimada por bitstring:", h_binary_addicional)
        print("Entropia estimada inicial:", h_estimada)
        print("Entropia estimada por fabricante:", h_fabricante)

    h_i = min (h_estimada, h_binary_addicional)

    if (not skip_test):
        # Paso 4: Test de reinicio
        print("\r")
        print("-------------------------------------------------------------------")
        print("[Stage 4] Iniciando test de reinicio")
        print("-------------------------------------------------------------------")
        is_valid,h_m = restart_test(h_i)
        
        # Paso 5: Impresion de resultados
        if is_valid:    
            print("\r")
            print("-------------------------------------------------------------------")
            print("\033[92m[Stage 5] Resultados \033[0m")
            print("-------------------------------------------------------------------")
            print("- Entropia alcanzada:",h_m,"-")
            print("\r")
    else:
        print("\r")
        print("-------------------------------------------------------------------")
        print("\033[92m[Stage 4] Resultados \033[0m")
        print("-------------------------------------------------------------------")
        print("- Entropia alcanzada:",h_i,"-")
        print("\r")

