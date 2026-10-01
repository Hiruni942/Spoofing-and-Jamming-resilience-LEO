# Project Architecture

## Overview

The GNSS LEO Resilience library is organized into four main modules:

### Core Module (`gnss_leo.core`)
Handles orbital mechanics and satellite positions.

**Submodules:**
- `constants.py` - Physical constants and default orbital parameters
- `orbit.py` - Kepler's equation solver and orbital propagation
- `constellation.py` - LEO and GPS constellation creation and propagation
- `coordinates.py` - Coordinate system transformations (ECI, ECEF, geodetic)
- `rotations.py` - Rotation matrices for coordinate transforms

### Signal Module (`gnss_leo.signal`)
Handles signal propagation and reception modeling.

**Submodules:**
- `doppler.py` - Doppler shift calculations
- `ranging.py` - Distance and pseudorange calculations
- `propagation.py` - Signal propagation models (path loss, atmospheric delays, SNR)

### Utils Module (`gnss_leo.utils`)
Utilities for visualization and analysis.

**Submodules:**
- `plotting.py` - Plotting functions for trajectories and analysis

### Detection Module (`gnss_leo.detection`)
(Future) Spoof and jamming detection algorithms using ML/AI.

## Class Hierarchy

```
gnss_leo/
├── core/
│   ├── constants (module-level constants)
│   ├── orbit (functions for propagation)
│   ├── constellation (functions for multi-satellite systems)
│   ├── coordinates (functions for coordinate transforms)
│   └── rotations (functions for matrix rotations)
├── signal/
│   ├── doppler (Doppler effect modeling)
│   ├── ranging (Range measurements)
│   └── propagation (Signal path models)
├── utils/
│   └── plotting (Visualization tools)
└── detection/
    └── (detection algorithms - future)
```

## Key Concepts

### Orbital Elements
Each satellite is defined by six Keplerian elements:
- `a` - Semi-major axis [m]
- `e` - Eccentricity (0 = circular)
- `inclination` - Orbital inclination [rad]
- `raan` - Right ascension of ascending node [rad]
- `arg_periapsis` - Argument of periapsis [rad]
- `true_anomaly` - True anomaly [rad]

### Coordinate Systems
- **ECI** (Earth-Centered Inertial) - Inertial reference frame
- **ECEF** (Earth-Centered Earth-Fixed) - Earth-fixed, rotating frame
- **Geodetic** - Latitude, longitude, altitude on WGS-84 ellipsoid

### Signal Parameters
- **Pseudorange** - Measured range including receiver clock bias
- **Doppler Shift** - Frequency shift due to satellite motion
- **Path Loss** - Signal attenuation over distance
- **C/N0** - Carrier-to-Noise density [dB-Hz]
