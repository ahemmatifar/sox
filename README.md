# SOX
Playground for exploring battery state estimation methods.

This project provides a simple playground for running battery state of charge estimation methods with 
simulated cycling data and sensor noise and fault injection. 

Multiple sensor noise and fault models available for exploration. Random noise models include
uniform, normal, Poisson and exponential. Sensor faults include offset, scaling, drift, and stuck-at. Faults 
can be injected randomly, or at any time during the simulation.

State estimation methods currently supported include Coulomb counting (CC), Extended Kalman Filter (EKF), 
and Unscented Kalman Filter (UKF).

Documentation and tutorials can be found at [SOX Documentation](https://sox.readthedocs.io/en/latest/).