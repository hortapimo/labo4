#Ajuste datos por exponencia osilante
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from scipy import stats
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
fig,ax=plt.subplots(figsize=(8,8),nrows=3, ncols=2,sharex=True,constrained_layout=True)
n=0
for i in range(3):
    for j in range(2):
        # Datos para el ajuste
        x_fit = tiempo[inicio:]
        y_fit = termocuplas[n][inicio:]
        sigma_y = 2.2 # Error de las termocuplas
        
        popt, pcov = curve_fit(funcionAjuste, x_fit, y_fit, p0=guest_iniciales[n])
        
        # --- CÁLCULO DEL CHI CUADRADO REDUCIDO ---
        y_pred = funcionAjuste(x_fit, *popt)
        residuos = y_fit - y_pred
        chi_cuadrado = np.sum((residuos / sigma_y)**2)
        grados_libertad = len(y_fit) - len(popt)
        chi_reducido = chi_cuadrado / grados_libertad
        # -----------------------------------------
        
        popt,pcov = curve_fit(funcionAjuste, tiempo[inicio:], termocuplas[n][inicio:], p0=guest_iniciales[n])
        ax[i,j].errorbar(tiempo[inicio::3], termocuplas[n][inicio::3],yerr=2.2, label=f"Datos termocupla #{n+1}", 
                    zorder=3,fmt='s',color='black',ecolor='black', errorevery=4, capsize=5,ms=3,capthick=1.5,)
        
        # Agregamos el chi cuadrado al label usando el operador %
        label_ajuste = r"Ajuste: $%.1f ^{\circ}C + %.3f ^{\circ}C \cdot \sin(%.6f \frac{1}{s} \cdot t)$" % (popt[0], popt[1], popt[2])
        label_chi = r"$\chi^2_{\nu} = %.3f$" % chi_reducido
        
        p_valor = stats.chi2.sf(chi_reducido, grados_libertad)
        label_p =f"p={p_valor}"
        # Unimos ambos en el label del plot (usando \n para que quede en dos líneas si quieres)
        ax[i,j].plot(x_fit, y_pred, zorder=10, label=label_ajuste + "\n" + label_chi+ "\n" +label_p)
        ax[i,j].grid(which='major')
        if(i==2):
            ax[i,j].set_xlabel("Tiempo [seg]")
        ax[i,j].set_ylabel(r"Temperatura $[^\circ C]$")
        ax[i,j].minorticks_on()
        y_min, y_max = ax[i,j].get_ylim()
        ax[i,j].set_ylim(y_min, y_max + (y_max - y_min) * 0.25)
        ax[i,j].legend(fontsize='x-small', loc='upper right')
        ax[i,j].grid(which='minor', alpha=0.3)
        n=n+1
    
    
plt.savefig(f"resultado_termocuplas.svg")    
