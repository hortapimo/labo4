import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from datetime import datetime

def tuki(nombre: Path):
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3), delimiter=',')
    return data.T

kp = 0.6*8
ki = kp*2/(4.75)
kd = kp *(4.75)/8
set_value_aux =50
tiempo, altura, senial, set_value = tuki("aux.csv")

fig,ax = plt.subplots()
ax.scatter(tiempo, altura, label="Altura [cm]")
#ax.scatter(tiempo, senial, label="Señal")
ax.plot(tiempo, set_value, label=f"Set value = {set_value[-1]:.0f} cm",c='0.1')
#ax.plot([],[],label=r"$K_P$ = "f"{kp}")
#ax.plot([],[],label=r"$K_I$ = "f"{ki}")
#ax.plot([],[],label=r"$K_D$ = "f"{kd}")
ax.plot([],[]," ",label=r"$K_P$ = "f"{kp:.1f} | "r"$K_I$ = "f"{ki:.1f} | "r"$K_D$ = "f"{kd:.1f}")
ax.set_xlabel("Tiempo [s]")
ax.grid(which="major")
ax.minorticks_on()
ax.grid(which="minor", alpha=0.3)
ax.legend()


fig.savefig(f'kp{kp}_ki{ki}_kd{kd}_setValue{set_value_aux}.png')
plt.show()

