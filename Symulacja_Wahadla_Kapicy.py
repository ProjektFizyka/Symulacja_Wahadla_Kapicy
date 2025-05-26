import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Parametry fizyczne
L = 1.0
A = 0.1
g = 9.81
dt = 0.02
t_max = 10
t_vals = np.arange(0, t_max, dt)

# Warunki początkowe
theta0 = np.pi - 0.1
theta_dot0 = 0.0

# Obliczenie wartości granicznej omega
omega_critical = np.sqrt(2 * g / A)  # ok. 14.0
omega_init = omega_critical  # startujemy dokładnie od wartości krytycznej

# Funkcja do symulacji
def simulate_kapitza(omega):
    theta_vals = [theta0]
    theta_dot_vals = [theta_dot0]
    for t in t_vals[:-1]:
        theta = theta_vals[-1]
        theta_dot = theta_dot_vals[-1]
        y_ddot = -omega ** 2 * A * np.sin(omega * t)
        theta_ddot = -(g + y_ddot) / L * np.sin(theta)
        theta_dot_new = theta_dot + theta_ddot * dt
        theta_new = theta + theta_dot_new * dt
        theta_dot_vals.append(theta_dot_new)
        theta_vals.append(theta_new)
    return theta_vals

theta_vals = simulate_kapitza(omega_init)
x_trail = []
y_trail = []

# Tworzenie wykresu
fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
plt.subplots_adjust(bottom=0.25)
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Kapitza Pendulum")

line, = ax.plot([], [], 'r-', lw=3)
bob, = ax.plot([], [], 'o', markersize=15, color='blue')
pivot, = ax.plot([], [], 'ko', markersize=5)
trail, = ax.plot([], [], 'g-', lw=1)
time_text = ax.text(1.1, 1.6, '', ha='center')
freq_text = ax.text(-1.9, 1.6, '', ha='left', fontsize=10)

# Suwak
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
omega_slider = Slider(ax_slider, 'Omega', 5.0, 100.0, valinit=omega_init, valstep=0.1)

# 🔴 Czerwona kreska na suwaku przy omega_critical
ax_slider.axvline(x=omega_critical, color='red', linestyle='--', label='omega_critical')

def init():
    line.set_data([], [])
    bob.set_data([], [])
    trail.set_data([], [])
    time_text.set_text('')
    return line, bob, pivot, trail, time_text, freq_text

def update(frame):
    global theta_vals, x_trail, y_trail
    t = t_vals[frame]
    theta = theta_vals[frame]
    omega = omega_slider.val
    y0 = A * np.cos(omega * t)
    x = L * np.sin(theta)
    y = y0 - L * np.cos(theta)

    x_trail.append(x)
    y_trail.append(y)

    line.set_data([0, x], [y0, y])
    bob.set_data([x], [y])
    trail.set_data(x_trail, y_trail)
    time_text.set_text(f'time = {t:.2f} s\nomega = {omega:.1f}')
    freq_text.set_text(f'freq = {omega / (2 * np.pi):.2f} Hz')
    return line, bob, pivot, trail, time_text, freq_text

def update_omega(val):
    global theta_vals, x_trail, y_trail
    omega = omega_slider.val
    theta_vals = simulate_kapitza(omega)
    x_trail = []
    y_trail = []

omega_slider.on_changed(update_omega)

ani = FuncAnimation(fig, update, frames=len(t_vals), init_func=init, blit=True, interval=dt * 1000)
plt.show()
