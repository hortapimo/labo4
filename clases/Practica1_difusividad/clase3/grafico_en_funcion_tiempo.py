import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
import math
from scipy.special import erf

def tuki(nombre: Path):
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3,4,5,6), delimiter=',')
    return data.T

tiempo, t1, t2, t3, t4, t5, t6 = tuki("auxiliar.csv")

siz = 14
plt.figure(figsize=(8,6))
error=0
plt.errorbar(tiempo,t1,yerr=error, fmt=".", label="Ter. 1")
plt.errorbar(tiempo,t2,yerr=error, fmt=".", label="Ter. 2")
plt.errorbar(tiempo,t3,yerr=error, fmt=".", label="Ter. 3")
plt.errorbar(tiempo,t4,yerr=error, fmt=".", label="Ter. 4")
plt.errorbar(tiempo,t5,yerr=error, fmt=".", label="Ter. 5")
plt.errorbar(tiempo,t6,yerr=error, fmt=".", label="Ter. 6")
plt.xlabel("Tiempo [s]", fontsize=siz)
plt.ylabel("Temperatura [°C]", fontsize=siz)
plt.xticks(fontsize=siz)
plt.yticks(fontsize=siz)
plt.grid()
plt.legend(fontsize=siz+2)
plt.show()