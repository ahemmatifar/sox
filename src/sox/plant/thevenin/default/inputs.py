import os

import pybamm as pb
from scipy.interpolate import interp1d

from sox.plant.thevenin.parameters import Inputs

path = os.path.dirname(__file__)

ocv_data = pb.parameters.process_1D_data("thevenin_ocv.csv", path=path)
r0_data = pb.parameters.process_3D_data_csv("thevenin_r0.csv", path=path)
r1_data = pb.parameters.process_3D_data_csv("thevenin_r1.csv", path=path)
c1_data = pb.parameters.process_3D_data_csv("thevenin_c1.csv", path=path)
dOCVdT_data = pb.parameters.process_2D_data_csv("thevenin_docvdt.csv", path=path)

# scales resistance and capacitance data
scale_factor = 10.0
r0_data = r0_data[0], (r0_data[1][0], r0_data[1][1] * scale_factor)
r1_data = r1_data[0], (r1_data[1][0], r1_data[1][1] * scale_factor)
c1_data = c1_data[0], (c1_data[1][0], c1_data[1][1] / scale_factor * 2)


def open_circuit_voltage(soc):
    """Open circuit voltage as a function of state of charge."""
    name, (x, y) = ocv_data
    return pb.Interpolant(x, y, soc, name, extrapolate=True)


def r0(temperature, current, soc):
    """Series resistance as a function of temperature, current and state of charge."""
    name, (x, y) = r0_data
    return pb.Interpolant(x, y, [temperature, current, soc], name, extrapolate=True)


def r1(temperature, current, soc):
    """Resistance of the first RC pair as a function of temperature, current and state of charge."""
    name, (x, y) = r1_data
    return pb.Interpolant(x, y, [temperature, current, soc], name, extrapolate=True)


def c1(temperature, current, soc):
    """Capacitance of the first RC pair as a function of temperature, current and state of charge."""
    name, (x, y) = c1_data
    return pb.Interpolant(x, y, [temperature, current, soc], name, extrapolate=True)


def entropic_change(ocv, temperature):
    """Entropic change in open circuit voltage as a function of open circuit voltage and
    temperature."""
    name, (x, y) = dOCVdT_data
    return pb.Interpolant(x, y, [ocv, temperature], name, extrapolate=True)


default_inputs = Inputs(
    # electrical properties
    rc_pairs=1,
    initial_rc_voltage=[0.0],  # V
    voltage_high_cut=4.5,
    voltage_low_cut=2.5,
    capacity=10,  # Ah
    initial_soc=0.8,
    open_circuit_voltage=open_circuit_voltage,
    entropic_change=entropic_change,
    series_resistance=r0,  # Ohm
    rc_resistance=[r1],  # Ohm
    rc_capacitance=[c1],  # F
    # thermal properties
    initial_temperature=25,  # degC
    ambient_temperature=25,  # degC
    cth_cell=200.0,  # J/K
    cth_jig=100.0,  # J/K
    k_cell_jig=2.0,  # W/K
    k_jig_air=2.0,  # W/K
)
