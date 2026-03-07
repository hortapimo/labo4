import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d


# Configuración del archivo
archivo = 'captura_laton_Vertical_acelerometro_1.csv' 

def media_movil(señal, n=5):
    # Creamos una ventana de pesos iguales que sumen 1
    ventana = np.ones(n) / n
    return np.convolve(señal, ventana, mode='same')

df = pd.read_csv(archivo,skiprows=1)
df.columns = ['t', 'az', 'ay','ax']
ac= np.sqrt(df['az']**2+df['ay']**2+df['ax']**2)
fig, ax = plt.subplots()
taux=df['t']-df['t'][0]
#ax.scatter(taux, df['az'], label="az")
#ax.scatter(taux, df['ay'],label="ay")
#ax.scatter(taux, df['ax'],label="ax")
ax.set_xlabel(f"t[$\mu$s]")
ax.set_ylabel(f"Amplitud")
ax.plot(df['t'], ac,label="a")
ax.legend()

#%%
ac_filtrada = media_movil(ac, n=10)
ac_filtrada_2 = savgol_filter(ac, window_length=11, polyorder=2)
t= df['t']-df['t'][0]
fig3, ax3 = plt.subplots()
# ax3.scatter(t,ac_filtrada, label="filtro media movil")
ax3.scatter(t,ac, label="datos", marker="p")
# ax3.scatter(t,ac_filtrada_2, label="filtro savgol",marker="v")



t_fijo = np.linspace(t[0], t[len(t)-1], len(t))
f_interp = interp1d(t, ac, kind='cubic')
ac_interpolada  = f_interp(t_fijo)

ax3.scatter(t_fijo,ac_interpolada, label="interpolada",marker="x")
ax3.legend()
fig4, ax4= plt.subplots()
ax4.scatter(t_fijo, ac_interpolada)

#%%
t_fijo_seg=t_fijo*1e-6
frecuencias_busqueda = np.linspace(1, 150, 5000)
ang_freqs = 2 * np.pi * frecuencias_busqueda
pgram = lombscargle(t_fijo_seg, ac_interpolada, ang_freqs)

fig2, ax2 = plt.subplots()
ax2.plot(frecuencias_busqueda, pgram)
ax2.set_yscale("log")
ax2.set_title("Periodograma de Lomb-Scargle (Datos Irregulares)")
#%%
from scipy.signal.windows import hann, hamming, blackman
from scipy.signal import spectrogram
ac_interpolada_sin_media = ac_interpolada-np.mean(ac_interpolada)
fft_valores = np.fft.fft(ac_interpolada_sin_media)
fs=1/(t_fijo_seg[4]-t_fijo_seg[3])
frecuencias = np.fft.fftfreq(len(t), 1/fs)

N = len(ac_interpolada_sin_media)
ventana = hamming(N)
señal_ventaneada = ac_interpolada_sin_media * ventana* 2.0
fft_valores_ventana = np.fft.fft(señal_ventaneada)
# Solo nos interesa la mitad positiva del espectro
n = len(t) // 2
fig5,ax5=plt.subplots()
ax5.set_yscale("log")
ax5.plot(frecuencias[1:n], np.abs(fft_valores[1:n]))
#ax5.plot(frecuencias[1:n], np.abs(fft_valores_ventana[1:n]))

f, t, Sxx = spectrogram(ac_interpolada_sin_media, fs)
fig6,ax6=plt.subplots()
ax6.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')