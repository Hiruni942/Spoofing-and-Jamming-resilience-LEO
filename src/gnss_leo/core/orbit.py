"""
Orbital mechanics: Kepler's equation solver and orbital propagation.
"""

import numpy as np
from .constants import MU_EARTH
from .rotations import rotation_1, rotation_3


def solve_keplers_equation(M, e, tolerance=1e-12, max_iterations=100):
    """
    Solve Kepler's equation: M = E - e*sin(E) for eccentric anomaly E.
    
    Uses Newton-Raphson iteration.
    
    Parameters
    ----------
    M : float or np.ndarray
        Mean anomaly [rad]
    e : float
        Eccentricity
    tolerance : float, optional
        Convergence tolerance (default: 1e-12)
    max_iterations : int, optional
        Maximum iterations (default: 100)
        
    Returns
    -------
    float or np.ndarray
        Eccentric anomaly [rad]
    """
    # Initial guess
    E = M if e < 0.8 else np.pi
    
    for _ in range(max_iterations):
        f = E - e * np.sin(E) - M
        f_prime = 1 - e * np.cos(E)
        
        delta_E = f / f_prime
        E -= delta_E
        
        if np.all(np.abs(delta_E) < tolerance):
            break
    
    return E


def eccentric_to_true_anomaly(E, e):
    """
    Convert eccentric anomaly to true anomaly.
    
    Parameters
    ----------
    E : float or np.ndarray
        Eccentric anomaly [rad]
    e : float
        Eccentricity
        
    Returns
    -------
    float or np.ndarray
        True anomaly [rad]
    """
    numerator = np.sqrt(1 + e) * np.sin(E / 2)
    denominator = np.sqrt(1 - e) * np.cos(E / 2)
    
    nu = 2 * np.arctan2(numerator, denominator)
    
    return nu


def orbital_elements_to_state(a, e, inclination, raan, arg_periapsis, true_anomaly):
    """
    Convert orbital elements to ECI position and velocity vectors.
    
    Parameters
    ----------
    a : float
        Semi-major axis [m]
    e : float
        Eccentricity
    inclination : float
        Orbital inclination [rad]
    raan : float
        Right ascension of ascending node [rad]
    arg_periapsis : float
        Argument of periapsis [rad]
    true_anomaly : float
        True anomaly [rad]
        
    Returns
    -------
    tuple
        (position_eci, velocity_eci) - Position and velocity vectors in ECI [m, m/s]
    """
    # Calculate orbital radius
    r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
    
    # Position in perifocal (PQW) frame
    position_pqw = np.array([
        r * np.cos(true_anomaly),
        r * np.sin(true_anomaly),
        0.0
    ])
    
    # Velocity in PQW frame
    velocity_factor = np.sqrt(MU_EARTH / (a * (1 - e**2)))
    velocity_pqw = velocity_factor * np.array([
        -np.sin(true_anomaly),
        e + np.cos(true_anomaly),
        0.0
    ])
    
    # Rotate PQW → ECI
    transformation = rotation_3(raan) @ rotation_1(inclination) @ rotation_3(arg_periapsis)
    
    position_eci = transformation @ position_pqw
    velocity_eci = transformation @ velocity_pqw
    
    return position_eci, velocity_eci


def propagate_orbit(a, e, inclination, raan, arg_periapsis, true_anomaly_0, times):
    """
    Propagate orbital state over time using Kepler's equations.
    
    Parameters
    ----------
    a : float
        Semi-major axis [m]
    e : float
        Eccentricity
    inclination : float
        Orbital inclination [rad]
    raan : float
        Right ascension of ascending node [rad]
    arg_periapsis : float
        Argument of periapsis [rad]
    true_anomaly_0 : float
        Initial true anomaly [rad]
    times : np.ndarray
        Time array [seconds]
        
    Returns
    -------
    tuple
        (positions, velocities) - Arrays of shape (N, 3) in ECI frame [m, m/s]
    """
    # Convert initial true anomaly to eccentric anomaly
    E0 = 2 * np.arctan2(
        np.sqrt(1 - e) * np.sin(true_anomaly_0 / 2),
        np.sqrt(1 + e) * np.cos(true_anomaly_0 / 2)
    )
    
    # Calculate initial mean anomaly
    M0 = E0 - e * np.sin(E0)
    
    # Calculate mean motion
    n = np.sqrt(MU_EARTH / a**3)
    
    positions = []
    velocities = []
    
    for t in times:
        # Mean anomaly at time t
        M = M0 + n * t
        
        # Normalize to [0, 2π)
        M = M % (2 * np.pi)
        
        # Solve Kepler's equation
        E = solve_keplers_equation(M, e)
        
        # Convert to true anomaly
        nu = eccentric_to_true_anomaly(E, e)
        
        # Convert orbital elements to ECI state
        position, velocity = orbital_elements_to_state(
            a, e, inclination, raan, arg_periapsis, nu
        )
        
        positions.append(position)
        velocities.append(velocity)
    
    return np.array(positions), np.array(velocities)
