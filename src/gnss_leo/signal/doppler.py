"""
Doppler effect calculations for satellite signals.
"""

import numpy as np


def calculate_doppler_shift(relative_velocity, signal_frequency, speed_of_light=3e8):
    """
    Calculate Doppler frequency shift for a satellite signal.
    
    Parameters
    ----------
    relative_velocity : float
        Radial velocity (positive = approaching) [m/s]
    signal_frequency : float
        Transmitted signal frequency [Hz]
    speed_of_light : float, optional
        Speed of light [m/s] (default: 3e8)
        
    Returns
    -------
    float
        Doppler-shifted frequency [Hz]
    """
    # Non-relativistic approximation
    doppler_factor = 1 + relative_velocity / speed_of_light
    shifted_frequency = signal_frequency * doppler_factor
    
    return shifted_frequency


def calculate_doppler_shift_relativistic(relative_velocity, signal_frequency, speed_of_light=3e8):
    """
    Calculate Doppler frequency shift using relativistic formula.
    
    Parameters
    ----------
    relative_velocity : float
        Radial velocity (positive = approaching) [m/s]
    signal_frequency : float
        Transmitted signal frequency [Hz]
    speed_of_light : float, optional
        Speed of light [m/s] (default: 3e8)
        
    Returns
    -------
    float
        Doppler-shifted frequency [Hz]
    """
    beta = relative_velocity / speed_of_light
    gamma = 1 / np.sqrt(1 - beta**2)
    
    doppler_factor = gamma * (1 + beta)
    shifted_frequency = signal_frequency / doppler_factor
    
    return shifted_frequency


def calculate_radial_velocity(position, velocity):
    """
    Calculate radial velocity from position and velocity vectors.
    
    Parameters
    ----------
    position : np.ndarray
        Position vector [m]
    velocity : np.ndarray
        Velocity vector [m/s]
        
    Returns
    -------
    float
        Radial velocity [m/s]
    """
    r_magnitude = np.linalg.norm(position)
    if r_magnitude == 0:
        return 0.0
    
    radial_velocity = np.dot(position, velocity) / r_magnitude
    
    return radial_velocity


def calculate_doppler_rate(position, velocity, acceleration, signal_frequency):
    """
    Calculate rate of change of Doppler shift.
    
    Parameters
    ----------
    position : np.ndarray
        Position vector [m]
    velocity : np.ndarray
        Velocity vector [m/s]
    acceleration : np.ndarray
        Acceleration vector [m/s^2]
    signal_frequency : float
        Transmitted signal frequency [Hz]
        
    Returns
    -------
    float
        Rate of Doppler shift [Hz/s]
    """
    r = np.linalg.norm(position)
    v_r = np.dot(position, velocity) / r
    
    # Derivative of radial velocity
    dv_r_dt = (np.dot(velocity, velocity) + np.dot(position, acceleration) - (v_r**2 / r)) / r
    
    doppler_rate = signal_frequency * dv_r_dt / 3e8
    
    return doppler_rate
