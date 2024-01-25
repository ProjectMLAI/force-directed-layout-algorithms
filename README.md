# Enhanced Force Directed Layout Algorithms with Carbon Emission Visualization

## Dependencies
To use this package, install the necessary dependencies:

```bash
python3 -m pip install forcelayout
python3 -m pip install PyQt6
python3 -m pip install tkinter
python3 -m pip install PIL
python3 -m pip install codecarbon
### Additional dependencies if any
python3 -m pip install -r requirements.txt
```
or

```bash
python3 -m pip install -r requirements.txt
```
`
## Algorithms 
Locations of the three main algorithms of this project:
- [Chalmers' 1996 algorithm](https://ieeexplore.ieee.org/document/567787) is implemented in `forcelayout/algorithms/neighbour_sampling.py`
- [Hybrid Layout algorithm](https://ieeexplore.ieee.org/document/1173161) is implemented in `forcelayout/algorithms/hybrid.py`
- [Pivot Layout algorithm](https://ieeexplore.ieee.org/document/1249012) is implemented in `forcelayout/algorithms/pivot.py`

### Usage

[Documentation](forcelayout/README.md) on full usage of the `forcelayout` package is available in the `forcelayout/README.md`

### Examples

Examples are contained in the `examples/` folder. Three command line scripts are included and a jupyter notebook.

nhanced Visualization and Carbon Emission Calculation
Examples
New scripts in the examples/ folder are added:

com.py: The main script for launching the PyQt6-based GUI. It provides a user-friendly interface, integrating data handling, algorithm visualization, and carbon emission calculation.

data.py: Handles data processing using tkinter and PIL, and visualizes algorithm outcomes. It integrates codecarbon for real-time carbon emission tracking during algorithm execution.

calculator.py: A dedicated PyQt6 widget for calculating and displaying carbon emissions. Offers interactive tools for users to input data and view the carbon footprint of different algorithms.


### Testing

In order to run tests, `pytest` is required:

```bash
python3 -m pip install pytest
```

To run the test cases run the following command from the root directory:

```bash
python3 -m pytest forcelayout/ tests/forcelayout
```

Note that the test cases are written and run on Ubuntu 18.04 with Python 3.6.7 with Pytest 4.0.2.

### Datasets

I do not own the datasets in this repository, they can be accessed from their source at:
- [Poker hands](https://archive.ics.uci.edu/ml/datasets/Poker+Hand)
- [Iris](https://archive.ics.uci.edu/ml/datasets/iris)
