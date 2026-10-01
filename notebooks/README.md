# Notebooks

This directory contains interactive Jupyter notebooks demonstrating the GNSS LEO resilience library.

## Notebooks

### 1. Orbital Mechanics (`01_orbital_mechanics.ipynb`)
**Topics:**
- Kepler's equations and orbital propagation
- Satellite state vector calculations
- LEO vs GPS constellation comparison
- Altitude and velocity profiles

**Skills Gained:**
- Understanding orbital mechanics fundamentals
- Visualizing satellite trajectories
- Working with orbital elements

---

### 2. Signal Propagation (`02_signal_propagation.ipynb`)
**Topics:**
- Doppler shift calculations
- Pseudorange and pseudorange rate
- Path loss and atmospheric delays
- Carrier-to-noise density (C/N0)
- Inter-satellite link analysis

**Skills Gained:**
- Signal modeling for GNSS/LEO
- Understanding signal degradation
- Calculating observable quantities

---

### 3. Spoof/Jamming Analysis (`03_spoof_jamming_analysis.ipynb`)
**Topics:**
- Cross-layer PNT concepts
- Spoofing detection strategies
- Jamming resilience analysis
- LEO-augmented positioning
- Detection algorithm development

**Skills Gained:**
- Threat modeling for GNSS
- Cross-validation techniques
- Resilience evaluation methods

---

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Lab or Jupyter Notebook
- The gnss_leo library (install with `pip install -e .`)

### Running Notebooks

1. Install the library:
   ```bash
   pip install -e ".[jupyter]"
   ```

2. Start Jupyter:
   ```bash
   jupyter lab
   ```

3. Navigate to this directory and open a notebook

### Quick Start

To run all notebooks in sequence:
```bash
jupyter nbconvert --to notebook --execute 01_orbital_mechanics.ipynb
jupyter nbconvert --to notebook --execute 02_signal_propagation.ipynb
jupyter nbconvert --to notebook --execute 03_spoof_jamming_analysis.ipynb
```

## Tips for Working with Notebooks

- **Run cells sequentially**: Most notebooks assume cells are run in order
- **Modify parameters**: Try changing orbital parameters, times, or frequencies
- **Experiment**: The notebooks are designed for exploration—modify and re-run!
- **Save outputs**: Generated plots can be saved directly from the notebook

## Common Issues

**Issue**: `ModuleNotFoundError: No module named 'gnss_leo'`
- **Solution**: Make sure you've installed the library with `pip install -e .` from the project root

**Issue**: Plots not displaying
- **Solution**: Make sure you have matplotlib installed: `pip install matplotlib`

**Issue**: Long computation times
- **Solution**: Reduce `num_steps` in simulation parameters for faster testing

## Further Resources

- See `../docs/` for detailed API documentation
- See `../examples/` for standalone Python scripts
- Check `../tests/` to see example usage patterns

## Contributing

If you'd like to contribute new notebooks:
1. Use consistent naming: `NN_descriptive_name.ipynb`
2. Add markdown cells explaining concepts
3. Include docstrings for custom functions
4. Test thoroughly before submitting

---

**Happy learning! 🛰️**
