import numpy as np
from scipy.integrate import quad

# ==========================================================
# 1. PARÁMETROS DEL SISTEMA (Ingresá tus medidas en metros)
# ==========================================================
D_tubo = 0.09565      # Diámetro interno del tubo (ej: 120mm)
D_i = 0.04575         # Diámetro inferior del vaso (base menor)
D_s = 0.07880         # Diámetro superior del vaso (base mayor)
h_v = 0.09380         # Altura del vaso
m_v = 0.005         # Masa del vaso en kg (ej: 5 gramos)
Q = 0.0236          # Caudal del ventilador en m^3/s (85 m^3/h)
rho_aire = 1.225    # Densidad del aire (kg/m^3)
V_vaso = 0.0003     # Volumen de aire desplazado por el vaso (m^3)
g = 9.81            # Gravedad (m/s^2)

# ==========================================================
# 2. DEFINICIÓN DE LA FUNCIÓN A INTEGRAR (BETA)
# ==========================================================
def integrand_beta(y, D_tubo, D_i, D_s, h_v):
    # Pendiente de ensanchamiento del vaso
    k = (D_s - D_i) / h_v
    
    # Numerador: D'(y) * D(y) -> surge de derivar el área proyectada
    numerador = (k**2)*y+k*D_i
    # Denominador: (D_tubo^2 - D_y^2)^2 -> surge de la velocidad local al cuadrado
    denominador = (D_tubo**2 - (D_i+k*y)**2)**2
    
    return numerador / denominador

# ==========================================================
# 3. RESOLUCIÓN NUMÉRICA
# ==========================================================
# Calculamos la integral beta entre 0 y h_v
beta, error_estimado = quad(integrand_beta, 0, h_v, args=(D_tubo, D_i, D_s, h_v))

# Término correspondiente al choque en la base plana (A_p(0))
termino_base = (D_i / D_tubo**2)**2 * (4 / np.pi)

# Calculamos el Coeficiente de Drag experimental (Cd)
# Usando la fórmula despejada de tu modelo:
numerador_Cd = 2 * g * (m_v - rho_aire * V_vaso)
denominador_Cd = rho_aire * (Q**2) * ((8 / np.pi) * beta + (4 / np.pi) * (D_i**2 / D_tubo**4))

Cd = numerador_Cd / denominador_Cd

# ==========================================================
# 4. SALIDA DE RESULTADOS
# ==========================================================
print("-" * 40)
print(f"{'RESULTADOS DEL MODELO':^40}")
print("-" * 40)
print(f"Valor de la integral (beta): {beta:.6f}")
print(f"Error numérico estimado:    {error_estimado:.2e}")
print(f"Coeficiente de Drag (Cd):    {Cd:.4f}")
print("-" * 40)