import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
#from scipy.optimize import curve_fit

RUTA_CARPETA = Path(r"F:\Juan\UBA\Materias\Física\Laboratorio 4\Control PID\Clase 6")

def tuki(nombre: str):
    ruta_completa = RUTA_CARPETA / nombre
    data = np.genfromtxt(ruta_completa, skip_header=1, usecols=(0,1,2,3), delimiter=',')
    return data.T

error = 2.05 # cm

plt.rc('font', size=24)
def gr_ziegler(archivo, kp, nombre):
    tiempo, altura, senial, set_value = tuki(archivo)
    ki = kp*2/(4.75)
    kd = kp *(4.75)/8
    fig,ax = plt.subplots(figsize=(16,8))
    ax.errorbar(tiempo, altura, label="Datos", fmt=".",zorder=2)
    ax.errorbar(tiempo, altura, yerr=error,label="Incertezas", fmt=".",zorder=1)
    ax.plot(tiempo, set_value, label="Set value",c='0.1', zorder=3, lw=3)# = {set_value[-1]:.0f} cm",c='0.1')
    ax.plot([],[]," ",label=r"$K_P$ = "f"{kp:.1f} | "r"$K_I$ = "f"{ki:.1f} | "r"$K_D$ = "f"{kd:.1f}")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Altura [cm]")
   # ax.set_ylim(10,63)
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor", alpha=0.3)
    ax.legend()
    ruta_pdf = RUTA_CARPETA / f"{nombre}.pdf"
    ruta_png = RUTA_CARPETA / f"{nombre}.png"
    fig.savefig(ruta_pdf, bbox_inches='tight')
    fig.savefig(ruta_png, bbox_inches='tight')
    plt.show()

gr_ziegler("kp4.8_ki2.0210526315789474_kd2.85_setValue50_escalon.csv",
           4.8, "escalon_2valores")

gr_ziegler("kp4.8_ki2.0_kd2.9_setValue55.0_vqariosEscalones.csv",
           4.8, "escalon_varios")

#%%
def gr_calib(archivo, kp, nombre):
    tiempo, altura, senial, set_value = tuki(archivo)
    tiempo = tiempo[:4100]
    altura = altura[:4100]
    senial = senial[:4100]
    set_value = set_value[:4100]
    fig,ax = plt.subplots(figsize=(16,8))
    ax.errorbar(tiempo, altura, label="Datos", fmt=".",zorder=2)
    ax.errorbar(tiempo, altura, yerr=error,label="Incertezas", fmt=".",zorder=1)
    ax.plot(tiempo, set_value, label="Set value",c='0.1', zorder=3, lw=3)
    ax.plot([],[]," ",label=r"$K_P$ = "f"{kp:.1f}")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Altura [cm]")
   # ax.set_ylim(10,63)
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor", alpha=0.3)
    ax.legend()
    ruta_pdf = RUTA_CARPETA / f"{nombre}.pdf"
    ruta_png = RUTA_CARPETA / f"{nombre}.png"
    fig.savefig(ruta_pdf, bbox_inches='tight')
    fig.savefig(ruta_png, bbox_inches='tight')
    plt.show()

gr_calib("kp5_ki0.3_kd3.5_setValue30.csv",
           5, "calib_ziegler_kp5")

gr_calib("kp8_ki0.3_kd3.5_setValue30.csv",
           8, "calib_ziegler_kp8_usamos")

gr_calib("kp9_ki0.3_kd3.5_setValue30.csv",
           9, "calib_ziegler_kp9")

gr_calib("kp10_ki0.3_kd3.5_setValue30.csv",
           10, "calib_ziegler_kp10")



#%%

def gr_peso(archivo, kp, nombre,peso):
    tiempo, altura, senial, set_value = tuki(archivo)
    ki = kp*2/(4.75)
    kd = kp *(4.75)/8
    fig,ax = plt.subplots(figsize=(16,8))
    ax.errorbar(tiempo, altura, label="Datos", fmt=".",zorder=2)
    ax.errorbar(tiempo, altura, yerr=error,label="Incertezas", fmt=".",zorder=1)
    ax.plot(tiempo, set_value, label="Set value",c='0.1', zorder=3, lw=3)
    ax.plot([],[]," ",label=r"$K_P$ = "f"{kp:.1f} | "r"$K_I$ = "f"{ki:.1f} | "r"$K_D$ = "f"{kd:.1f}")
    ax.plot([],[]," ",label=f"Peso: {peso}")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Altura [cm]")
   # ax.set_ylim(10,63)
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor", alpha=0.3)
    ax.legend()
    ruta_pdf = RUTA_CARPETA / f"{nombre}.pdf"
    ruta_png = RUTA_CARPETA / f"{nombre}.png"
    fig.savefig(ruta_pdf, bbox_inches='tight')
    fig.savefig(ruta_png, bbox_inches='tight')
    plt.show()


gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_sinpeso.csv",
           4.8, "vaso_sinpeso_p1", "sin bolita")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_0bolitas_prueba2.csv",
           4.8, "vaso_sinpeso_p2", "sin bolita")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_1bolita.csv",
           4.8, "vaso_1bolita_p1", "1 bolita")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_1bolitas_prueba2.csv",
           4.8, "vaso_1bolita_p2", "1 bolita")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_2bolita.csv",
           4.8, "vaso_2bolitas_p1", "2 bolitas")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_2bolitas_prueba2.csv",
           4.8, "vaso_2bolitas_p2", "2 bolitas")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_3bolita.csv",
           4.8, "vaso_3bolitas_p1", "3 bolitas")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_3bolitas_prueba2.csv",
           4.8, "vaso_3bolitas_p2", "3 bolitas")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_4bolita.csv",
           4.8, "vaso_4bolitas_p1", "4 bolitas")

gr_peso("kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_4bolitas_prueba1.csv",
           4.8, "vaso_4bolitas_p2", "4 bolitas")





