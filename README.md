# Discrete Event Systems

This repositories houses the work for my final project for the course Discrete Event Systems that I am taking at Rowan University during Fall 2025 for my graduate degree in Electrical Computer Engineering.

# Building Paper

The included shell script `build_tex.sh` will run `tex/Dockerfile` and copy the artifacts to `tex/build_artifacts`.

# Running simulation

To run the simulation, we execute src/ as a python module as it includes a `__main__.py` and as such will be treated as a module when passed to `python`.

`python src/` to run.

`python -m pdb -c continue src/` to run with debugger.

`python src/ --help` to print help.

# Tests

Pytest is utilized as a test suite to provide a mechanism to assert reproducability of the original paper.

`pytest tests` to run.

`pytest --pdb tests` to run with debugger.

`pytest --trace tests` to run and pass with debugger at start of each test call`.

# Development

Conda will be utilized act as the system packager manager. This project is being developed in a Linux VM using WSL. It is advised to use Linux as no dependencies are being tracked for Windows. I make no promise of an easy development environment in any other operation system.

Download [`miniforge`](https://github.com/conda-forge/miniforge?tab=readme-ov-file#requirements-and-installers) for your OS and install it under your user. You can find directions on downloading and initilization for your shell and then do a `conda env create -f envionrment.yaml` (assumes your working directory in shell is this repository).

For dependencies that cannot be placed into a conda environment, Docker is utilized. An associated dockerfile will be present for each.

Please see the official [Docker documentation](https://daniel.es/blog/how-to-install-docker-in-wsl-without-docker-desktop/#how-to-install-docker-in-wsl-without-installing-docker-desktop) for setup. 