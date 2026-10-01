

import numpy as np
import matplotlib.pyplot as plt

#Defining earth
# Earth parameters

R_EARTH = 6_378_137.0       # Earth radius [m](We're using the WGS-84 equatorial radius for now.)
MU_EARTH = 3.986004418e14   # Earth's gravitational parameter [m^3/s^2]

# Satellite altitudes

LEO_ALTITUDE = 600e3       # 600 km
MEO_ALTITUDE = 20_200e3    # 20,200 km

LEO_PHASE = 0.0
MEO_PHASE = np.deg2rad(90)

MEO_a = R_EARTH + 20_200e3
MEO_e = 0.01
MEO_i = np.deg2rad(55)
MEO_raan = np.deg2rad(120)
MEO_arg_periapsis = np.deg2rad(45)
MEO_true_anomaly_0 = np.deg2rad(180)

LEO_a = R_EARTH + 600e3
LEO_e = 0.01

LEO_i = np.deg2rad(53)

LEO_raan = np.deg2rad(40)

LEO_arg_periapsis = np.deg2rad(30)

LEO_true_anomaly_0 = np.deg2rad(0)

gps_satellite = {
    "name": "GPS-01",
    "a": MEO_a,
    "e": MEO_e,
    "inclination": MEO_i,
    "raan": MEO_raan,
    "arg_periapsis": MEO_arg_periapsis,
    "true_anomaly_0": MEO_true_anomaly_0
}

leo_satellite = {
    "name": "LEO-01",
    "a": LEO_a,
    "e": LEO_e,
    "inclination": LEO_i,
    "raan": LEO_raan,
    "arg_periapsis": LEO_arg_periapsis,
    "true_anomaly_0": LEO_true_anomaly_0
}

def create_leo_constellation(
    num_planes=2,
    satellites_per_plane=3
):

    constellation = []

    for plane in range(num_planes):

        raan = np.deg2rad(
            plane * 360 / num_planes
        )

        for sat in range(satellites_per_plane):

            true_anomaly = np.deg2rad(
                sat * 360 / satellites_per_plane
            )

            satellite = {
                "name": f"LEO-{len(constellation)+1:02d}",

                "plane": plane,

                "a": R_EARTH + 600e3,
                "e": 0.01,
                "inclination": np.deg2rad(53),

                "raan": raan,
                "arg_periapsis": 0.0,
                "true_anomaly_0": true_anomaly
            }

            constellation.append(satellite)

    return constellation

def create_gps_constellation(
    num_planes=6,
    satellites_per_plane=4
):

    constellation = []

    for plane in range(num_planes):

        raan = np.deg2rad(
            plane * 360 / num_planes
        )

        for sat in range(satellites_per_plane):

            true_anomaly = np.deg2rad(
                sat * 360 / satellites_per_plane
            )

            satellite = {
                "name": f"GPS-{len(constellation)+1:02d}",

                "plane": plane,

                "a": R_EARTH + 20_200e3,
                "e": 0.01,
                "inclination": np.deg2rad(55),

                "raan": raan,
                "arg_periapsis": 0.0,
                "true_anomaly_0": true_anomaly
            }

            constellation.append(satellite)

    return constellation

gps_constellation = create_gps_constellation()
print(len(gps_constellation))

leo_constellation = create_leo_constellation()
print(len(leo_constellation))

from coordinates import propagate_orbit

def propagate_constellation(constellation, times):

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

# Simulation time: 24 hours
simulation_time = 24 * 3600

# Number of simulation samples
num_steps = 3000

times = np.linspace(
    0,
    simulation_time,
    num_steps
)

gps_positions, gps_velocities = propagate_constellation(
    gps_constellation,
    times
)

leo_positions, leo_velocities = propagate_constellation(
    leo_constellation,
    times
)

leo_positions["LEO-01"]

gps_positions["GPS-01"]