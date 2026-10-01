# GNSS LEO Resilience

A comprehensive Python library for simulating GNSS and LEO satellite systems, analyzing spoofing/jamming resilience, and developing cross-layer PNT (Position, Navigation, and Timing) solutions.

## Overview

This project explores:
- **GNSS Simulation**: GPS and other GNSS constellation modeling
- **LEO Constellation Dynamics**: Low Earth Orbit satellite propagation and kinematics
- **Cross-Layer Integration**: Leveraging LEO signals for PNT resilience against spoofing/jamming
- **Signal Analysis**: Doppler shifts, pseudoranges, and signal propagation models
- **Spoof/Jamming Detection**: AI-driven detection using cross-layer validation

## Features

✨ **Complete Orbital Mechanics**
- Accurate satellite propagation using Kepler's equations
- LEO and GPS constellation generation
- Multiple coordinate system transformations (ECI, ECEF, geodetic)

📡 **Signal Processing**
- Doppler shift calculation (relativistic and non-relativistic)
- Pseudorange and pseudorange rate modeling
- Signal propagation (path loss, atmospheric delays)
- Carrier-to-noise density (C/N0) estimation

🛰️ **Constellation Analysis**
- Multi-satellite constellation propagation
- Visibility and elevation angle calculations
- Inter-satellite link analysis

🔬 **Extensible Architecture**
- Modular design for easy extension
- Prepared for ML-based detection algorithms
- Well-tested with comprehensive unit tests

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Hiruni942/Spoofing-and-Jamming-resilience-LEO.git
cd Spoofing-and-Jamming-resilience-LEO

# Install in development mode
pip install -e .

# Optional: Install development dependencies
pip install -e ".[dev]"

# Optional: Install Jupyter for notebooks
pip install -e ".[jupyter]"
```

### Basic Usage

```python
import numpy as np
from gnss_leo.core import create_leo_constellation, propagate_constellation
from gnss_leo.signal import calculate_doppler_shift, calculate_radial_velocity
from gnss_leo.utils import plot_constellation_positions

# Create a LEO constellation
leo_const = create_leo_constellation(num_planes=2, satellites_per_plane=3)

# Propagate for 24 hours
times = np.linspace(0, 24*3600, 1000)
positions, velocities = propagate_constellation(leo_const, times)

# Calculate Doppler shift between two satellites
from gnss_leo.signal import calculate_distance
dist = calculate_distance(positions["LEO-01"][0], positions["LEO-02"][0])
print(f"Distance: {dist/1e3:.1f} km")

# Plot trajectories
plot_constellation_positions(positions, times)
```

## Project Structure

```
Spoofing-and-Jamming-resilience-LEO/
├── src/gnss_leo/           # Main package
│   ├── core/               # Orbital mechanics
│   ├── signal/             # Signal processing
│   ├── utils/              # Visualization & utilities
│   └── detection/          # ML-based detection (future)
├── notebooks/              # Jupyter notebooks
│   ├── 01_orbital_mechanics.ipynb
│   ├── 02_signal_propagation.ipynb
│   └── 03_spoof_jamming_analysis.ipynb
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── examples/               # Example scripts
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## Documentation

- **[Architecture](docs/architecture.md)** - System design and module overview
- **[API Reference](docs/api.md)** - Detailed function documentation
- **Notebooks** - Interactive examples in `notebooks/`
- **Examples** - Standalone scripts in `examples/`

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gnss_leo

# Run specific test file
pytest tests/test_orbit.py -v
```

## Notebooks

Interactive Jupyter notebooks are available in the `notebooks/` directory:

1. **Orbital Mechanics** - Satellite propagation fundamentals
2. **Signal Propagation** - Doppler, pseudorange, and atmospheric effects
3. **Spoof/Jamming Analysis** - Cross-layer resilience concepts

Launch notebooks with:
```bash
jupyter lab notebooks/
```

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## References

- Curtis, H. D. (2013). *Orbital Mechanics for Engineering Students*
- Parkinson, B. W., & Spilker, J. J. (1996). *Global Positioning System*
- Kaplan, E. D., & Hegarty, C. (2017). *Understanding GPS/GNSS*

## License

MIT License - see LICENSE file for details

## Authors

GNSS LEO Research Team

---

**Questions or issues?** Open an issue on [GitHub](https://github.com/Hiruni942/Spoofing-and-Jamming-resilience-LEO/issues)
