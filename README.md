# SOX
Playground for exploring battery state estimation methods.

This project provides a simple playground for running battery state of charge estimation methods 
(Coulomb counting and Extended Kalman Filter are currently supported) with simulated cycling data and 
sensor noise and fault injection. 

Multiple sensor noise and fault models available for exploration. Random noise models include
uniform, normal, Poisson and exponential. Sensor faults include offset, scaling, drift, and stuck-at. Faults 
can be injected randomly, or at any time during the simulation.

# Examples
Example notebooks are available in the [examples](examples/) directory.

# Installation
1. clone the repository 
    ```bash
    git clone https://github.com/ahemmatifar/sox.git
    ```
2. Change to project directory and install the project
    ```bash
    cd sox
    make dev_install
    ```