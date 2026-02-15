import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt 
import cv2
import serial
import time
import csv
from datetime import datetime

#%%
# 1. Inicializamos la variable fuera
puertoSerial = None
try:
    # Abrimos el puerto de forma manual (sin 'with')
    puerto='COM6'
    puertoSerial = serial.Serial(port=puerto, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.05, xonxoff=0, rtscts=0)   
    # Es vital esperar un poco a que el hardware (ej. Arduino) se resetee al conectar
    time.sleep(2) 
    print(f"Conectado exitosamente a {puerto}")
except serial.SerialException as e:
    print(f"Error al conectar: {e}")
#%%
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not camara.isOpened():
    print("Error: No se puede abrir la cámara")
    exit()
camara.set(cv2.CAP_PROP_BUFFERSIZE, 1)
imagenVaso = cv2.imread("vaso.png", 0)
  
def obtenerAltura(): 
    time.sleep(0.1)
    camara.grab()
    ret, im = camara.read()
    # 4. Verificar si la lectura fue exitosa
    if not ret or im is None:
        print("Error: No se pudo capturar la imagen. ¿Está la cámara conectada?")
        exit()
        
    limites=[100, 1900, 120, 200]
    #limites=[118, 197, 128, 187]
    min_x, max_x, min_y, max_y = limites
    im = im[min_y:max_y, min_x:max_x, :]
    imagenCompleta = np.mean(im, axis=2)
    #imsave('completa.png', im, cmap='gray')
    
    imagenCompleta = np.asarray(imagenCompleta, np.uint8)
    
    res = cv2.matchTemplate(imagenCompleta, imagenVaso, cv2.TM_CCOEFF)
    top_left = cv2.minMaxLoc(res)[3]
    altura_pixeles = top_left[0]-19
    cm_pixel=0.13618677
    altura=altura_pixeles*cm_pixel
    
    return altura
#%%

P=0
PI=1
PID=2
MODO = PID #0 es solo P, 1 es PI, 2 es PID
kp = 0.9
ki = 0.3
kd = 0.4
constante = 170
set_value=30 #cm

archivo_data= open(f'kp{kp}_ki{ki}_kd{kd}_setValue{set_value}.csv', 'w', newline='', encoding='utf-8')
escritor = csv.writer(archivo_data)
escritor.writerow(["Tiempo", "Altura", "Senal_de_Control","Set_value"])

#loop principal
inicio = time.perf_counter()
tiempo = time.perf_counter()-inicio
print("iniciando")
j=0
error_acumulado = 0
errores = [0,0]
i=0
while(True):
    
    tiempo_anterior=tiempo
    altura = obtenerAltura()
    tiempo = time.perf_counter()-inicio
    delta_t = tiempo-tiempo_anterior
    error = set_value - altura
    error_acumulado += error*delta_t
    if i==0:
        error_anterior= 0
    else:
        error_anterior = errores[1]
    errores[0]=error_anterior
    errores[1]=error
    
    if MODO ==P:
        senial = kp*error  + constante#implementar como dijo damian
    elif MODO == PI:
      #  print('falta implementar!!')
        senial = kp*error  + constante + ki*error_acumulado
    elif MODO == PID:
        if i==0:
            delta_error=errores[1]
        else:
            delta_error=errores[1]-errores[0]
       # print('falta implementar!!')
        senial = kp*error  + constante + ki*error_acumulado + kd*delta_error/delta_t
        
    
    if senial > 255:
        senial = 255
    if senial<0:
        senial=0
        
    puertoSerial.write(bytes(f'a{senial}\n', 'utf-8'))
    
    senial_p= senial/255 *100
    escritor.writerow([tiempo, altura, senial_p, set_value])
    if(j>20):
        archivo_data.flush()
        print(f"tiempo[s]:{tiempo}, altura[cm]: {altura},  senial enviada[%]: {senial_p}, set_Value{set_value}")
        j=0
    j+=1
    i+=1
    

archivo_data.close()
puertoSerial.close()
