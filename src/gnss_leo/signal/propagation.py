"""
Signal propagation models for GNSS/LEO systems.
"""

import numpy as np


def ionospheric_delay(frequency, electron_density_content, speed_of_light=3e8):
    """
    Calculate ionospheric delay using simple model.
    
    Parameters
    ----------
    frequency : float
        Signal frequency [Hz]
    electron_density_content : float
        Total electron content (TEC) [electrons/m^2]
    speed_of_light : float, optional
        Speed of light [m/s] (default: 3e8)
        
    Returns
    -------
    float
        Ionospheric delay [m]
    """
    # Ionospheric delay is frequency-dependent
    # Formula: delay = K / f^2 where K depends on TEC
    K = 40.3e16 * electron_density_content
    delay = K / (frequency**2)
    
    return delay


def tropospheric_delay(elevation_angle, temperature=288.15, pressure=101325, humidity=0.5):
    """
    Calculate tropospheric delay using simplified model.
    
    Uses the Saastaminen model approximation.
    
    Parameters
    ----------
    elevation_angle : float
        Satellite elevation angle [radians]
    temperature : float, optional
        Temperature [K] (default: 288.15 K = 15°C)
    pressure : float, optional
        Atmospheric pressure [Pa] (default: 101325 Pa)
    humidity : float, optional
        Relative humidity (0-1) (default: 0.5)
        
    Returns
    -------
    float
        Tropospheric delay [m]
    """
    # Simplified tropospheric delay
    # Full model would use hydrostatic + wet components
    
    el = elevation_angle
    
    # Approximate formula (zenith delay)
    T_z = (0.2277 * pressure + 4.3e-3 * humidity * pressure) / (273.15 + temperature - 0.0065 * 1000)
    
    # Mapping function (simple)
    mf = 1.0 / np.sin(el + 0.0031 / (np.tan(el) + 0.002))
    
    delay = T_z * mf
    
    return delay


def path_loss(distance, frequency, include_atmospheric=False, atmospheric_attenuation=0.0):
    """
    Calculate path loss in dB.
    
    Free-space path loss: L = 20*log10(distance) + 20*log10(frequency) + K
    
    Parameters
    ----------
    distance : float
        Distance between transmitter and receiver [m]
    frequency : float
        Signal frequency [Hz]
    include_atmospheric : bool, optional
        Include atmospheric attenuation (default: False)
    atmospheric_attenuation : float, optional
        Atmospheric attenuation coefficient [dB/m] (default: 0)
        
    Returns
    -------
    float
        Path loss [dB]
    """
    # Speed of light
    c = 3e8
    
    # Free-space path loss
    wavelength = c / frequency
    loss = 20 * np.log10(4 * np.pi * distance / wavelength)
    
    # Add atmospheric attenuation if requested
    if include_atmospheric:
        loss += atmospheric_attenuation * distance
    
    return loss


def signal_to_noise_ratio(transmitted_power, path_loss_db, noise_figure_db=0, bandwidth=1e6):
    """
    Calculate signal-to-noise ratio (SNR).
    
    Parameters
    ----------
    transmitted_power : float
        Transmitted power [W]
    path_loss_db : float
        Path loss [dB]
    noise_figure_db : float, optional
        Receiver noise figure [dB] (default: 0)
    bandwidth : float, optional
        Signal bandwidth [Hz] (default: 1 MHz)
        
    Returns
    -------
    float
        SNR [dB]
    """
    # Boltzmann constant
    k_b = 1.380649e-23  # J/K
    
    # Reference temperature
    T_0 = 290  # K
    
    # Noise power
    noise_power = k_b * T_0 * bandwidth * 10**(noise_figure_db / 10)
    
    # Received power
    received_power = transmitted_power * 10**(-path_loss_db / 10)
    
    # SNR
    snr_linear = received_power / noise_power
    snr_db = 10 * np.log10(snr_linear)
    
    return snr_db


def calculate_c_n0(snr_db, bandwidth):
    """
    Calculate Carrier-to-Noise density (C/N0) from SNR.
    
    Parameters
    ----------
    snr_db : float
        Signal-to-noise ratio [dB]
    bandwidth : float
        Bandwidth [Hz]
        
    Returns
    -------
    float
        Carrier-to-noise density [dB-Hz]
    """
    c_n0 = snr_db + 10 * np.log10(bandwidth)
    
    return c_n0
