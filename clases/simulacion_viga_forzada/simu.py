"""
La ecuacion diferencial es la siguiente:
    q'' + 2 alpha q' + (EI/rho)K_n² q = f(t)
llevo la ecuacion a un sistema de orden 1, defino a l=q'
 Entonces ahora tengo ahora el siguiente sistema acoplado de primer orden:
     l' + 2 alpha l+(EI/rho)K_n² q =f(t)
     l=q'
Que lo puedo rescribir de la siguiente manera para poder tratarlo vectorialmente
l'=f(t)-2 alpha l+(EI/rho)K_n² q
q'=l
Donde el vector es X=(l,q)
Resuelvo esto usando runge kutta, uso la implementacion que esta en scipy
"""
#%% simualcion primer modo
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- Parámetros Físicos y Geométricos ---
D = 0.005          # Diámetro en metros 
L = 0.48           # Longitud en metros
alpha = 0.13      # Coeficiente de amortiguamiento (ajustar según experimento)
frec_f = 64.0     # Frecuencia del forzamiento en Hz

E = 105e9         # Módulo de Young del Latón (Pa) 
peso = 0.085    # kg

# Cálculos de geometría circular
Area = np.pi * (D**2) / 4
I = np.pi * (D**4) / 64
rho_lin = peso / L  

# Constantes beta*L para los primeros 3 modos (Cantilever)
beta_L = np.array([1.8751, 4.6941, 7.8548])
# Calculamos Kn para cada modo: Kn = (beta_L / L)^2
Kn = (beta_L / L)**2

def f_ext(t, frec):
    # f(t) es la fuerza externa normalizada
    return np.sin(2 * np.pi * frec * t)

def Ed(t, X, frec,K,f_ext):
    """
    X[0] = l = q' (velocidad)
    X[1] = q (desplazamiento)
    """
    # l' = f(t) - 2*alpha*l - (EI/rho)*K^2 * q
    dldt = f_ext(t, frec) - 2*alpha*X[0] - (E*I/rho_lin)*(K**2)*X[1]
    # q' = l
    dqdt = X[0]
    
    return [dldt, dqdt]

# --- Simulación ---
t_span = (0, 10) 
t_eval = np.linspace(0, 3, 10000)
X0 = [0, 0] # Condición inicial: reposo

# Resolver usando solve_ivp (RK45 por defecto)
sol = solve_ivp(Ed, t_span, X0, t_eval=t_eval, args=(frec_f,Kn[1],f_ext))

# --- Gráfico de Deflexión ---
plt.figure(figsize=(10, 5))
plt.plot(sol.t, sol.y[1], label=r'Deflexión $q(t)$')
plt.title("Modelado de Barra laton- 1 modo")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [m]")
plt.grid(True, linestyle='--')
plt.legend()
plt.show()

#%% simulacion varios modos en conjunto, con frecuencia variable

def f_ext_2(t, frec):
    # f(t) es la fuerza externa normalizada
    if t<10:
        return np.sin(2 * np.pi * frec * t)
    else:
        return np.sin(2 * np.pi * frec*6 * t)
frec=10#Hz
t_span = (0, 20) 
t_eval = np.linspace(0, 20, 90000)
X0 = [0, 0] # Condición inicial: reposo

sol1 = solve_ivp(Ed, t_span, X0, t_eval=t_eval, args=(frec,Kn[0],f_ext_2))
sol2 = solve_ivp(Ed, t_span, X0, t_eval=t_eval, args=(frec,Kn[1],f_ext_2))

y= 2*sol1.y[1]+2*sol2.y[1]
fig, ax= plt.subplots()
ax.plot(sol1.t, y, label=r'Deflexión $q(t)$')
ax.set_title("Modelado de Barra laton- 2 modos. f variable")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud [m]")
ax.grid(True, linestyle='--')
ax.legend()


#%% calculo frecuencia

# Expresión para la frecuencia natural fn en Hz
f_n = (Kn / (2 * np.pi)) * np.sqrt((E * I) / rho_lin)
# Mostrar resultados
for i, f in enumerate(f_n):
    print(f"Frecuencia del armónico {i+1}: {f:.2f} Hz")