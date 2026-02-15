import numpy as np
import time
import matplotlib.pyplot as plt
import Agilent34970A_multiplexor 
import TektronixAFG3021B as tek
import csv
import os

DUTY_HIGH = 99.999
DUTY_LOW = 0.001
#%%
lectorCanales= Agilent34970A_multiplexor.Agilent34970A(name= 'ASRL2::INSTR')
distancias=np.array([81.4, 123.1, 164, 211.9, 249.6, 410.5])
generadorSeniales= tek.AFG3021B('USB0::0x0699::0x0346::C036492::INSTR')
#%%
#lectorCanales._mux.write('*RST')
time.sleep(1)
data = lectorCanales.one_scan()
temperaturaCaneles = data[1].astype(float)[:-2]
print(temperaturaCaneles)

fig,ax = plt.subplots()
ax.scatter(distancias,temperaturaCaneles)
ax.set_xlabel("distancia [mm]")
ax.set_ylabel("Temperatura [Cº]")
ax.grid(which="major")
ax.minorticks_on()
ax.grid(which="minor", alpha=0.3)
#%%
#Prueba rapida para ver transitorio
import csv
import os
# 1. Definir el nombre del archivo
archivo_datos = "mediciones_difusividad.csv"

# 2. Preparar el encabezado (Header)
# Creamos nombres de columnas según la cantidad de distancias que tienes
header = ['Tiempo'] + [f'Temp_Dist_{d}mm' for d in distancias]

# Crear el archivo y escribir el encabezado
with open(archivo_datos, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

generadorSeniales.setDuty(DUTY_HIGH)
periodoMediciones = 30 

print(f"Iniciando toma de datos. Guardando en: {archivo_datos}")
i=0
while(True):
    try:
        # Toma de datos
        data, temperatura, tiempo, canal = lectorCanales.one_scan()
        temp_float = temperatura.astype(float)[:-2]
        
        # 3. Guardar en el archivo (Modo 'a' de append)
        with open(archivo_datos, mode='a', newline='') as f:
            writer = csv.writer(f)
            # Combinamos el tiempo con la lista de temperaturas
            fila = [i*periodoMediciones] + list(temp_float)
            writer.writerow(fila)
        
        print(f"Medición guardada - Tiempo: {i*periodoMediciones} s")
        
        # (Aquí iría tu código de actualización de gráfico que vimos antes)
        
        time.sleep(periodoMediciones)
        i=i+1    
    except Exception as e:
        print(f"Error detectado: {e}")
        time.sleep(5) # Esperar un poco antes de reintentar
    
#%%