import pandas as pd
import matplotlib.pyplot as plt

# Configuración del archivo
archivo = 'cl.csv' 

df = pd.read_csv('cl.csv', 
                 header=None, 
                 encoding_errors='ignore', 
                 on_bad_lines='skip')
