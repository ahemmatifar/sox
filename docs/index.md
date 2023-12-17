# 🧦 SOX documentation

[SOX](https://github.com/ahemmatifar/sox/tree/feature/add_tutorials) is a playground for exploring battery state estimation methods written in Python. SOX provides a simple interface for running battery state of charge estimation methods with 
simulated cycling data and sensor noise and fault injection. 

This project consists of
1. Battery plant model based on the Thevenin equivalent circuit.
1. State estimation algorithms such as Coulomb counting (CC), Extended Kalman Filter (EKF), 
and Unscented Kalman Filter (UKF).
1. Sensor noise models such as uniform, normal, Poisson and exponential. 
1. Sensor fault models such as offset, scaling, drift, and stuck-at. These faults can be injected randomly, or at any time during the simulation.

Table of contents:
```{toctree}
:maxdepth: 1

🚀 Get Started <get_started>
📖 Tutorials <tutorials/index>
📦 Source Code <https://github.com/ahemmatifar/sox>
```