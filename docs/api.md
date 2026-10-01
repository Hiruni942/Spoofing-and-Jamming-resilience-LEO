# API Reference

## Core Module

### Orbital Mechanics

#### `solve_keplers_equation(M, e, tolerance=1e-12, max_iterations=100)`
Solve Kepler's equation for eccentric anomaly using Newton-Raphson iteration.

**Parameters:**
- `M` (float): Mean anomaly [rad]
- `e` (float): Eccentricity
- `tolerance` (float): Convergence tolerance
- `max_iterations` (int): Maximum iterations

**Returns:** Eccentric anomaly [rad]

---

#### `propagate_orbit(a, e, inclination, raan, arg_periapsis, true_anomaly_0, times)`
Propagate satellite orbit over time using Kepler's equations.

**Parameters:**
- `a` (float): Semi-major axis [m]
- `e` (float): Eccentricity
- `inclination` (float): Inclination [rad]
- `raan` (float): Right ascension of ascending node [rad]
- `arg_periapsis` (float): Argument of periapsis [rad]
- `true_anomaly_0` (float): Initial true anomaly [rad]
- `times` (np.ndarray): Time array [seconds]

**Returns:** Tuple of (positions, velocities) arrays, shape (N, 3)

---

#### `create_leo_constellation(num_planes=2, satellites_per_plane=3)`
Create a LEO satellite constellation.

**Returns:** List of satellite dictionaries with orbital elements

---

#### `create_gps_constellation(num_planes=6, satellites_per_plane=4)`
Create a GPS satellite constellation.

**Returns:** List of satellite dictionaries with orbital elements

---

### Coordinate Transformations

#### `ecef_to_geodetic(ecef_pos, tolerance=1e-12, max_iterations=100)`
Convert ECEF to geodetic coordinates (WGS-84).

**Returns:** Tuple (latitude [rad], longitude [rad], altitude [m])

---

#### `geodetic_to_ecef(lat, lon, alt)`
Convert geodetic to ECEF coordinates (WGS-84).

**Returns:** ECEF position array [m]

---

## Signal Module

### Doppler Effect

#### `calculate_doppler_shift(relative_velocity, signal_frequency, speed_of_light=3e8)`
Calculate Doppler-shifted frequency.

**Parameters:**
- `relative_velocity` (float): Radial velocity [m/s] (positive = approaching)
- `signal_frequency` (float): Transmitted frequency [Hz]

**Returns:** Doppler-shifted frequency [Hz]

---

#### `calculate_radial_velocity(position, velocity)`
Calculate radial velocity from position and velocity vectors.

**Returns:** Radial velocity [m/s]

---

### Ranging

#### `calculate_distance(receiver_pos, satellite_pos)`
Calculate Euclidean distance.

**Returns:** Distance [m]

---

#### `calculate_pseudorange(receiver_pos, satellite_pos, clock_bias=0, atmospheric_delay=0)`
Calculate pseudorange including clock bias and atmospheric delays.

**Returns:** Pseudorange [m]

---

#### `calculate_elevation_angle(receiver_pos, satellite_pos)`
Calculate elevation angle from receiver to satellite.

**Returns:** Elevation angle [rad] (0 = horizon, π/2 = zenith)

---

#### `is_visible(receiver_pos, satellite_pos, min_elevation=np.deg2rad(10))`
Check if satellite is visible from receiver.

**Returns:** Boolean

---

### Signal Propagation

#### `path_loss(distance, frequency, include_atmospheric=False)`
Calculate free-space path loss in dB.

**Returns:** Path loss [dB]

---

#### `ionospheric_delay(frequency, electron_density_content)`
Calculate ionospheric delay.

**Parameters:**
- `electron_density_content` (float): Total electron content (TEC) [electrons/m²]

**Returns:** Delay [m]

---

#### `tropospheric_delay(elevation_angle, temperature=288.15, pressure=101325, humidity=0.5)`
Calculate tropospheric delay (hydrostatic).

**Returns:** Delay [m]

---

#### `signal_to_noise_ratio(transmitted_power, path_loss_db, noise_figure_db=0, bandwidth=1e6)`
Calculate SNR.

**Returns:** SNR [dB]

---

## Utilities

### Plotting

#### `plot_constellation_positions(positions_dict, times, title="Satellite Constellation Positions")`
Plot 3D trajectories of satellites.

**Parameters:**
- `positions_dict` (dict): Satellite positions with names as keys
- `times` (np.ndarray): Time array [seconds]

**Returns:** (fig, ax) matplotlib objects

---

#### `plot_altitude_profile(positions, times, satellite_name="Satellite")`
Plot altitude vs time.

**Returns:** (fig, ax) matplotlib objects

---
