
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

plt.style.use("seaborn-v0_8-talk")
seniales_promedio = np.array([63.8, 70.2,75.9, 85.9, 92.2])
std_seniales = np.array([4, 4.4,2.3,4.4,4]) #Tioene la señal muy cortado en la ultima medicion con lo cual el devio tiene un sesgo importante, lo multiplico por 2 asumiendo e l doble de la desicacion debido al corte
caudal = 85*seniales_promedio/100*1/3600#m^3/seg
errorCaudal=std_seniales*85/100*1/3600
errorCaudal_rel = errorCaudal/caudal
error_caudalCuadradoRel = 2*errorCaudal_rel
masa = np.array([2052.2, 2286.9, 2530.9, 2907, 3117.8])*1e-6
fi2,ax2 = plt.subplots(figsize=(7,5))


ax2.errorbar(masa,caudal**2, yerr=error_caudalCuadradoRel*caudal**2, fmt='s', ecolor='black', capthick=2,capsize=8)
ax2.grid(which='major')
ax2.minorticks_on()
ax2.grid(which='minor', alpha=0.3)
ax2.set_ylabel(f"Caudal de aire [m$^3$/s]")
ax2.set_xlabel(f"Masa vaso [kg]")


def ajuste(m,Cd):
    #la expresion sera del tipo A*B*1/C_d*m + D*(1/Cd)
    rho=1.184#kg/m^3
    g=9.81#m/s^2
    beta=252.7#1/m^2
    D_i=0.04575
    D_t=0.09565
    V=6.4866e-5
    A=(2*g)/rho
    B=1/(beta +((D_i/(D_t**2))**2)*(4/np.pi))
    D=2*V*g/((beta +((D_i/(D_t**2))**2)*(4/np.pi)))
    
    return A*B*(1/Cd)*m-D*(1/Cd)

res = curve_fit(ajuste,masa, caudal**2,p0=[0.7])
masa_aux=np.linspace(2000e-6,3200e-6,100)
ax2.plot(masa_aux, ajuste(masa_aux,res[0]))


ax2.plot()
plt.tight_layout()
fi2.savefig("caudalPeso.pdf")
