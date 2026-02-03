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

inicio=3000
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

fig,ax=plt.subplots()

for i in range(6):
    
    popt,pcov = curve_fit(funcionAjuste, tiempo[inicio:], termocuplas[i][inicio:], p0=guest_iniciales[i])
    ax.errorbar(tiempo[inicio::5], termocuplas[i][inicio::5],yerr=2.2, label=f"datos termocupla #{i}", zorder=3,fmt='o', errorevery=8, capsize=3,ms=3)
    ax.plot(tiempo[inicio:], funcionAjuste(tiempo[inicio:],popt[0],popt[1], popt[2]), zorder=10)
ax.grid(which='major')
ax.minorticks_on()
ax.grid(which='minor', alpha=0.3)
ax.legend()