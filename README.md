# 🧦 SOX

Playground for exploring battery state estimation methods.

[SOX](https://sox.readthedocs.io/en/latest/) provides a simple playground for running battery state of charge estimation methods with simulated cycling data and sensor noise and fault injection. 

The project supports multiple state estimation methods, including Coulomb counting (CC), Extended Kalman Filter (EKF), and Unscented Kalman Filter (UKF).

The project offers multiple sensor noise and fault models for exploration. Random noise models such as uniform, normal, Poisson, and exponential are available. Sensor faults include offset, scaling, drift, and stuck-at. These faults can be injected randomly or at any time during the simulation.

The [full documentation](https://sox.readthedocs.io/en/latest/) as well as [tutorials](https://sox.readthedocs.io/en/latest/tutorials/index.html) and [API reference](https://sox.readthedocs.io/en/latest/autoapi/index.html) is also available.