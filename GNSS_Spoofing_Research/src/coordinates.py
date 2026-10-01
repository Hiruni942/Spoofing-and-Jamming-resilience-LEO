import numpy as np
import matplotlib.pyplot as plt

#Defining earth
# Earth parameters

R_EARTH = 6_378_137.0       # Earth radius [m](We're using the WGS-84 equatorial radius for now.)
MU_EARTH = 3.986004418e14   # Earth's gravitational parameter [m^3/s^2]

# Satellite altitudes

LEO_ALTITUDE = 600e3       # 600 km
MEO_ALTITUDE = 20_200e3    # 20,200 km

# V2 : Full orbital orientaion

           
def solve_keplers_equation(M, e, tolerance=1e-12, max_iterations=100):
    """
    Solve M = E - e*sin(E) for eccentric anomaly E.
    """

    # Initial guess
    E = M if e < 0.8 else np.pi

    for _ in range(max_iterations):

        f = E - e * np.sin(E) - M
        f_prime = 1 - e * np.cos(E)

        delta_E = f / f_prime
        E -= delta_E

        if abs(delta_E) < tolerance:
            break

    return E

def eccentric_to_true_anomaly(E, e):

    numerator = np.sqrt(1 + e) * np.sin(E / 2)
    denominator = np.sqrt(1 - e) * np.cos(E / 2)

    nu = 2 * np.arctan2(numerator, denominator)

    return nu

def rotation_1(angle):
    """
    Rotation about x-axis.
    """

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s,  c]
    ])


def rotation_3(angle):
    """
    Rotation about z-axis.
    """

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ])
    
    
# Actual orbital-elements propagator

def orbital_elements_to_state(
    a,
    e,
    inclination,
    raan,
    arg_periapsis,
    true_anomaly
):

    # ------------------------------------------------
    # 1. Calculate orbital radius
    # ------------------------------------------------

    r = (
        a * (1 - e**2)
        / (1 + e * np.cos(true_anomaly))
    )

    # ------------------------------------------------
    # 2. Position in PQW frame
    # ------------------------------------------------

    position_pqw = np.array([
        r * np.cos(true_anomaly),
        r * np.sin(true_anomaly),
        0.0
    ])

    # ------------------------------------------------
    # 3. Velocity in PQW frame
    # ------------------------------------------------

    velocity_factor = np.sqrt(
        MU_EARTH / (a * (1 - e**2))
    )

    velocity_pqw = velocity_factor * np.array([
        -np.sin(true_anomaly),
        e + np.cos(true_anomaly),
        0.0
    ])

    # ------------------------------------------------
    # 4. Rotate PQW → ECI
    # ------------------------------------------------

    transformation = (
        rotation_3(raan)
        @ rotation_1(inclination)
        @ rotation_3(arg_periapsis)
    )

    position_eci = transformation @ position_pqw
    velocity_eci = transformation @ velocity_pqw

    return position_eci, velocity_eci

#propegator
def propagate_orbit(
    a,
    e,
    inclination,
    raan,
    arg_periapsis,
    true_anomaly_0,
    times
):

    # Initial eccentric anomaly
    E0 = 2 * np.arctan2(
        np.sqrt(1 - e) * np.sin(true_anomaly_0 / 2),
        np.sqrt(1 + e) * np.cos(true_anomaly_0 / 2)
    )

    # Initial mean anomaly
    M0 = E0 - e * np.sin(E0)

    # Mean motion
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
            a,
            e,
            inclination,
            raan,
            arg_periapsis,
            nu
        )

        positions.append(position)
        velocities.append(velocity)

    return (
        np.array(positions),
        np.array(velocities)
    )
    
simulation_time = 24 * 3600
num_steps = 2000

times = np.linspace(0, simulation_time, num_steps)