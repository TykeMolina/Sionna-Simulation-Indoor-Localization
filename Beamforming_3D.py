import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import cm

# ==========================================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================================
initial_theta_sigma = 0.2  # Valor inicial de Elevación
initial_phi_sigma = 1.0  # Valor inicial de Azimut

# Crear la figura y el eje 3D, dejando espacio abajo para los sliders
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.25)  # Margen inferior

# Crear la malla de ángulos fijos
phi = np.linspace(-np.pi, np.pi, 100)
theta = np.linspace(0, np.pi, 50)
Phi, Theta = np.meshgrid(phi, theta)

theta_center = np.pi / 2.0
phi_center = 0.0


# ==========================================================
# 2. FUNCIÓN MATEMÁTICA (Calcula las coordenadas)
# ==========================================================
def calculate_surface(theta_sig, phi_sig):
    # Ecuación de la campana de Gauss
    Gain = np.exp(-0.5 * (((Theta - theta_center) / theta_sig) ** 2 +
                          ((Phi - phi_center) / phi_sig) ** 2))

    # Coordenadas 3D
    X = Gain * np.sin(Theta) * np.cos(Phi)
    Y = Gain * np.sin(Theta) * np.sin(Phi)
    Z = Gain * np.cos(Theta)
    return X, Y, Z, Gain


# ==========================================================
# 3. RENDERIZADO VISUAL Y EJES
# ==========================================================
def format_axes():
    """Vuelve a aplicar las etiquetas y límites para que el gráfico no salte"""
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('Eje X (Frente a la puerta)')
    ax.set_ylabel('Eje Y (Pasillo lateral)')
    ax.set_zlabel('Eje Z (Techo/Suelo)')
    ax.set_title('Simulador de Beamforming Interactivo 6G', fontsize=14)


# Dibujar la superficie inicial
X, Y, Z, Gain = calculate_surface(initial_theta_sigma, initial_phi_sigma)
ax.plot_surface(X, Y, Z, facecolors=cm.jet(Gain), rstride=1, cstride=1,
                linewidth=0, antialiased=False, alpha=0.9)
format_axes()

# ==========================================================
# 4. CREACIÓN DE LOS SLIDERS INTERACTIVOS
# ==========================================================
# Definir las posiciones de los sliders en la ventana [x, y, ancho, alto]
ax_theta = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_phi = plt.axes([0.25, 0.05, 0.65, 0.03])

# Crear los objetos Slider
slider_theta = Slider(ax_theta, 'Apertura Vertical\n(Theta $\sigma$)',
                      valmin=0.05, valmax=1.5, valinit=initial_theta_sigma)

slider_phi = Slider(ax_phi, 'Apertura Horizontal\n(Phi $\sigma$)',
                    valmin=0.05, valmax=2.0, valinit=initial_phi_sigma)


# Función que se ejecuta cada vez que mueves el mouse en un slider
def update(val):
    ax.clear()  # Limpia el gráfico anterior

    # Obtiene los nuevos valores de los sliders
    t_sig = slider_theta.val
    p_sig = slider_phi.val

    # Recalcula y vuelve a dibujar
    X, Y, Z, Gain = calculate_surface(t_sig, p_sig)
    ax.plot_surface(X, Y, Z, facecolors=cm.jet(Gain), rstride=1, cstride=1,
                    linewidth=0, antialiased=False, alpha=0.9)
    format_axes()  # Reestablece los límites
    fig.canvas.draw_idle()  # Actualiza el dibujo en pantalla


# Conectar el evento de cambio a la función update
slider_theta.on_changed(update)
slider_phi.on_changed(update)

# Mostrar la ventana interactiva
plt.show()



