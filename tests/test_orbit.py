"""
Tests for orbital mechanics module.
"""

import numpy as np
import pytest
from gnss_leo.core.orbit import (
    solve_keplers_equation, eccentric_to_true_anomaly,
    orbital_elements_to_state, propagate_orbit
)
from gnss_leo.core.constants import MU_EARTH


class TestKeplersEquation:
    """Test Kepler's equation solver."""
    
    def test_zero_eccentricity(self):
        """For zero eccentricity, M = E."""
        M = 1.0
        e = 0.0
        E = solve_keplers_equation(M, e)
        assert np.isclose(E, M, atol=1e-10)
    
    def test_small_eccentricity(self):
        """Test with small eccentricity."""
        M = 0.5
        e = 0.01
        E = solve_keplers_equation(M, e)
        # Verify solution: M = E - e*sin(E)
        M_check = E - e * np.sin(E)
        assert np.isclose(M_check, M, atol=1e-10)


class TestOrbitalElements:
    """Test orbital element conversions."""
    
    def test_state_vector_magnitude(self, leo_orbital_elements):
        """Position magnitude should be semi-latus rectum / (1 + e*cos(nu)) = a(1-e^2)/(1+e*cos(nu))."""
        orb = leo_orbital_elements
        position, velocity = orbital_elements_to_state(
            orb["a"], orb["e"], orb["inclination"],
            orb["raan"], orb["arg_periapsis"], orb["true_anomaly_0"]
        )
        
        # Distance from Earth center
        r = np.linalg.norm(position)
        
        # Expected value
        p = orb["a"] * (1 - orb["e"]**2)
        r_expected = p / (1 + orb["e"] * np.cos(orb["true_anomaly_0"]))
        
        assert np.isclose(r, r_expected, rtol=1e-10)


class TestOrbitPropagation:
    """Test orbit propagation."""
    
    def test_propagation_returns_correct_shape(self, leo_orbital_elements, simulation_times):
        """Test that propagation returns correct array shapes."""
        orb = leo_orbital_elements
        positions, velocities = propagate_orbit(
            orb["a"], orb["e"], orb["inclination"],
            orb["raan"], orb["arg_periapsis"], orb["true_anomaly_0"],
            simulation_times
        )
        
        assert positions.shape == (len(simulation_times), 3)
        assert velocities.shape == (len(simulation_times), 3)
    
    def test_altitude_near_constant(self, leo_orbital_elements):
        """Test that altitude remains nearly constant for circular orbit."""
        orb = leo_orbital_elements
        orb["e"] = 0.0  # Make it circular
        
        simulation_time = 24 * 3600
        num_steps = 100
        times = np.linspace(0, simulation_time, num_steps)
        
        positions, velocities = propagate_orbit(
            orb["a"], orb["e"], orb["inclination"],
            orb["raan"], orb["arg_periapsis"], orb["true_anomaly_0"],
            times
        )
        
        # Calculate altitudes
        from gnss_leo.core.constants import R_EARTH
        altitudes = np.linalg.norm(positions, axis=1) - R_EARTH
        
        # For circular orbit, altitude should be constant
        assert np.std(altitudes) < 1e3  # Less than 1 km variation
