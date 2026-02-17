import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
rango_0bolitas = (120, 374)
rango_1bolitas = (120, 374)
rango_2bolitas = (210, 1300)
rango_3bolitas = (538, 914)
rango_4bolitas = (400, 915)


#%%
fileName="kp4.8_ki2.0_kd2.9_setValue50.0_pruebaPesos_1bolitas_prueba2.csv"
df = pd.read_csv(fileName)

tiempo = df['Tiempo']
senial = df['Senal_de_Control']
altura = df['Altura']
set_value = df['Set_value']


#%%
inicio = rango_1bolitas[0]
fin = rango_1bolitas[1]
promedio = np.mean(senial[inicio:fin])
desvio = np.std(senial[inicio:fin])
desvioMEdia = promedio/np.sqrt(len(senial[inicio:fin]))
print(promedio)
print(desvioMEdia)
print(desvio)

#%%
plt.style.use("seaborn-v0_8-talk")
seniales_promedio = np.array([63.8, 70.2,75.9, 85.9, 92.2])
std_seniales = np.array([4, 4.4,2.3,4.4,4]) #Tioene la señal muy cortado en la ultima medicion con lo cual el devio tiene un sesgo importante, lo multiplico por 2 asumiendo e l doble de la desicacion debido al corte
caudal = 85*seniales_promedio/100
errorCaudal=std_seniales*85/100
masa = np.array([2052.2, 2286.9, 2530.9, 2907, 3117.8])

fig,ax=plt.subplots(figsize=(6,5))
ax.scatter(tiempo, senial,label="señal",s=15)
ax.plot(tiempo,promedio*np.ones(len(tiempo)), label=f"señal media, $\mu$={promedio:.0f}", c="0.1" )
ax.plot([],[], label=rf"$\sigma_{{\mu}}=${desvioMEdia:.1f}", c="1")
ax.grid(which='major')
ax.minorticks_on()
ax.grid(which='minor', alpha=0.3)
ax.set_ylabel(f"Señal [%]")
ax.set_xlabel(f"tiempo [seg]")
ax.legend()
plt.tight_layout()

#%%
fi2,ax2 = plt.subplots(figsize=(7,5))
ax2.errorbar(masa,caudal, yerr=errorCaudal, fmt='s', ecolor='black', capthick=2,capsize=8)
ax2.grid(which='major')
ax2.minorticks_on()
ax2.grid(which='minor', alpha=0.3)
ax2.set_ylabel(f"Caudal de aire [m$^3$/h]")
ax2.set_xlabel(f"Masa vaso [g]")
plt.tight_layout()
fi2.savefig("caudalPeso.pdf")