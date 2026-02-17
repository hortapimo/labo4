import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

# Configuración de estilo profesional
plt.style.use("seaborn-v0_8-talk")
#plt.rcParams.update({'font.family': 'serif', 'text.usetex': False}) # Usar True si tenés LaTeX instalado

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
Cd_error = np.sqrt(pcov[0,0])

# --- ESTADÍSTICAS ---
y_fit = ajuste(masa, Cd_fit)
chi_cuadrado = np.sum(((y_exp - y_fit) / y_err)**2)
gl = len(masa) - 1 
chi_cuadrado_red = chi_cuadrado / gl
p_valor = stats.chi2.sf(chi_cuadrado, gl)

# --- PROPAGACIÓN DE ERROR PARA BANDAS DE CONFIANZA ---
# Derivada parcial |dy/dCd| = |y / Cd| para este modelo lineal en 1/Cd
masa_aux = np.linspace(min(masa)*0.95, max(masa)*1.05, 100)
y_aux = ajuste(masa_aux, Cd_fit)
y_aux_error = np.abs(y_aux / Cd_fit) * Cd_error # Error propagado

# --- GRÁFICO ---
fig, (ax_top, ax_res) = plt.subplots(2, 1, figsize=(7, 6), sharex=True, 
                                     gridspec_kw={'height_ratios': [3, 1]})

factor_eje_y = 1e4
factor_eje_x = 1e6 # Para visualizar en mg

# Gráfico principal
ax_top.errorbar(masa*factor_eje_x, y_exp*factor_eje_y, yerr=y_err*factor_eje_y, 
                fmt='s', color='black', markerfacecolor='white', markeredgewidth=1.5,
                ecolor='black', capsize=4, label="Datos experimentales", zorder=3)

ax_top.plot(masa_aux*factor_eje_x, y_aux*factor_eje_y, color='firebrick', lw=2,
            label=f"Ajuste: $C_d = {Cd_fit:.2f} \pm {Cd_error:.2f}$", zorder=2)

# Banda de confianza (1 sigma)
ax_top.fill_between(masa_aux*factor_eje_x, (y_aux - y_aux_error)*factor_eje_y, 
                    (y_aux + y_aux_error)*factor_eje_y, color='firebrick', alpha=0.15, 
                    label="Banda de confianza ($1\sigma$)", zorder=1)

# Cuadro de texto con métricas
stats_text = (f"$\chi^2_{{\\nu}} = {chi_cuadrado_red:.2f}$\n"
              f"$p$-valor $= {p_valor:.2f}$")
ax_top.text(0.05, 0.92, stats_text, transform=ax_top.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.8), fontsize=12)

ax_top.set_ylabel(r"$Q^2$ [$10^{-4}$ m$^6$/s$^2$]", fontsize=13)
ax_top.legend(loc='lower right', frameon=True, fontsize=11)

# --- GRÁFICO DE RESIDUOS CORREGIDO ---
residuos = y_exp - y_fit
ax_res.errorbar(masa*factor_eje_x, residuos*factor_eje_y, yerr=y_err*factor_eje_y, 
                fmt='s',                 # Cambiado a cuadrado para consistencia
                color='royalblue',       # Color de la línea de conexión (si hubiera)
                ecolor='black',          # Color de las barras de error
                capsize=3,               # Ancho de los remates de las barras
                markerfacecolor='white', # Fondo blanco para resaltar
                markeredgecolor='black', # Borde negro (esto arregla el problema)
                markeredgewidth=1.5)     # Grosor del borde

ax_res.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.7)
ax_res.set_ylabel(r"Residuos", fontsize=12)
ax_res.set_xlabel("Masa del vaso [mg]", fontsize=13)

# Ajustes finales de grilla y escala
for ax in [ax_top, ax_res]:
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(labelsize=11)

plt.tight_layout()
plt.subplots_adjust(hspace=0.1)
plt.show()