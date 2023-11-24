# SOX documentation

{doc}`get_started`

SOX is a playground for exploring battery state estimation methods written in Python. SOX provides a simple 
interface for running battery state of charge estimation methods with 
simulated cycling data and sensor noise and fault injection. This project consists of 

1. Battery plant model based on the Thevenin equivalent circuit.
2. Sensor noise models such as uniform, normal, Poisson and exponential. 
3. Sensor fault models such as offset, scaling, drift, and stuck-at. These faults can be injected randomly, or at any time during the simulation.
4. State estimation algorithms such as Coulomb counting (CC), Extended Kalman Filter (EKF), 
and Unscented Kalman Filter (UKF).

```{toctree}
:caption: 'Contents:'
:maxdepth: 1

Get Started <get_started>
Tutorial 1: Battery Cycling <tutorials/01 - battery cycling>
Tutorial 2: SOC Estimation with EKF <tutorials/02 - soc estimation by ekf>
```