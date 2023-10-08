from dataclasses import dataclass
from typing import List, Callable, Any

Temp = Any  # degC
Current = Any
SOC = Any
OCV = Any
dOCVdT = Any
Resistance = Any
Capacitance = Any


@dataclass
class Parameters:
    # electrical properties
    rc_pairs: int
    initial_rc_voltage: List[float]  # Element-1 initial overpotential [V]
    toc_voltage_cut_off: float  # Upper voltage cut-off [V]
    capacity: float  # Cell capacity [A.h]
    initial_soc: float  # Initial SoC
    bod_voltage_cut_off: float  # Lower voltage cut-off [V]
    open_circuit_voltage: Callable[[SOC], OCV]  # Open-circuit voltage [V]
    entropic_change: Callable[[OCV, Temp], dOCVdT]  # Entropic change [V/K] (temp in degC)
    series_resistance: Callable[[Temp, Current, SOC], Resistance]  # R0 [Ohm]
    rc_resistance: List[Callable[[Temp, Current, SOC], Resistance]]  # [R1 [Ohm], R2 [Ohm], ..., Rn [Ohm]]
    rc_capacitance: List[Callable[[Temp, Current, SOC], Capacitance]]  # [C1 [F], C2 [F], ..., Cn [F]]

    # thermal properties
    initial_temperature: float  # Initial temperature [K]
    ambient_temperature: float  # Ambient temperature [K]
    cp_cell: float  # Cell thermal mass [J/K]
    cp_jig: float  # Jig thermal mass [J/K]
    h_jig: float  # Cell-jig heat transfer coefficient [W/K]
    h_air: float  # Jig-air heat transfer coefficient [W/K]
