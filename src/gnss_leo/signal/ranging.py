"""
Ranging calculations and pseudorange models.
"""

import numpy as np


def calculate_distance(receiver_pos, satellite_pos):
    """
    Calculate Euclidean distance between receiver and satellite.
    
    Parameters
    ----------
    receiver_pos : np.ndarray
        Receiver position [x, y, z] [m]
    satellite_pos : np.ndarray
        Satellite position [x, y, z] [m]
        
    Returns
    -------
    float
        Geometric distance [m]
    """
    diff = satellite_pos - receiver_pos
    distance = np.linalg.norm(diff)
    
    return distance


def calculate_pseudorange(receiver_pos, satellite_pos, clock_bias=0, atmospheric_delay=0):
    """
    Calculate pseudorange from receiver to satellite.
    
    Pseudorange = geometric range + c*clock_bias + atmospheric delays
    
    Parameters
    ----------
    receiver_pos : np.ndarray
        Receiver position [x, y, z] [m]
    satellite_pos : np.ndarray
        Satellite position [x, y, z] [m]
    clock_bias : float, optional
        Receiver clock bias [m] (default: 0)
    atmospheric_delay : float, optional
        Ionospheric + tropospheric delay [m] (default: 0)
        
    Returns
    -------
    float
        Pseudorange [m]
    """
    geometric_range = calculate_distance(receiver_pos, satellite_pos)
    pseudorange = geometric_range + clock_bias + atmospheric_delay
    
    return pseudorange


def calculate_pseudorange_rate(receiver_pos, receiver_vel, satellite_pos, satellite_vel, clock_rate=0):
    """
    Calculate rate of change of pseudorange (pseudorange rate).
    
    Parameters
    ----------
    receiver_pos : np.ndarray
        Receiver position [m]
    receiver_vel : np.ndarray
        Receiver velocity [m/s]
    satellite_pos : np.ndarray
        Satellite position [m]
    satellite_vel : np.ndarray
        Satellite velocity [m/s]
    clock_rate : float, optional
        Receiver clock rate [m/s] (default: 0)
        
    Returns
    -------
    float
        Pseudorange rate [m/s]
    """
    relative_pos = satellite_pos - receiver_pos
    relative_vel = satellite_vel - receiver_vel
    
    distance = np.linalg.norm(relative_pos)
    if distance == 0:
        return 0.0
    
    # Range rate
    range_rate = np.dot(relative_pos, relative_vel) / distance
    
    # Pseudorange rate includes clock drift
    pseudorange_rate = range_rate + clock_rate
    
    return pseudorange_rate


def calculate_elevation_angle(receiver_pos, satellite_pos):
    """
    Calculate elevation angle from receiver to satellite.
    
    Parameters
    ----------
    receiver_pos : np.ndarray
        Receiver position in ECEF [m]
    satellite_pos : np.ndarray
        Satellite position in ECEF [m]
        
    Returns
    -------
    float
        Elevation angle [radians] (0 = horizon, π/2 = zenith)
    """
    # This assumes receiver is on Earth surface (simplified)
    # For accurate calculation, need local horizon plane
    
    relative_pos = satellite_pos - receiver_pos
    distance = np.linalg.norm(relative_pos)
    
    # Nadir angle from receiver
    nadir_angle = np.arccos(np.dot(relative_pos, -receiver_pos) / (distance * np.linalg.norm(receiver_pos)))
    
    # Elevation angle
    elevation = np.pi / 2 - nadir_angle
    
    return elevation


def is_visible(receiver_pos, satellite_pos, min_elevation=np.deg2rad(10)):
    """
    Check if satellite is visible from receiver.
    
    Parameters
    ----------
    receiver_pos : np.ndarray
        Receiver position in ECEF [m]
    satellite_pos : np.ndarray
        Satellite position in ECEF [m]
    min_elevation : float, optional
        Minimum elevation angle [radians] (default: 10 degrees)
        
    Returns
    -------
    bool
        True if satellite is visible, False otherwise
    """
    elevation = calculate_elevation_angle(receiver_pos, satellite_pos)
    return elevation >= min_elevation
