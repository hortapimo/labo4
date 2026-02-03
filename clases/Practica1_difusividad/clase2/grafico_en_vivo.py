# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. CARGA DE DATOS ---
# Supongamos que tu archivo se llama 'datos_difusividad.csv'
# Si la primera fila es el tiempo, lo cargamos sin encabezado primero
df = pd.read_csv('auxiliar.csv', header=None)

# Extraemos el tiempo (primera fila)
tiempos = df.iloc[0, :].values

# Extraemos las temperaturas (todas las filas siguientes)
# Cada fila representa un sensor a una distancia distinta
temperaturas = df.iloc[1:, :].values

# Definimos las distancias (eje X)
# Si no las tienes en el CSV, puedes crearlas manualmente. 
# Por ejemplo, si tenés 5 sensores cada 1 cm:
cant_sensores = temperaturas.shape[0]
distancias = np.linspace(0, 10, cant_sensores) # De 0 a 10 cm

# --- 2. PREPARACIÓN DE LA MALLA (MESHGRID) ---
# Para graficar superficies 3D, necesitamos una grilla de coordenadas
X, Z = np.meshgrid(distancias, tiempos)

# La matriz de temperaturas debe estar transpuesta para coincidir con la grilla
# si X es (sensores) y Z es (tiempos)
Y = temperaturas.T 

# --- 3. GRÁFICO 3D ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficamos la superficie
# cmap='hot' o 'viridis' suelen ser buenos para temperatura
surf = ax.plot_surface(X, Z, Y, cmap='magma', edgecolor='none', alpha=0.8)

# Etiquetas según tu pedido
ax.set_xlabel('Distancia (x)')
ax.set_ylabel('Tiempo (z)')
ax.set_zlabel('Temperatura (y)')
ax.set_title('Perfil de Temperatura en función de Distancia y Tiempo')

# Añadimos una barra de color
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Temp (°C)')

# Ajustamos el ángulo de visión inicial
ax.view_init(elev=30, azim=45)

plt.show()