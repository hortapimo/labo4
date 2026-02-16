import numpy as np
from scipy.integrate import quad

def resolver_integral():
    """
    Calcula numéricamente la integral de la imagen.
    Ds: Diámetro superior del objeto
    Di: Diámetro inferior del objeto
    hv: Altura del objeto (límite superior de integración)
    Dtubo: Diámetro del tubo
    """
    Ds= 0.0788
    Di=0.04575
    hv =0.0938
    Dtubo =0.09565
    # Definimos la constante fuera para mayor claridad
    cte = 8 / np.pi
    
    # Pendiente de la variación del diámetro (m)
    m = (Ds - Di) / hv
    
    def integrand(y):
        # Numerador: m^2 * y + Di * m
        numerador = (m**2) * y + Di * m
        
        # Denominador: (Dtubo^2 - (Di + m*y)^2)^2
        # Notar que (Di + m*y) es el diámetro local del objeto a altura y
        denominador = (Dtubo**2 - (Di + m * y)**2)**2
        
        return cte * (numerador / denominador)

    # Realizamos la integración desde 0 hasta hv
    resultado, error_estimado = quad(integrand, 0, hv)
    
    return resultado

# --- Ejemplo de uso con valores arbitrarios ---
# Ajustá estos valores a los de tu experimento:

resultado_final = resolver_integral()

print(f"El resultado de la integral es: {resultado_final:.6f}")
