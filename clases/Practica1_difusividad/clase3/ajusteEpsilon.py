#Ajuste datos por exponencia osilante
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
plt.style.use('seaborn-v0_8-talk')

def tuki(nombre: Path):
    data = np.genfromtxt(nombre, skip_header=1, usecols=(0,1,2,3,4,5,6), delimiter=',')
    return data.T

inicio=3300
w=2*np.pi*2e-3

tiempo, t1, t2, t3, t4, t5, t6 = tuki("auxiliar.csv")

termocuplas = [t1, t2, t3, t4, t5, t6]
def fAux(x,Tref,Amp):
    epsilon=0.0071028
    omega=0.01256637061 
    v=1.52
    return Amp*np.exp(-epsilon*x)*np.cos(omega*(t-x/v)) + Tref

def ajusteExponencial(x,y):
    def fAjuste(x,epsilon,theta0):
        return theta0*np.exp(-epsilon*x)
    
    return curve_fit(fAjuste, x, y,p0=(0.0071028,20))

epsilons=np.zeros(len(tiempo[2324:]))#el 2324 el tiempo es 7000s que es cuando ya la parte exponencial apenas se observa

#%% probemos con un solo tiempo para ver si tengo cosas coerentes, por ejemplo el que esta en 1200s, ya que hay un pico y deberia ser mas facil de ajustar

t=tiempo[4000]
y=np.zeros(6)
x=np.array([81.4, 123.1, 164.0, 241.9, 249.6, 410.5])
Tref = np.array([164.5, 157, 150.4, 143.3, 138.8, 125.7 ])
Amp=np.array([11.889, 8.237, 5.742, 3.696, 2.669, 0.7])
i=0
for ter in termocuplas:
    y[i]=ter[4000]
    i+=1

parametros, covariaza = ajusteExponencial(x, Amp)

#%%

import matplotlib.gridspec as gridspec
from scipy import stats

# --- Configuración de la figura con GridSpec ---
fig = plt.figure(figsize=(7, 7))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)

ax = fig.add_subplot(gs[0])     # Gráfico principal
ax_res = fig.add_subplot(gs[1], sharex=ax) # Gráfico de residuos

# --- Cálculos previos para el ajuste y estadística ---
sigma_y = 2.2
y_modelo_puntos = parametros[1] * np.exp(-parametros[0] * x)
residuos = Amp - y_modelo_puntos

# Cálculo de Chi Cuadrado y P-valor
chi_absoluto = np.sum((residuos / sigma_y)**2)
dof = len(Amp) - 2 # 2 parámetros: Amplitud y Coef. de decaimiento
chi_reducido = chi_absoluto / dof
p_valor = stats.chi2.sf(chi_absoluto, dof) # Se usa el absoluto para el p-valor

# --- Gráfico Principal ---
ax.errorbar(x, Amp, yerr=sigma_y, label="Datos", capthick=2, fmt='s', zorder=3)

x_aux = np.linspace(81, 410, 100)
y_modelo_curva = parametros[1] * np.exp(-parametros[0] * x_aux)

# Leyenda con LaTeX y estadísticos
label_ajuste = r"Ajuste: $%.2f ^\circ C \cdot e^{-%.4f \frac{1}{mm} x}$" % (parametros[1], parametros[0])
label_stats = r"$\chi^2_{\nu} = %.3f$ | $p = %.2f$" % (chi_reducido, p_valor)

ax.plot(x_aux, y_modelo_curva, label=label_ajuste + "\n" + label_stats, c="0.2", zorder=4)

# Estética del principal
ax.legend(fontsize='small')
ax.grid(which="major")
ax.set_ylabel(r"Amplitud de oscilación [$^\circ C$]")
ax.minorticks_on()
ax.grid(which="minor", alpha=0.3)
plt.setp(ax.get_xticklabels(), visible=False)

# --- Gráfico de Residuos ---
ax_res.errorbar(x, residuos, yerr=sigma_y, fmt='s', capsize=3, color='tab:blue', alpha=0.7)
ax_res.axhline(0, color='red', linestyle='--', lw=1.5)

ax_res.grid(which="major")
ax_res.grid(which="minor", alpha=0.3)
ax_res.minorticks_on()
ax_res.set_xlabel("Posición de termocupla x [mm]")
ax_res.set_ylabel("Res. [°C]")

plt.tight_layout()
plt.show()