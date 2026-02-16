import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

plt.style.use("seaborn-v0_8-talk")

# --- DATOS ---
seniales_promedio = np.array([63.8, 70.2, 75.9, 85.9, 92.2])
std_seniales = np.array([4, 4.4, 2.3, 4.4, 4]) 
caudal = 85*seniales_promedio/100*1/3600 
errorCaudal = std_seniales*85/100*1/3600
error_caudalCuadradoRel = 2 * (errorCaudal/caudal)
y_exp = caudal**2
y_err = error_caudalCuadradoRel * y_exp
masa = np.array([2052.2, 2286.9, 2530.9, 2907, 3117.8])*1e-6

def ajuste(m, Cd):
    rho, g, beta = 1.184, 9.81, 252.7
    D_i, D_t, V = 0.04575, 0.09565, 6.4866e-5
    A = (2*g)/rho
    B = 1/(beta + ((D_i/(D_t**2))**2)*(4/np.pi))
    D = 2*V*g/((beta + ((D_i/(D_t**2))**2)*(4/np.pi)))
    return A*B*(1/Cd)*m - D*(1/Cd)

# --- AJUSTE PONDERADO ---
popt, pcov = curve_fit(ajuste, masa, y_exp, p0=[0.7], sigma=y_err, absolute_sigma=True)
Cd_fit = popt[0]
# El error de Cd es la raíz cuadrada de la diagonal de la matriz de covarianza
Cd_error = np.sqrt(pcov[0,0])

# --- ESTADÍSTICAS ---
y_fit = ajuste(masa, Cd_fit)
chi_cuadrado = np.sum(((y_exp - y_fit) / y_err)**2)
gl = len(masa) - 1 
chi_cuadrado_red = chi_cuadrado / gl
p_valor = stats.chi2.sf(chi_cuadrado, gl)

# --- GRÁFICO ---
fig, (ax_top, ax_res) = plt.subplots(2, 1, figsize=(7, 6), sharex=True, 
                                     gridspec_kw={'height_ratios': [3, 1]})

factor_eje_y = 1e4
factor_eje_x = 1e6 # Para visualizar en mg

# Gráfico principal con Cd +/- error en la leyenda
ax_top.errorbar(masa*factor_eje_x, y_exp*factor_eje_y, yerr=y_err*factor_eje_y, fmt='s', ecolor='black', 
                capthick=2, capsize=8, label="Datos exp.")

masa_aux = np.linspace(min(masa)*0.98, max(masa)*1.02, 100)
ax_top.plot(masa_aux*factor_eje_x, ajuste(masa_aux, Cd_fit)*factor_eje_y, color='red', 
            label=f"Ajuste: $C_d = {Cd_fit:.3f} \pm {Cd_error:.3f}$")

# Cuadro de texto simplificado
stats_text = (f"$\chi^2_{{red}} = {chi_cuadrado_red:.2f}$\n"
              f"$p$-valor $= {p_valor:.3f}$")
ax_top.text(0.05, 0.95, stats_text, transform=ax_top.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.5), fontsize=13)

ax_top.set_ylabel(r"Caudal$^2$ [m$^6$/s$^2 \cdot 10^{-4}$]")
ax_top.legend(loc='lower right')
ax_top.grid(True, which="both", alpha=0.3)
ax_top.minorticks_on()

# Gráfico de residuos
residuos = y_exp - y_fit
ax_res.errorbar(masa*factor_eje_x, residuos*factor_eje_y, yerr=y_err*factor_eje_y, fmt='o', color='purple', 
                ecolor='black', capsize=4)
ax_res.axhline(0, color='black', linestyle='--', linewidth=1)
ax_res.set_ylabel(r"Res. [m$^6$/s$^2 \cdot 10^{-4}$]")
ax_res.set_xlabel("Masa vaso [mg]")
ax_res.grid(True, which="both", alpha=0.3)
ax_res.minorticks_on()

plt.tight_layout()
plt.subplots_adjust(hspace=0.08)
plt.show()