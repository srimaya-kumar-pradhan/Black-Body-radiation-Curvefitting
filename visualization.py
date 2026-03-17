import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from planck import planck_law
from utils import temperature_to_color

def plot_static_fit(wavelengths, intensity_noisy, intensity_fit, intensity_true, T_true, T_est):
    """Saves the final static plot of the optimized curve fit."""
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    plt.scatter(wavelengths * 1e9, intensity_noisy, color='gray', s=10, label='Observation Data', alpha=0.5)
    plt.plot(wavelengths * 1e9, intensity_true, 'w--', label=f'True Curve ({T_true}K)', alpha=0.5)
    
    color_est = temperature_to_color(T_est)
    plt.plot(wavelengths * 1e9, intensity_fit, color=color_est, linewidth=2, label=f'Fitted Model ({T_est:.0f}K)')
    
    plt.title('Blackbody Radiation Fit', fontsize=14, fontweight='bold', color='white')
    plt.xlabel('Wavelength (nm)', fontsize=12, color='white')
    plt.ylabel('Spectral Radiance', fontsize=12, color='white')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/static_fit.png', dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def plot_star(T_est, star_class):
    """Renders a visually appealing star based on the estimated temperature using glow techniques."""
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    color = temperature_to_color(T_est)
    
    # Draw nested circles with decreasing alpha for a glow effect
    for alpha, size in zip(np.linspace(0.05, 0.4, 10), np.linspace(15000, 2000, 10)):
        ax.scatter([0], [0], s=size, color=color, alpha=0.1, edgecolors='none')
        
    ax.scatter([0], [0], s=1200, color='white', alpha=0.9, edgecolors='none') # Solid Core
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    plt.title(f"{star_class}\nEstimated T = {T_est:.0f} K", color=color, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('results/star_visualization.png', dpi=300, facecolor='black')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def plot_black_hole(T_est):
    """Renders a simplified artistic accretion disk using concentric rings."""
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    color_base = temperature_to_color(T_est)
    
    # Event horizon (absolute black in the center)
    circle_eh = plt.Circle((0, 0), 0.3, color='black', zorder=10)
    ax.add_artist(circle_eh)
    
    # Photon ring and accretion disk layers
    for radius in np.linspace(0.3, 0.8, 30):
        # Brightness drops off exponentially from the event horizon
        alpha = np.exp(-10 * (radius - 0.3))
        circle_disk = plt.Circle((0, 0), radius, color=color_base, alpha=alpha * 0.5, fill=False, linewidth=12, zorder=1)
        ax.add_artist(circle_disk)
        
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    plt.title('Accretion Disk Temperature Proxy', color='white', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/black_hole.png', dpi=300, facecolor='black')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def launch_interactive_slider():
    """Launches an interactive matplotlib window with a slider to adjust Temperature."""
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')
    
    wavelengths = np.linspace(100e-9, 3000e-9, 500)
    initial_T = 5800
    
    line, = ax.plot(wavelengths * 1e9, planck_law(wavelengths, initial_T), color=temperature_to_color(initial_T), lw=3)
    ax.set_xlim(0, 3000)
    
    # Base the y-limit on a max reference temperature so the curve doesn't just jump off screen constantly
    y_max_ref = np.max(planck_law(wavelengths, 8000))
    ax.set_ylim(0, y_max_ref * 0.5) 
    
    ax.set_xlabel('Wavelength (nm)', color='white')
    ax.set_ylabel('Spectral Radiance', color='white')
    ax.set_title('Interactive Blackbody Explorer\n(Move the slider to see color and intensity shift)', color='white', pad=15)
    ax.grid(alpha=0.2)
    
    plt.subplots_adjust(bottom=0.25)
    
    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='black')
    T_slider = Slider(
        ax=ax_slider,
        label='Temperature (K)',
        valmin=2000,
        valmax=15000,
        valinit=initial_T,
        color='cyan'
    )
    
    def update(val):
        T = T_slider.val
        curr_y = planck_law(wavelengths, T)
        line.set_ydata(curr_y)
        line.set_color(temperature_to_color(T))
        
        # Dynamically bump Y-axis if we exceed it
        curr_max = np.max(curr_y)
        if curr_max > ax.get_ylim()[1] or curr_max < ax.get_ylim()[1] * 0.1:
            ax.set_ylim(0, curr_max * 1.5)
            
        fig.canvas.draw_idle()
        
    T_slider.on_changed(update)
    plt.show()

def animate_optimization(wavelengths, intensity_noisy, T_true, guess_history):
    """Animates the curve fitting process progressing over multiple iteration guesses."""
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.style.use('dark_background')
    
    ax.scatter(wavelengths * 1e9, intensity_noisy, color='gray', s=10, alpha=0.5, label='Actual Data')
    line, = ax.plot([], [], 'r-', lw=2, label='Optimizer Guess')
    
    ax.set_xlim(np.min(wavelengths * 1e9), np.max(wavelengths * 1e9))
    max_y = np.max(intensity_noisy)
    ax.set_ylim(0, max_y * 1.2)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Intensity')
    title_text = ax.set_title('Curve Fitting Optimizer Progress', fontsize=14, color='white')
    ax.legend(loc='upper right')
    
    def init():
        line.set_data([], [])
        return line,
        
    def animate(i):
        T = guess_history[i]
        y = planck_law(wavelengths, T)
        line.set_data(wavelengths * 1e9, y)
        line.set_color(temperature_to_color(T))
        title_text.set_text(f'Optimization Iteration {i+1}/{len(guess_history)} - Guessed T: {T:.0f}K')
        return line, title_text
        
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(guess_history), blit=False, interval=150, repeat=False)
    
    try:
        # Attempt to save a GIF
        ani.save('results/optimization.gif', writer='pillow', fps=8)
    except Exception as e:
        print(f"   [Notice] Could not save GIF (Pillow might be missing). {e}")
        
    plt.show(block=False)
    plt.pause(len(guess_history) * 0.15 + 1.5)
    plt.close()
