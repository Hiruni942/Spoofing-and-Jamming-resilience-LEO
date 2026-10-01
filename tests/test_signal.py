"""
Tests for signal processing module.
"""

import numpy as np
import pytest
from gnss_leo.signal.doppler import calculate_doppler_shift, calculate_radial_velocity
from gnss_leo.signal.ranging import calculate_distance, calculate_pseudorange
from gnss_leo.signal.propagation import path_loss, ionospheric_delay


class TestDopplerShift:
    """Test Doppler shift calculations."""
    
    def test_approaching_satellite(self):
        """Frequency should increase for approaching satellite."""
        v_r = 1000  # 1 km/s approaching
        f0 = 1.5e9  # 1.5 GHz
        f = calculate_doppler_shift(v_r, f0)
        assert f > f0
    
    def test_receding_satellite(self):
        """Frequency should decrease for receding satellite."""
        v_r = -1000  # 1 km/s receding
        f0 = 1.5e9
        f = calculate_doppler_shift(v_r, f0)
        assert f < f0
    
    def test_zero_velocity(self):
        """No Doppler shift for zero velocity."""
        v_r = 0
        f0 = 1.5e9
        f = calculate_doppler_shift(v_r, f0)
        assert np.isclose(f, f0)


class TestRadialVelocity:
    """Test radial velocity calculations."""
    
    def test_radial_velocity_sign(self):
        """Radial velocity should be positive for approaching."""
        position = np.array([6.4e6, 0, 0])  # Along x-axis
        velocity = np.array([-1000, 0, 0])  # Toward origin (approaching)
        v_r = calculate_radial_velocity(position, velocity)
        assert v_r < 0  # Negative means approaching in our convention
    
    def test_orthogonal_velocity(self):
        """Radial velocity should be zero for orthogonal velocity."""
        position = np.array([6.4e6, 0, 0])
        velocity = np.array([0, 1000, 0])  # Orthogonal
        v_r = calculate_radial_velocity(position, velocity)
        assert np.isclose(v_r, 0, atol=1e-6)


class TestRanging:
    """Test ranging calculations."""
    
    def test_distance_calculation(self):
        """Test Euclidean distance."""
        receiver = np.array([0, 0, 0])
        satellite = np.array([3, 4, 0])
        dist = calculate_distance(receiver, satellite)
        assert np.isclose(dist, 5.0)
    
    def test_pseudorange_with_bias(self):
        """Pseudorange should include clock bias."""
        receiver = np.array([0, 0, 0])
        satellite = np.array([1e7, 0, 0])
        clock_bias = 1000  # 1 km
        
        pr = calculate_pseudorange(receiver, satellite, clock_bias=clock_bias)
        pr_no_bias = calculate_pseudorange(receiver, satellite, clock_bias=0)
        
        assert np.isclose(pr - pr_no_bias, clock_bias)


class TestSignalPropagation:
    """Test signal propagation models."""
    
    def test_path_loss_increases_with_distance(self):
        """Path loss should increase with distance."""
        f = 1.5e9  # 1.5 GHz
        
        loss_1 = path_loss(1e4, f)  # 10 km
        loss_2 = path_loss(1e5, f)  # 100 km
        
        assert loss_2 > loss_1
    
    def test_ionospheric_delay_frequency_dependent(self):
        """Ionospheric delay should decrease with higher frequencies."""
        tec = 50e16  # 50 TECU
        
        delay_1 = ionospheric_delay(1e9, tec)   # 1 GHz
        delay_2 = ionospheric_delay(1.5e9, tec)  # 1.5 GHz
        
        assert delay_1 > delay_2
