import numpy as np

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

def temperature_to_color(T):
    """
    Approximates RGB color for a given temperature (K) for visualization.
    Uses a simple standardized mapping based on typical star colors.
    """
    T = np.clip(T, 1000, 40000)
    
    if T < 3500:
        return '#ff3300' # Red
    elif T < 5000:
        return '#ff9900' # Orange
    elif T < 6000:
        return '#ffe666' # Yellow
    elif T < 7500:
        return '#ffffff' # White
    elif T < 10000:
        return '#cce6ff' # Blue-white
    else:
        return '#99ccff' # Blue

def get_star_class(T):
    """Returns the Morgan-Keenan spectral classification based on temperature."""
    if T >= 30000: return "O-type (Blue star)"
    elif T >= 10000: return "B-type (Blue-white star)"
    elif T >= 7500: return "A-type (White star)"
    elif T >= 6000: return "F-type (Yellow-white star)"
    elif T >= 5200: return "G-type (Yellow dwarf / Sun-like)"
    elif T >= 3700: return "K-type (Orange dwarf)"
    else: return "M-type (Red dwarf)"
