import numpy as np

# Physical Constants
h = 6.62607015e-34  # Planck constant (J*s)
c = 2.99792458e8    # Speed of light (m/s)
k = 1.380649e-23    # Boltzmann constant (J/K)

def planck_law(wavelength, T):
    """
    Computes spectral radiance according to Planck's Law.
    
    Parameters:
    - wavelength: array of wavelengths in meters.
    - T: temperature in Kelvin.
    
    Returns:
    - intensity: spectral radiance array.
    """
    exponent = (h * c) / (wavelength * k * T)
    exponent = np.clip(exponent, None, 700) # prevent overflow
    intensity = (2 * h * c**2) / (wavelength**5) * (1 / (np.exp(exponent) - 1))
    return intensity

def generate_synthetic_data(T_true, num_points=200, noise_level=0.05):
    """
    Generates synthetic blackbody radiation data with scaled noise.
    
    Parameters:
    - T_true: Source temperature in K.
    - num_points: Number of discrete wavelengths.
    - noise_level: Fractional noise standard deviation.
    
    Returns:
    - wavelengths: array in meters
    - intensity_noisy: array with noise
    - intensity_true: noiseless array
    """
    wavelengths = np.linspace(100e-9, 3000e-9, num_points)
    intensity_true = planck_law(wavelengths, T_true)
    
    noise = noise_level * np.max(intensity_true) * np.random.normal(size=num_points)
    intensity_noisy = np.maximum(intensity_true + noise, 0)
    
    return wavelengths, intensity_noisy, intensity_true

def compute_metrics(y_true, y_pred, T_true, T_est):
    """
    Computes relevant performance metrics for the curve fit.
    """
    mse = np.mean((y_true - y_pred)**2)
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    
    r2 = 1.0 if ss_tot == 0 else 1 - (ss_res / ss_tot)
    
    percentage_error = np.abs(T_true - T_est) / T_true * 100
    accuracy = 100 - percentage_error
    
    return mse, r2, percentage_error, accuracy
