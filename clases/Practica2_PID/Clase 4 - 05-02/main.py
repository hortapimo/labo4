import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt 
import cv2
import serial
import time
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
def obtenerAltura():
    camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(0.5)
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
    imsave('completa.png', im, cmap='gray')
    
    imagenVaso = cv2.imread("vaso.png", 0)
    imagenCompleta = np.asarray(imagenCompleta, np.uint8)
    
    res = cv2.matchTemplate(imagenCompleta, imagenVaso, cv2.TM_CCOEFF)
    top_left = cv2.minMaxLoc(res)[3]
    altura_pixeles = top_left[0]-19
    cm_pixel=0.13618677
    altura=altura_pixeles*cm_pixel
    
    return altura


P=0
PI=1
PID=2
MODO = P #0 es solo P, 1 es PI, 2 es PID

while(True):
    altura = obtenerAltura()
    print(f"altura medida:{altura}")    
    set_value=30 #cm
    error = set_value - altura
    print(f"error: {error}")
    kp = 0.5
    
    constante = 170
    if MODO ==P:
        senial = kp*error  + constante#implementar como dijo damian
    elif MODO == PI:
        print('falta implementar!!')
        #senial = kp*error  + constante
    elif MODO == PID:
        print('falta implementar!!')
        #senial = kp*error  + constante
        
    senial = int(senial)
    if senial > 255:#hay que ver el caso de acotar con PID
        senial = 255
    print(f"senial enviada: {senial}")
    puertoSerial.write(bytes(f'a{senial}\n', 'utf-8'))



puertoSerial.close()
