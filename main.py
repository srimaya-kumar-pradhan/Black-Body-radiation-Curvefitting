import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from planck import planck_law, generate_synthetic_data
from utils import compute_metrics, get_star_class
import visualization

def main():
    print("🚀 Starting Astrophysics Blackbody Simulation...\n")
    
    os.makedirs('results', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # 1. Generate Environment
    T_true = 5800  # Sun-like star
    print(f"🌌 Generating synthetic spectral data for True T = {T_true} K")
    wavelengths, intensity_noisy, intensity_true = generate_synthetic_data(T_true, num_points=200, noise_level=0.1)
    
    # Save simulated data
    np.savez('data/synthetic_spectral_data.npz', wavelengths=wavelengths, intensity_noisy=intensity_noisy)
    
    # 2. Optimization (Curve Fitting with history)
    print(f"⚙️ Running nonlinear optimization tracking iterations...")
    guess_history = []
    
    def residual(params, wl, data):
        T = params[0]
        # Append only if it significantly moved to reduce frame bloat
        if not guess_history or abs(guess_history[-1] - T) > 50:
            guess_history.append(T)
        model = planck_law(wl, T)
        return data - model
        
    # Start intentionally low so the optimizer has to travel (good for animation)
    initial_guess = [2000.0]  
    res = least_squares(residual, initial_guess, args=(wavelengths, intensity_noisy), bounds=(1000, 20000))
    
    T_est = res.x[0]
    star_class = get_star_class(T_est)
    
    if guess_history[-1] != T_est:
        guess_history.append(T_est)
    
    # Evaluate
    intensity_fit = planck_law(wavelengths, T_est)
    mse, r2, perc_error, accuracy = compute_metrics(intensity_noisy, intensity_fit, T_true, T_est)
    
    print("\n✅ Optimization Complete:")
    print(f"   - Estimated Temperature: {T_est:.0f} K")
    print(f"   - Star Classification:   {star_class}")
    print(f"   - Estimation Accuracy:   {accuracy:.2f}%\n")
    
    # Ensure a non-blocking interactive environment for the sequential popups
    plt.ion() 
    
    print("🎬 1. Animating optimization process... (Check pop-up window)")
    visualization.animate_optimization(wavelengths, intensity_noisy, T_true, guess_history)
    
    print("📊 2. Rendering static fit plot...")
    visualization.plot_static_fit(wavelengths, intensity_noisy, intensity_fit, intensity_true, T_true, T_est)
    
    print("⭐ 3. Rendering Star Visualization based on temperature...")
    visualization.plot_star(T_est, star_class)
    
    print("🌌 4. Rendering simple Accretion Disk proxy...")
    visualization.plot_black_hole(T_est)
    
    print("\n🎛️ 5. Launching Interactive Slider... (Close the window to exit program)")
    plt.ioff() # Turn interactive mode off for the final blocking window
    visualization.launch_interactive_slider()
    
    print("\n🎉 Simulation Finished successfully!")

if __name__ == "__main__":
    # Suppress verbose warnings from matplotlib bounds interactions locally
    import warnings
    warnings.filterwarnings("ignore")
    plt.rcParams['toolbar'] = 'None' 
    main()
