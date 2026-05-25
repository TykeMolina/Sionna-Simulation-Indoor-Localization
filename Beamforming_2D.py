import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
initial_theta_sigma = 0.2
initial_phi_sigma = 1.0

# Crear figura con 2 subgráficos polares
fig, (ax_phi, ax_theta) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))
plt.subplots_adjust(bottom=0.3, wspace=0.3)

# Generar 360 puntos (de -pi a pi) para hacer el círculo completo
phi_angles = np.linspace(-np.pi, np.pi, 360)
theta_angles = np.linspace(-np.pi, np.pi, 360)

# ==========================================
# 2. FUNCIONES DE CÁLCULO (CORTES 2D)
# ==========================================
def calc_gain_azimut(phi_sig):
    """Corte Horizontal: Elevación fija en 90° (pi/2)"""
    # La ecuación gaussiana solo depende de Phi ahora
    return np.exp(-0.5 * (phi_angles / phi_sig)**2)

def calc_gain_elevacion(theta_sig):
    """Corte Vertical: Azimut fijo al frente (0°)"""
    # Usamos valor absoluto para que la gráfica sea simétrica arriba y abajo
    theta_center = np.pi / 2.0
    return np.exp(-0.5 * ((np.abs(theta_angles) - theta_center) / theta_sig)**2)

# ==========================================
# 3. DIBUJAR GRÁFICAS POLARES
# ==========================================
# Plano Azimutal (Horizontal)
line_phi, = ax_phi.plot(phi_angles, calc_gain_azimut(initial_phi_sigma), color='blue', lw=2.5)
ax_phi.set_title("Corte Azimutal (Horizontal)\nVista desde arriba", va='bottom', fontsize=12)
ax_phi.set_rmax(1.0) # Potencia máxima 1
ax_phi.set_rticks([0.2, 0.5, 0.8, 1.0])
ax_phi.set_yticklabels([]) # Ocultar números del radio para limpieza

# Plano de Elevación (Vertical)
line_theta, = ax_theta.plot(theta_angles, calc_gain_elevacion(initial_theta_sigma), color='red', lw=2.5)
ax_theta.set_title("Corte de Elevación (Vertical)\nVista de lado", va='bottom', fontsize=12)
# Configurar para que 0° (Zenith) esté arriba y 90° (Horizonte) a la derecha
ax_theta.set_theta_zero_location("N")
ax_theta.set_theta_direction(-1)
ax_theta.set_rmax(1.0)
ax_theta.set_rticks([0.2, 0.5, 0.8, 1.0])
ax_theta.set_yticklabels([])

# ==========================================
# 4. SLIDERS INTERACTIVOS
# ==========================================
ax_slider_t = plt.axes([0.25, 0.15, 0.5, 0.03])
ax_slider_p = plt.axes([0.25, 0.08, 0.5, 0.03])

slider_t = Slider(ax_slider_t, 'Apertura Vertical\n(Theta $\sigma$)', 0.05, 1.5, valinit=initial_theta_sigma, color='red')
slider_p = Slider(ax_slider_p, 'Apertura Horizontal\n(Phi $\sigma$)', 0.05, 2.0, valinit=initial_phi_sigma, color='blue')

def update(val):
    # Actualizar la data 'Y' (que en polar es el Radio/Ganancia)
    line_phi.set_ydata(calc_gain_azimut(slider_p.val))
    line_theta.set_ydata(calc_gain_elevacion(slider_t.val))
    fig.canvas.draw_idle()

slider_t.on_changed(update)
slider_p.on_changed(update)

plt.show()