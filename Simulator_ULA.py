import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Configuración inicial de tu ULA
N_init = 4
d_init = 0.5 # Separación en longitudes de onda (lambda/2)

# Ecuación del Factor de Arreglo (Array Factor)
def calcular_af(N, d, theta):
    AF = np.zeros_like(theta, dtype=complex)
    for n in range(1, int(N) + 1):
        # Fase para cada antena basándonos en su posición
        fase = (n - 1) * (1j * 2 * np.pi * d * np.cos(theta))
        AF += np.exp(fase)
    return np.abs(AF)

# Preparar la gráfica polar
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)

theta = np.linspace(0, 2 * np.pi, 360)
AF_mag = calcular_af(N_init, d_init, theta)
linea, = ax.plot(theta, AF_mag, color='red', lw=2)
ax.set_title('Factor de Arreglo (ULA)\n', fontsize=14)

# Configurar Sliders interactivos
axcolor = 'lightgrey'
ax_N = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_d = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)

s_N = Slider(ax_N, 'Elementos (N)', 1, 16, valinit=N_init, valstep=1)
s_d = Slider(ax_d, 'Separación (d/λ)', 0.1, 2.0, valinit=d_init)

# Función de actualización al mover los sliders
def update(val):
    N = s_N.val
    d = s_d.val
    nuevo_AF = calcular_af(N, d, theta)
    linea.set_ydata(nuevo_AF)
    ax.set_rmax(np.max(nuevo_AF) + 0.5) # Ajustar el zoom dinámicamente
    fig.canvas.draw_idle()

s_N.on_changed(update)
s_d.on_changed(update)

plt.show()