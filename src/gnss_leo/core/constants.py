"""
Physical constants and orbital parameters for GNSS and LEO systems.
"""

import numpy as np

# Earth Parameters
R_EARTH = 6_378_137.0  # Earth radius [m] (WGS-84 equatorial radius)
MU_EARTH = 3.986004418e14  # Earth's gravitational parameter [m^3/s^2]

# Satellite Altitudes
LEO_ALTITUDE = 600e3  # 600 km
MEO_ALTITUDE = 20_200e3  # 20,200 km (GPS)

# MEO (GPS) Orbital Elements
MEO_a = R_EARTH + MEO_ALTITUDE
MEO_e = 0.01
MEO_i = np.deg2rad(55)
MEO_raan = np.deg2rad(120)
MEO_arg_periapsis = np.deg2rad(45)
MEO_true_anomaly_0 = np.deg2rad(180)

# LEO Orbital Elements
LEO_a = R_EARTH + LEO_ALTITUDE
LEO_e = 0.01
LEO_i = np.deg2rad(53)
LEO_raan = np.deg2rad(40)
LEO_arg_periapsis = np.deg2rad(30)
LEO_true_anomaly_0 = np.deg2rad(0)

# GPS Orbital Elements
GPS_i = np.deg2rad(55)

# Constellation Configuration
LEO_PLANES = 2
LEO_SATS_PER_PLANE = 3
GPS_PLANES = 6
GPS_SATS_PER_PLANE = 4

# Simulation Parameters (default)
SIMULATION_TIME = 24 * 3600  # 24 hours in seconds
DEFAULT_NUM_STEPS = 3000
