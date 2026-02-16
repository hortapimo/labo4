import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

plt.style.use("seaborn-v0_8-talk")

# Datos
seniales_promedio = np.array([63.8, 70.2, 75.9, 85.9, 92.2])
std_seniales = np.array([4, 4.4, 2.3, 4.4, 4]) 
caudal = 85*seniales_promedio/100*1/3600 # m^3/seg
errorCaudal = std_seniales*85/100*1/3600
error_caudalCuadradoRel = 2 * (errorCaudal/caudal)
y_exp = caudal**2
y_err = error_caudalCuadradoRel * y_exp
masa = np.array([2052.2, 2286.9, 2530.9, 2907, 3117.8])*1e-6

def ajuste(m, Cd):
    rho = 1.184
    g = 9.81
    beta = 252.7
    D_i = 0.04575
    D_t = 0.09565
    V = 6.4866e-5
    A = (2*g)/rho
    B = 1/(beta + ((D_i/(D_t**2))**2)*(4/np.pi))
    D = 2*V*g/((beta + ((D_i/(D_t**2))**2)*(4/np.pi)))
    return A*B*(1/Cd)*m - D*(1/Cd)

# Ajuste
popt, pcov = curve_fit(ajuste, masa, y_exp, p0=[0.7])
Cd_fit = popt[0]

# Cálculo de residuos
residuos = y_exp - ajuste(masa, Cd_fit)

# --- CREACIÓN DEL GRÁFICO DOBLE ---
# subplots(2, 1) crea dos filas, sharex alinea el eje X, 
# y gridspec_kw le da menos altura al de abajo.
fig, (ax_top, ax_res) = plt.subplots(2, 1, figsize=(8, 8), sharex=True, 
                                     gridspec_kw={'height_ratios': [3, 1]})

# Gráfico principal
factor_eje_y=1e4
factor_eje_x=1e6
ax_top.errorbar(masa*factor_eje_x, y_exp*factor_eje_y, yerr=y_err*factor_eje_y, fmt='s', ecolor='black', 
                capthick=2, capsize=8, label="Datos exp.")
masa_aux = np.linspace(min(masa)*0.98, max(masa)*1.02, 100)
ax_top.plot(masa_aux*factor_eje_x, ajuste(masa_aux, Cd_fit)*factor_eje_y, color='red', label=f"Ajuste ($C_d$={Cd_fit:.2f})")
ax_top.set_ylabel(rf"Caudal$^2$ [m$^6$/s$^2$]$\cdot 10^{-4}$")
ax_top.legend()
ax_top.grid("major")
ax_top.minorticks_on()
ax_top.grid("minor", alpha=0.3)

# Gráfico de residuos
ax_res.errorbar(masa*factor_eje_x, residuos*factor_eje_y, yerr=y_err*factor_eje_y, fmt='o', color='purple', 
                ecolor='black', capsize=4)
ax_res.axhline(0, color='black', linestyle='--', linewidth=1) # Línea en cero
ax_res.set_ylabel("Residuos")
ax_res.set_xlabel("Masa vaso [mg]")
ax_res.grid("major")
ax_res.minorticks_on()
ax_res.grid("minor", alpha=0.3)

# Ajustes estéticos finales
plt.tight_layout()
plt.subplots_adjust(hspace=0.05) # Une un poco más los gráficos
plt.show()
fig.savefig("caudalPeso_con_residuos.pdf")
