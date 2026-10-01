"""
GNSS LEO resilience library - Utilities.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_constellation_positions(positions_dict, times, title="Satellite Constellation Positions"):
    """
    Plot 3D trajectory of satellites.
    
    Parameters
    ----------
    positions_dict : dict
        Dictionary with satellite names as keys and position arrays as values
    times : np.ndarray
        Time array [seconds]
    title : str
        Plot title
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(positions_dict)))
    
    for (name, positions), color in zip(positions_dict.items(), colors):
        ax.plot(positions[:, 0] / 1e6, positions[:, 1] / 1e6, positions[:, 2] / 1e6,
                label=name, alpha=0.7, linewidth=1, color=color)
    
    ax.set_xlabel('X [Mm]')
    ax.set_ylabel('Y [Mm]')
    ax.set_zlabel('Z [Mm]')
    ax.set_title(title)
    ax.legend(fontsize=8, ncol=2)
    
    return fig, ax


def plot_altitude_profile(positions, times, satellite_name="Satellite"):
    """
    Plot altitude vs time for a satellite.
    
    Parameters
    ----------
    positions : np.ndarray
        Position array shape (N, 3) [m]
    times : np.ndarray
        Time array [seconds]
    satellite_name : str
        Satellite name for title
    """
    # Calculate altitude (distance from Earth center - Earth radius)
    from .constants import R_EARTH
    
    altitudes = np.linalg.norm(positions, axis=1) - R_EARTH
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(times / 3600, altitudes / 1e3, linewidth=2)
    ax.set_xlabel('Time [hours]')
    ax.set_ylabel('Altitude [km]')
    ax.set_title(f'{satellite_name} Altitude Profile')
    ax.grid(True, alpha=0.3)
    
    return fig, ax


__all__ = [
    'plot_constellation_positions',
    'plot_altitude_profile'
]
