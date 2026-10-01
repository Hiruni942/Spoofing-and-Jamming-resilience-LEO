"""
Satellite constellation utilities for LEO and GPS systems.
"""

import numpy as np
from .constants import (
    R_EARTH, LEO_ALTITUDE, MEO_ALTITUDE, 
    LEO_PLANES, LEO_SATS_PER_PLANE, GPS_PLANES, GPS_SATS_PER_PLANE,
    LEO_i, GPS_i
)
from .orbit import propagate_orbit


def create_leo_constellation(num_planes=LEO_PLANES, satellites_per_plane=LEO_SATS_PER_PLANE):
    """
    Create a LEO satellite constellation.
    
    Parameters
    ----------
    num_planes : int, optional
        Number of orbital planes (default: 2)
    satellites_per_plane : int, optional
        Satellites per plane (default: 3)
        
    Returns
    -------
    list
        List of satellite dictionaries with orbital elements
    """
    constellation = []
    
    for plane in range(num_planes):
        raan = np.deg2rad(plane * 360 / num_planes)
        
        for sat in range(satellites_per_plane):
            true_anomaly = np.deg2rad(sat * 360 / satellites_per_plane)
            
            satellite = {
                "name": f"LEO-{len(constellation)+1:02d}",
                "plane": plane,
                "a": R_EARTH + LEO_ALTITUDE,
                "e": 0.01,
                "inclination": LEO_i,
                "raan": raan,
                "arg_periapsis": 0.0,
                "true_anomaly_0": true_anomaly
            }
            
            constellation.append(satellite)
    
    return constellation


def create_gps_constellation(num_planes=GPS_PLANES, satellites_per_plane=GPS_SATS_PER_PLANE):
    """
    Create a GPS satellite constellation.
    
    Parameters
    ----------
    num_planes : int, optional
        Number of orbital planes (default: 6)
    satellites_per_plane : int, optional
        Satellites per plane (default: 4)
        
    Returns
    -------
    list
        List of satellite dictionaries with orbital elements
    """
    constellation = []
    
    for plane in range(num_planes):
        raan = np.deg2rad(plane * 360 / num_planes)
        
        for sat in range(satellites_per_plane):
            true_anomaly = np.deg2rad(sat * 360 / satellites_per_plane)
            
            satellite = {
                "name": f"GPS-{len(constellation)+1:02d}",
                "plane": plane,
                "a": R_EARTH + MEO_ALTITUDE,
                "e": 0.01,
                "inclination": GPS_i,
                "raan": raan,
                "arg_periapsis": 0.0,
                "true_anomaly_0": true_anomaly
            }
            
            constellation.append(satellite)
    
    return constellation


def propagate_constellation(constellation, times):
    """
    Propagate all satellites in a constellation.
    
    Parameters
    ----------
    constellation : list
        List of satellite dictionaries
    times : np.ndarray
        Time array [seconds]
        
    Returns
    -------
    tuple
        (constellation_positions, constellation_velocities) - Dicts with satellite names as keys
    """
    constellation_positions = {}
    constellation_velocities = {}
    
    for satellite in constellation:
        positions, velocities = propagate_orbit(
            satellite["a"],
            satellite["e"],
            satellite["inclination"],
            satellite["raan"],
            satellite["arg_periapsis"],
            satellite["true_anomaly_0"],
            times
        )
        
        name = satellite["name"]
        constellation_positions[name] = positions
        constellation_velocities[name] = velocities
    
    return constellation_positions, constellation_velocities
