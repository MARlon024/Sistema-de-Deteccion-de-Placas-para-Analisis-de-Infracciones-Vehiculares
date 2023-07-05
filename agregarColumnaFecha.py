import csv
from datetime import datetime, timedelta
import random


def generar_fecha_aleatoria(fecha_inicio, fecha_fin):
    formato_fecha = '%d/%m/%y'
    fecha_inicio = datetime.strptime(fecha_inicio, formato_fecha)
    fecha_fin = datetime.strptime(fecha_fin, formato_fecha)
    diferencia = fecha_fin - fecha_inicio
    dias = random.randint(0, diferencia.days)
    fecha_generada = fecha_inicio + timedelta(days=dias)
    return fecha_generada.strftime(formato_fecha)


# Parámetros de entrada
fecha_inicio_parametro = input("Ingrese la fecha de inicio (DD/MM/YY): ")
fecha_fin_parametro = input("Ingrese la fecha de fin (DD/MM/YY): ")

# Abrir el archivo CSV de entrada
ruta_archivo_entrada = 'infracciones.csv'
# Nombre del archivo CSV de salida
ruta_archivo_salida = 'infracciones_modificado.csv'
columnas_nuevas = ['Fecha']  # Nombres de las nuevas columnas a añadir

with open(ruta_archivo_entrada, 'r') as archivo_entrada, open(ruta_archivo_salida, 'w', newline='') as archivo_salida:
    lector_csv = csv.reader(archivo_entrada)
    escritor_csv = csv.writer(archivo_salida)

    # Leer la primera fila del archivo (encabezados)
    encabezados = next(lector_csv)

    # Añadir los nombres de las nuevas columnas a los encabezados
    encabezados.extend(columnas_nuevas)

    # Escribir los encabezados en el archivo de salida
    escritor_csv.writerow(encabezados)

    # Generar y escribir las filas modificadas en el archivo de salida
    for fila in lector_csv:
        fecha_generada = generar_fecha_aleatoria(
            fecha_inicio_parametro, fecha_fin_parametro)
        fila.append(fecha_generada)
        escritor_csv.writerow(fila)

print("Archivo CSV modificado creado con éxito.")
