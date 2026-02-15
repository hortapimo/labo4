import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-v0_8-talk')

def funcionAjuste(t, A, B, C):
    return A + B * np.sin(C * t)

def tuki(nombre: Path):
    # Simulando carga de datos
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3,4,5,6), delimiter=',')
    return data.T

# --- CONFIGURACIÓN ---
inicio = 3300
w = 2 * np.pi * 2e-3
sigma_y = 2.2 
tiempo, t1, t2, t3, t4, t5, t6 = tuki("auxiliar.csv") # Descomentar en tu PC
termocuplas = [t1, t2, t3, t4, t5, t6]
guest_iniciales=[
    [150,15,w],
    [140,10,w],
    [120,5,w],
    [100,5,w],
    [80,5,w],
    [80,3,w]
    ]
# Crear la figura con GridSpec para tener control total de los tamaños
fig = plt.figure(figsize=(12, 14))
# Definimos 3 bloques de filas, cada bloque tiene 2 sub-filas (Ajuste y Residuo)
# 'height_ratios' da más espacio al ajuste (ratio 3) que al residuo (ratio 1)
outer_gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.25)

n = 0
for i in range(3):
    for j in range(2):
        # Crear un sub-grid para cada par (Ajuste, Residuo)
        inner_gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer_gs[i, j], 
                                                   height_ratios=[3, 1], hspace=0.05)
        
        ax_main = fig.add_subplot(inner_gs[0, 0])
        ax_res = fig.add_subplot(inner_gs[1, 0], sharex=ax_main)

        # --- LÓGICA DE DATOS Y AJUSTE ---
        x_fit = tiempo[inicio:]
        y_fit = termocuplas[n][inicio:]
        popt, pcov = curve_fit(funcionAjuste, x_fit, y_fit, p0=guest_iniciales[n])
        
        y_pred = funcionAjuste(x_fit, *popt)
        residuos = y_fit - y_pred
        
        # Estadísticos
        chi_cuadrado = np.sum((residuos / sigma_y)**2)
        grados_libertad = len(y_fit) - len(popt)
        chi_reducido = chi_cuadrado / grados_libertad
        p_valor = stats.chi2.sf(chi_cuadrado, grados_libertad)

        # --- GRÁFICO PRINCIPAL ---
        ax_main.errorbar(tiempo[inicio::10], termocuplas[n][inicio::10], yerr=sigma_y, 
                         fmt='s', color='black', ecolor='black', capsize=3, ms=2, 
                         label=f"Datos termocupla #{n+1}", alpha=0.5)
        
        label_txt = (r"Ajuste: $%.1f + %.2f \sin(%.4f t)$" % (popt[0], popt[1], popt[2]) + 
                     "\n" + r"$\chi^2_{\nu} = %.3f$" % chi_reducido + f"\n p={p_valor:.2f}")
        
        ax_main.plot(x_fit, y_pred, color='tab:blue', zorder=10, label=label_txt)
        ax_main.set_ylabel(r"Temp $[^\circ C]$")
        ax_main.legend(fontsize='xx-small', loc='upper right')
        ax_main.grid(True, alpha=0.3)
        plt.setp(ax_main.get_xticklabels(), visible=False) # Oculta X en el de arriba

        # --- GRÁFICO DE RESIDUOS ---
        ax_res.errorbar(x_fit[::10], residuos[::10], yerr=sigma_y, fmt='o', ms=2, alpha=0.6)
        ax_res.axhline(0, color='red', linestyle='--', lw=1)
        ax_res.set_ylabel("Res. [°C]", fontsize='small')
        ax_res.grid(True, alpha=0.3)
        
        if i == 2:
            ax_res.set_xlabel("Tiempo [seg]")
        
        n += 1
plt.tight_layout()
plt.show()