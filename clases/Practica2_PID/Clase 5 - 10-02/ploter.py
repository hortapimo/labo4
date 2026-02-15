import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from datetime import datetime

def tuki(nombre: Path):
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3), delimiter=',')
    return data.T

kp=0.9
ki=0.3
kd=0.4
set_value_aux =30
tiempo, altura, senial, set_value = tuki("_aux.csv")

fig,ax = plt.subplots()
ax.errorbar(tiempo, altura, fmt="o", label="Altura")
ax.errorbar(tiempo, senial, fmt="o", label="Señal")
ax.plot(tiempo, set_value, label=f"Set value = {set_value[-1]} cm")
#ax.plot([],[]," ",label=r"$K_P$ = "f"{kp}")
#ax.plot([],[]," ",label=r"$K_I$ = "f"{ki}")
#ax.plot([],[]," ",label=r"$K_D$ = "f"{kd}")
ax.plot([],[]," ",label=r"$K_P$ = "f"{kp} | "r"$K_I$ = "f"{ki} | "r"$K_D$ = "f"{kd}")



ax.set_xlabel("tiempo")
ax.grid(which="major")
ax.minorticks_on()
ax.grid(which="minor", alpha=0.3)
ax.legend()


fig.savefig(f'kp{kp}_ki{ki}_kd{kd}_setValue{set_value_aux}.png')
plt.show()

