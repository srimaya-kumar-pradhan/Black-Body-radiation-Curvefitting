import numpy as np

# Physical Constants
h = 6.62607015e-34  # Planck constant (J*s)
c = 2.99792458e8    # Speed of light (m/s)
k = 1.380649e-23    # Boltzmann constant (J/K)

def planck_law(wavelength, T):
    """
    Computes spectral radiance according to Planck's Law.
    """
    exponent = (h * c) / (wavelength * k * T)
    exponent = np.clip(exponent, None, 700) # prevent overflow
    intensity = (2 * h * c**2) / (wavelength**5) * (1 / (np.exp(exponent) - 1))
    return intensity

def generate_synthetic_data(T_true, num_points=300, noise_level=0.10):
    """
    Generates synthetic blackbody radiation data with scaled noise.
    """
    wavelengths = np.linspace(100e-9, 3000e-9, num_points)
    intensity_true = planck_law(wavelengths, T_true)
    
    noise = noise_level * np.max(intensity_true) * np.random.normal(size=num_points)
    intensity_noisy = np.maximum(intensity_true + noise, 0)
    
    return wavelengths, intensity_noisy, intensity_true
