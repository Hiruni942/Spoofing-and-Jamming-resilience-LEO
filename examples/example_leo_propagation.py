"""
Example: LEO satellite constellation propagation and analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from gnss_leo.core import create_leo_constellation, propagate_constellation, SIMULATION_TIME, DEFAULT_NUM_STEPS
from gnss_leo.utils import plot_constellation_positions, plot_altitude_profile
from gnss_leo.signal import calculate_distance, calculate_doppler_shift, calculate_radial_velocity

# Create time array
times = np.linspace(0, SIMULATION_TIME, DEFAULT_NUM_STEPS)
print(f"Simulating {SIMULATION_TIME/3600:.1f} hours with {len(times)} samples\n")

# Create LEO constellation
leo_constellation = create_leo_constellation(num_planes=2, satellites_per_plane=3)
print(f"Created LEO constellation with {len(leo_constellation)} satellites:")
for sat in leo_constellation:
    print(f"  - {sat['name']} in plane {sat['plane']}")

# Propagate constellation
print("\nPropagating constellation...")
leo_positions, leo_velocities = propagate_constellation(leo_constellation, times)

# Plot constellation
print("Creating visualizations...")
fig1, ax1 = plot_constellation_positions(leo_positions, times, title="LEO Constellation 3D Trajectory")
plt.tight_layout()
plt.savefig("leo_constellation_3d.png", dpi=100)
print("  ✓ Saved: leo_constellation_3d.png")

# Plot altitude profile for first satellite
sat_name = leo_constellation[0]["name"]
fig2, ax2 = plot_altitude_profile(leo_positions[sat_name], times, satellite_name=sat_name)
plt.tight_layout()
plt.savefig(f"{sat_name.lower()}_altitude.png", dpi=100)
print(f"  ✓ Saved: {sat_name.lower()}_altitude.png")

# Calculate Doppler shifts between satellites
print("\nCalculating Doppler shifts between satellites...")
receiver_sat = leo_constellation[0]["name"]
transmitter_sat = leo_constellation[1]["name"]

receiver_pos = leo_positions[receiver_sat][0]
receiver_vel = leo_velocities[receiver_sat][0]
transmitter_pos = leo_positions[transmitter_sat][0]
transmitter_vel = leo_velocities[transmitter_sat][0]

# Calculate relative velocity
relative_vel = transmitter_vel - receiver_vel
distance = calculate_distance(receiver_pos, transmitter_pos)
radial_vel = calculate_radial_velocity(transmitter_pos - receiver_pos, relative_vel)

# GPS L1 frequency
gps_l1_freq = 1.57542e9  # Hz

doppler_shift = calculate_doppler_shift(radial_vel, gps_l1_freq)

print(f"\nLink from {transmitter_sat} to {receiver_sat}:")
print(f"  Distance: {distance/1e3:.1f} km")
print(f"  Radial velocity: {radial_vel:.1f} m/s")
print(f"  Doppler shift: {doppler_shift - gps_l1_freq:.1f} Hz")
print(f"  Shifted frequency: {doppler_shift/1e9:.9f} GHz")

print("\n✓ Example completed successfully!")
