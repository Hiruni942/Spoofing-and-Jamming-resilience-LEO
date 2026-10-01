"""
Pytest configuration and fixtures.
"""

import pytest
import numpy as np


@pytest.fixture
def leo_orbital_elements():
    """Fixture for LEO orbital elements."""
    return {
        "a": 6378137.0 + 600e3,  # 600 km altitude
        "e": 0.01,
        "inclination": np.deg2rad(53),
        "raan": np.deg2rad(40),
        "arg_periapsis": np.deg2rad(30),
        "true_anomaly_0": np.deg2rad(0)
    }


@pytest.fixture
def gps_orbital_elements():
    """Fixture for GPS orbital elements."""
    return {
        "a": 6378137.0 + 20_200e3,  # 20,200 km altitude
        "e": 0.01,
        "inclination": np.deg2rad(55),
        "raan": np.deg2rad(120),
        "arg_periapsis": np.deg2rad(45),
        "true_anomaly_0": np.deg2rad(180)
    }


@pytest.fixture
def simulation_times():
    """Fixture for simulation time array."""
    simulation_time = 24 * 3600  # 24 hours
    num_steps = 100
    return np.linspace(0, simulation_time, num_steps)


@pytest.fixture
def receiver_position():
    """Fixture for receiver position (on Earth surface)."""
    # Example: latitude=0°, longitude=0° (Equator, Prime Meridian)
    lat = np.deg2rad(0)
    lon = np.deg2rad(0)
    alt = 0  # sea level
    
    # Convert to ECEF
    a = 6378137.0
    e2 = 0.00669437999014
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    x = (N + alt) * np.cos(lat) * np.cos(lon)
    y = (N + alt) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + alt) * np.sin(lat)
    
    return np.array([x, y, z])
