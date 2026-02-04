#Ajuste datos por exponencia osilante
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
plt.style.use('seaborn-v0_8-talk')

def funcionAjuste(t,A,B,C):
    return A+B*np.sin(C*t)

def tuki(nombre: Path):
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3,4,5,6), delimiter=',')
    return data.T

inicio=3300
w=2*np.pi*2e-3

tiempo, t1, t2, t3, t4, t5, t6 = tuki("auxiliar.csv")

termocuplas = [t1, t2, t3, t4, t5, t6]
guest_iniciales=[
    [150,15,w],
    [140,10,w],
    [120,5,w],
    [100,5,w],
    [80,5,w],
    [80,3,w]
    ]

for i in range(6):
    fig,ax=plt.subplots(figsize=(7,5.5))
    
    # Datos para el ajuste
    x_fit = tiempo[inicio:]
    y_fit = termocuplas[i][inicio:]
    sigma_y = 2.2 # Error de las termocuplas
    
    popt, pcov = curve_fit(funcionAjuste, x_fit, y_fit, p0=guest_iniciales[i])
    
    # --- CÁLCULO DEL CHI CUADRADO REDUCIDO ---
    y_pred = funcionAjuste(x_fit, *popt)
    residuos = y_fit - y_pred
    chi_cuadrado = np.sum((residuos / sigma_y)**2)
    grados_libertad = len(y_fit) - len(popt)
    chi_reducido = chi_cuadrado / grados_libertad
    # -----------------------------------------
    
    popt,pcov = curve_fit(funcionAjuste, tiempo[inicio:], termocuplas[i][inicio:], p0=guest_iniciales[i])
    ax.errorbar(tiempo[inicio::3], termocuplas[i][inicio::3],yerr=2.2, label=f"Datos termocupla #{i}", 
                zorder=3,fmt='s',color='black',ecolor='black', errorevery=4, capsize=5,ms=3,capthick=1.5,)
    
    # Agregamos el chi cuadrado al label usando el operador %
    label_ajuste = r"Ajuste: $%.1f ^{\circ}C + %.1f ^{\circ}C \cdot \sin(%.3f \frac{1}{s} \cdot t)$" % (popt[0], popt[1], popt[2])
    label_chi = r"$\chi^2_{\nu} = %.3f$" % chi_reducido
    # Unimos ambos en el label del plot (usando \n para que quede en dos líneas si quieres)
    ax.plot(x_fit, y_pred, zorder=10, label=label_ajuste + "\n" + label_chi)
    ax.grid(which='major')
    ax.set_xlabel("Tiempo [seg]")
    ax.set_ylabel(r"Temperatura $[^\circ C]$")
    ax.minorticks_on()
    y_min, y_max = ax.get_ylim()
    ax.set_ylim(y_min, y_max + (y_max - y_min) * 0.25)
    ax.legend(loc='upper left', frameon=True)
    ax.grid(which='minor', alpha=0.3)
    plt.savefig(f"resultado_termocupla_{i}.svg")
    plt.tight_layout()
    
