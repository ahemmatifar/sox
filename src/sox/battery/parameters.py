from dataclasses import dataclass
from typing import Any, Callable, List

import numpy as np

Temp = Any  # degC
Current = Any
SOC = Any
OCV = Any
dOCVdT = Any
Resistance = Any
Capacitance = Any


@dataclass
class Inputs:
    """Input parameters for the battery model."""

    # electrical properties
    rc_pairs: int
    initial_rc_voltage: List[float]  # Element-i initial overpotential [V]
    voltage_high_cut: float  # Upper voltage cut-off [V]
    voltage_low_cut: float  # Lower voltage cut-off [V]
    capacity: float  # Cell capacity [A.h]
    initial_soc: float  # Initial SoC
    open_circuit_voltage: Callable[[SOC], OCV]  # Open-circuit voltage [V]
    entropic_change: Callable[[OCV, Temp], dOCVdT]  # Entropic change [V/K] (temp in degC)
    series_resistance: Callable[[Temp, Current, SOC], Resistance]  # R0 [Ohm]
    rc_resistance: List[Callable[[Temp, Current, SOC], Resistance]]  # [R1 [Ohm], R2 [Ohm], ..., Rn [Ohm]]
    rc_capacitance: List[Callable[[Temp, Current, SOC], Capacitance]]  # [C1 [F], C2 [F], ..., Cn [F]]

    # thermal properties
    initial_temperature: float  # Initial temperature [K]
    ambient_temperature: float  # Ambient temperature [K]
    cth_cell: float  # Cell thermal mass [J/K]
    cth_jig: float  # Jig thermal mass [J/K]
    k_cell_jig: float  # Cell-jig heat transfer coefficient [W/K]
    k_jig_air: float  # Jig-air heat transfer coefficient [W/K]


@dataclass
class Outputs:
    """Output variables from the battery model."""

    # electrical properties
    time: np.ndarray  # 'Time [s]'
    voltage: np.ndarray  # 'Voltage [V]'
    rc_voltage: List[np.ndarray]  # ['Element-1 overpotential [V]', ..., 'Element-n overpotential [V]']
    ocv: np.ndarray  # 'Open-circuit voltage [V]'
    current: np.ndarray  # 'Current [A]'
    power: np.ndarray  # 'Power [W]'
    resistance: np.ndarray  # 'Resistance [Ohm]'
    series_resistance: np.ndarray  # 'R0 [Ohm]'
    rc_resistance: List[np.ndarray]  # ['R1 [Ohm]', ..., 'Rn [Ohm]']
    rc_capacitance: List[np.ndarray]  # ['C1 [F]', ..., 'Cn [F]']
    soc: np.ndarray  # 'SoC'

    # thermal properties
    ambient_temperature: np.ndarray  # 'Ambient temperature [degC]'
    cell_temperature: np.ndarray  # 'Cell temperature [degC]'
    jig_temperature: np.ndarray  # 'Jig temperature [degC]'

    # other properties (not used in the model)
    # 'C-rate'
    # 'Discharge capacity [A.h]'
    # 'Throughput capacity [A.h]'
    # 'Discharge energy [W.h]'
    # 'Throughput energy [W.h]'
    # 'Heat transfer from cell to jig [W]'
    # 'Heat transfer from jig to ambient [W]'
    # 'Entropic change [V/K]'
    # 'Reversible heat generation [W]'
    # 'Element-0 irreversible heat generation [W]'
    # 'Element-1 irreversible heat generation [W]'
    # 'Irreversible heat generation [W]'
    # 'Total heat generation [W]'
