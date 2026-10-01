"""
Coordinate system transformations (ECI, ECEF, geodetic).
"""

import numpy as np
from .constants import R_EARTH


def ecef_to_geodetic(ecef_pos, tolerance=1e-12, max_iterations=100):
    """
    Convert ECEF coordinates to geodetic (latitude, longitude, altitude).
    
    Uses iterative method based on Heikkinen's algorithm.
    
    Parameters
    ----------
    ecef_pos : np.ndarray
        Position in ECEF frame [x, y, z] in meters
    tolerance : float, optional
        Convergence tolerance (default: 1e-12)
    max_iterations : int, optional
        Maximum iterations (default: 100)
        
    Returns
    -------
    tuple
        (latitude, longitude, altitude) in radians and meters
    """
    # WGS84 parameters
    a = 6378137.0  # Semi-major axis
    b = 6356752.314245  # Semi-minor axis
    e2 = 1 - (b**2 / a**2)  # First eccentricity squared
    
    x, y, z = ecef_pos
    
    # Initial latitude guess
    lat = np.arctan2(z, np.sqrt(x**2 + y**2))
    
    for _ in range(max_iterations):
        N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
        lat_new = np.arctan2(z + e2 * N * np.sin(lat), np.sqrt(x**2 + y**2))
        
        if abs(lat_new - lat) < tolerance:
            lat = lat_new
            break
        lat = lat_new
    
    lon = np.arctan2(y, x)
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    alt = np.sqrt(x**2 + y**2) / np.cos(lat) - N
    
    return lat, lon, alt


def geodetic_to_ecef(lat, lon, alt):
    """
    Convert geodetic coordinates to ECEF.
    
    Parameters
    ----------
    lat : float
        Latitude [radians]
    lon : float
        Longitude [radians]
    alt : float
        Altitude [meters]
        
    Returns
    -------
    np.ndarray
        Position in ECEF frame [x, y, z] in meters
    """
    a = 6378137.0  # Semi-major axis
    e2 = 0.00669437999014  # First eccentricity squared
    
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    
    x = (N + alt) * np.cos(lat) * np.cos(lon)
    y = (N + alt) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + alt) * np.sin(lat)
    
    return np.array([x, y, z])


def eci_to_ecef(eci_pos, gst):
    """
    Convert ECI coordinates to ECEF using Greenwich Sidereal Time.
    
    Parameters
    ----------
    eci_pos : np.ndarray
        Position in ECI frame [m]
    gst : float
        Greenwich Sidereal Time [radians]
        
    Returns
    -------
    np.ndarray
        Position in ECEF frame [m]
    """
    c = np.cos(gst)
    s = np.sin(gst)
    
    rotation_matrix = np.array([
        [c, s, 0],
        [-s, c, 0],
        [0, 0, 1]
    ])
    
    return rotation_matrix @ eci_pos


def ecef_to_eci(ecef_pos, gst):
    """
    Convert ECEF coordinates to ECI using Greenwich Sidereal Time.
    
    Parameters
    ----------
    ecef_pos : np.ndarray
        Position in ECEF frame [m]
    gst : float
        Greenwich Sidereal Time [radians]
        
    Returns
    -------
    np.ndarray
        Position in ECI frame [m]
    """
    c = np.cos(gst)
    s = np.sin(gst)
    
    rotation_matrix = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
    
    return rotation_matrix @ ecef_pos
